"""Tkinter GUI for editing Pokemon Legends: Z-A save file boxes.

Workflow: pull the save file off the Switch's SD card with a homebrew save
manager (e.g. Checkpoint/JKSV) on a CFW console, edit it here, then push the
edited file back the same way. This tool never talks to the console itself.
"""

from __future__ import annotations

import random
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from . import sprites, theme
from .za import species
from .za.pa9 import PA9
from .za.save import BOX_COUNT, SLOTS_PER_BOX, SAV9ZA

IDENTITY_FIELDS: list[tuple[str, str, bool]] = [
    ("form", "Form", False),
    ("level", "Level", False),
    ("nickname", "Nickname", True),
    ("original_trainer_name", "OT Name", True),
    ("tid16", "TID", False),
    ("sid16", "SID", False),
    ("nature", "Nature (0-24)", False),
    ("ability", "Ability (id)", False),
    ("ability_number", "Ability Slot (0/1/2/4)", False),
    ("gender", "Gender (0=M 1=F 2=N)", False),
    ("ball", "Ball ID", False),
    ("held_item", "Held Item ID", False),
]

IV_FIELDS = [("iv_hp", "HP"), ("iv_atk", "Atk"), ("iv_def", "Def"), ("iv_spa", "SpA"), ("iv_spd", "SpD"), ("iv_spe", "Spe")]
EV_FIELDS = [("ev_hp", "HP"), ("ev_atk", "Atk"), ("ev_def", "Def"), ("ev_spa", "SpA"), ("ev_spd", "SpD"), ("ev_spe", "Spe")]
MOVE_FIELDS = [("move1", "Move 1"), ("move2", "Move 2"), ("move3", "Move 3"), ("move4", "Move 4")]

_ALL_SPECIES_OPTIONS = species.display_options()


class SpeciesPicker(ttk.Frame):
    """A searchable dropdown over the ~232 species available in Legends Z-A.
    Type to filter by name; you can also type a bare National Dex number
    directly (accepted even if it's not in the Z-A list, since there's no
    legality checker here -- that's on you)."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.var = tk.StringVar()
        self.combo = ttk.Combobox(self, textvariable=self.var, values=_ALL_SPECIES_OPTIONS, width=22)
        self.combo.pack()
        self.combo.bind("<KeyRelease>", self._on_keyrelease)

    def _on_keyrelease(self, event: tk.Event) -> None:
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return
        typed = self.var.get().strip().lower()
        if not typed:
            self.combo["values"] = _ALL_SPECIES_OPTIONS
        else:
            self.combo["values"] = [o for o in _ALL_SPECIES_OPTIONS if typed in o.lower()]

    def get_species_number(self) -> int:
        return species.parse_selection(self.var.get())

    def set_species_number(self, number: int) -> None:
        if not number:
            self.var.set("")
            return
        name = species.name_for(number)
        if name:
            self.var.set(f"{number:03d}  {name}")
        else:
            self.var.set(f"{number:03d}  (not in Z-A list)")


class PokeHexApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PokeHex")
        self.geometry("1040x620")
        theme.apply(self)

        self.sav: SAV9ZA | None = None
        self.save_path: str | None = None
        self.current_box = 0
        self.current_slot: int | None = None
        self.fields: dict[str, tk.Variable] = {}
        self._sprite_image = None  # keep a reference so Tk doesn't garbage-collect it

        self._build_menu()
        self._build_header()
        self._build_layout()

    # -- layout ---------------------------------------------------------
    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Save...", command=self.open_save)
        file_menu.add_command(label="Save (backs up original)", command=self.save_in_place)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=theme.BG)
        header.pack(side="top", fill="x")
        canvas = tk.Canvas(header, width=280, height=64, bg=theme.BG, highlightthickness=0)
        canvas.pack(side="left", padx=12, pady=8)
        theme.draw_logo(canvas)
        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x")

    def _build_layout(self) -> None:
        body = ttk.Frame(self)
        body.pack(side="top", fill="both", expand=True)

        left = ttk.Frame(body, style="Panel.TFrame", padding=8)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="BOX (1-32)", style="Panel.TLabel", font=theme.FONT_MONO_BOLD).pack(anchor="w")
        self.box_var = tk.IntVar(value=1)
        ttk.Spinbox(
            left, from_=1, to=BOX_COUNT, textvariable=self.box_var, width=5, command=self.refresh_slot_list,
        ).pack(anchor="w", pady=(2, 8))

        self.slot_list = tk.Listbox(
            left, width=30, height=30, font=theme.FONT_MONO,
            bg=theme.PANEL_ALT, fg=theme.FG, selectbackground=theme.ACCENT_DIM,
            selectforeground=theme.BG, highlightthickness=1, highlightbackground=theme.BORDER,
            relief="flat", borderwidth=0,
        )
        self.slot_list.pack(fill="y", expand=True)
        self.slot_list.bind("<<ListboxSelect>>", self.on_slot_select)

        right = ttk.Frame(body, padding=(12, 8))
        right.pack(side="left", fill="both", expand=True)

        top_row = ttk.Frame(right)
        top_row.pack(side="top", fill="x")

        self.sprite_canvas = tk.Canvas(top_row, width=96, height=96, highlightthickness=0)
        self.sprite_canvas.pack(side="left", padx=(0, 16))
        theme.draw_sprite_placeholder(self.sprite_canvas)

        identity_frame = ttk.Labelframe(top_row, text="IDENTITY", padding=8)
        identity_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(identity_frame, text="Species").grid(row=0, column=0, sticky="w", padx=(0, 4), pady=2)
        self.species_picker = SpeciesPicker(identity_frame)
        self.species_picker.grid(row=0, column=1, sticky="w", padx=(0, 16), pady=2)

        self._build_field_grid(identity_frame, IDENTITY_FIELDS, start_row=1)

        mid_row = ttk.Frame(right)
        mid_row.pack(side="top", fill="x", pady=8)

        iv_frame = ttk.Labelframe(mid_row, text="IVs", padding=8)
        iv_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))
        self._build_stat_row(iv_frame, IV_FIELDS)

        ev_frame = ttk.Labelframe(mid_row, text="EVs", padding=8)
        ev_frame.pack(side="left", fill="both", expand=True, padx=6)
        self._build_stat_row(ev_frame, EV_FIELDS)

        move_frame = ttk.Labelframe(right, text="MOVES", padding=8)
        move_frame.pack(side="top", fill="x", pady=(0, 8))
        self._build_move_row(move_frame)

        btn_frame = ttk.Frame(right)
        btn_frame.pack(side="top", fill="x", pady=4)
        ttk.Button(btn_frame, text="Apply to Slot", command=self.apply_to_slot).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="Make Shiny", command=self.make_shiny).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Clear Slot", command=self.clear_slot).pack(side="left", padx=6)

        self.status_var = tk.StringVar(value="Open a save file to begin.")
        status_bar = tk.Label(
            self, textvariable=self.status_var, anchor="w", bg=theme.PANEL, fg=theme.FG_DIM,
            font=theme.FONT_MONO, padx=8, pady=4,
        )
        status_bar.pack(side="bottom", fill="x")

    def _build_field_grid(self, parent: ttk.Frame, specs: list[tuple[str, str, bool]], start_row: int = 0) -> None:
        for i, (key, label, is_str) in enumerate(specs):
            row, col = divmod(i, 2)
            row += start_row
            ttk.Label(parent, text=label).grid(row=row, column=col * 2, sticky="w", padx=(0, 4), pady=2)
            var: tk.Variable = tk.StringVar() if is_str else tk.IntVar(value=0)
            ttk.Entry(parent, textvariable=var, width=14).grid(row=row, column=col * 2 + 1, sticky="w", padx=(0, 16), pady=2)
            self.fields[key] = var

    def _build_stat_row(self, parent: ttk.Frame, specs: list[tuple[str, str]]) -> None:
        for i, (key, label) in enumerate(specs):
            ttk.Label(parent, text=label).grid(row=0, column=i, padx=4)
            var = tk.IntVar(value=0)
            ttk.Entry(parent, textvariable=var, width=5).grid(row=1, column=i, padx=4)
            self.fields[key] = var

    def _build_move_row(self, parent: ttk.Frame) -> None:
        for i, (key, label) in enumerate(MOVE_FIELDS):
            ttk.Label(parent, text=label).grid(row=0, column=i, padx=6)
            var = tk.IntVar(value=0)
            ttk.Entry(parent, textvariable=var, width=10).grid(row=1, column=i, padx=6)
            self.fields[key] = var

    # -- file ops ---------------------------------------------------------
    def open_save(self) -> None:
        path = filedialog.askopenfilename(title="Open Legends Z-A save file")
        if not path:
            return
        try:
            self.sav = SAV9ZA.load(path)
        except Exception as exc:  # noqa: BLE001 -- surface any load failure to the user
            messagebox.showerror("Failed to open save", str(exc))
            return
        self.save_path = path
        self.current_slot = None
        self.status_var.set(f"Loaded {path}")
        self.refresh_slot_list()

    def save_in_place(self) -> None:
        if not self.sav or not self.save_path:
            messagebox.showwarning("No save loaded", "Open a save file first.")
            return
        if not messagebox.askyesno(
            "Overwrite save?",
            "This overwrites your save file (a .bak backup of the original will be made first). Continue?",
        ):
            return
        backup = self.save_path + ".bak"
        try:
            shutil.copyfile(self.save_path, backup)
            self.sav.save(self.save_path)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Save failed", str(exc))
            return
        self.status_var.set(f"Saved. Original backed up to {backup}")

    def save_as(self) -> None:
        if not self.sav:
            messagebox.showwarning("No save loaded", "Open a save file first.")
            return
        path = filedialog.asksaveasfilename(title="Save as")
        if not path:
            return
        self.sav.save(path)
        self.status_var.set(f"Saved to {path}")

    # -- box/slot browsing ---------------------------------------------
    def refresh_slot_list(self) -> None:
        if not self.sav:
            return
        self.current_box = self.box_var.get() - 1
        self.slot_list.delete(0, "end")
        for slot in range(SLOTS_PER_BOX):
            if self.sav.is_slot_empty(self.current_box, slot):
                self.slot_list.insert("end", f"{slot + 1:02d}  -- empty --")
            else:
                pkm = self.sav.get_box_slot(self.current_box, slot)
                name = species.name_for(pkm.species) or f"Dex #{pkm.species}"
                self.slot_list.insert("end", f"{slot + 1:02d}  {name:<12} Lv.{pkm.stat_level}")

    def on_slot_select(self, _event: object) -> None:
        selection = self.slot_list.curselection()
        if not selection or not self.sav:
            return
        self.current_slot = selection[0]
        pkm = self.sav.get_box_slot(self.current_box, self.current_slot)
        self._load_form_from_pkm(pkm)
        self._refresh_sprite(pkm.species)

    def _refresh_sprite(self, species: int) -> None:
        image = sprites.load_sprite(species, size=96) if species else None
        if image is not None:
            self._sprite_image = image
            self.sprite_canvas.delete("all")
            self.sprite_canvas.configure(bg=theme.PANEL_ALT, highlightthickness=1, highlightbackground=theme.BORDER)
            self.sprite_canvas.create_image(48, 48, image=image)
        else:
            self._sprite_image = None
            theme.draw_sprite_placeholder(self.sprite_canvas)

    def _load_form_from_pkm(self, pkm: PA9) -> None:
        self.species_picker.set_species_number(pkm.species)
        self.fields["form"].set(pkm.form)
        self.fields["level"].set(pkm.stat_level)
        self.fields["nickname"].set(pkm.nickname)
        self.fields["original_trainer_name"].set(pkm.original_trainer_name)
        self.fields["tid16"].set(pkm.tid16)
        self.fields["sid16"].set(pkm.sid16)
        self.fields["nature"].set(pkm.nature)
        self.fields["ability"].set(pkm.ability)
        self.fields["ability_number"].set(pkm.ability_number)
        self.fields["gender"].set(pkm.gender)
        self.fields["ball"].set(pkm.ball)
        self.fields["held_item"].set(pkm.held_item)
        self.fields["iv_hp"].set(pkm.iv_hp)
        self.fields["iv_atk"].set(pkm.iv_atk)
        self.fields["iv_def"].set(pkm.iv_def)
        self.fields["iv_spa"].set(pkm.iv_spa)
        self.fields["iv_spd"].set(pkm.iv_spd)
        self.fields["iv_spe"].set(pkm.iv_spe)
        self.fields["ev_hp"].set(pkm.ev_hp)
        self.fields["ev_atk"].set(pkm.ev_atk)
        self.fields["ev_def"].set(pkm.ev_def)
        self.fields["ev_spa"].set(pkm.ev_spa)
        self.fields["ev_spd"].set(pkm.ev_spd)
        self.fields["ev_spe"].set(pkm.ev_spe)
        self.fields["move1"].set(pkm.move(0))
        self.fields["move2"].set(pkm.move(1))
        self.fields["move3"].set(pkm.move(2))
        self.fields["move4"].set(pkm.move(3))

    def _build_pkm_from_form(self, pkm: PA9) -> PA9:
        if pkm.pid == 0:
            pkm.pid = random.getrandbits(32)
        if pkm.encryption_constant == 0:
            pkm.encryption_constant = random.getrandbits(32)

        pkm.species = self.species_picker.get_species_number()
        pkm.form = self.fields["form"].get()
        level = max(1, min(100, self.fields["level"].get()))
        pkm.stat_level = level
        pkm.met_level = level
        pkm.nickname = self.fields["nickname"].get()
        pkm.original_trainer_name = self.fields["original_trainer_name"].get()
        pkm.tid16 = self.fields["tid16"].get()
        pkm.sid16 = self.fields["sid16"].get()
        pkm.nature = self.fields["nature"].get()
        pkm.ability = self.fields["ability"].get()
        pkm.ability_number = self.fields["ability_number"].get()
        pkm.gender = self.fields["gender"].get()
        pkm.ball = self.fields["ball"].get()
        pkm.held_item = self.fields["held_item"].get()
        pkm.iv_hp = self.fields["iv_hp"].get()
        pkm.iv_atk = self.fields["iv_atk"].get()
        pkm.iv_def = self.fields["iv_def"].get()
        pkm.iv_spa = self.fields["iv_spa"].get()
        pkm.iv_spd = self.fields["iv_spd"].get()
        pkm.iv_spe = self.fields["iv_spe"].get()
        pkm.ev_hp = self.fields["ev_hp"].get()
        pkm.ev_atk = self.fields["ev_atk"].get()
        pkm.ev_def = self.fields["ev_def"].get()
        pkm.ev_spa = self.fields["ev_spa"].get()
        pkm.ev_spd = self.fields["ev_spd"].get()
        pkm.ev_spe = self.fields["ev_spe"].get()
        pkm.set_move(0, self.fields["move1"].get())
        pkm.set_move(1, self.fields["move2"].get())
        pkm.set_move(2, self.fields["move3"].get())
        pkm.set_move(3, self.fields["move4"].get())
        for i in range(4):
            if pkm.move(i) != 0 and pkm.move_pp(i) == 0:
                pkm.set_move_pp(i, 1)
        pkm.stat_hp_current = max(pkm.stat_hp_current, 1)
        return pkm

    def apply_to_slot(self) -> None:
        if not self.sav or self.current_slot is None:
            messagebox.showwarning("No slot selected", "Open a save and select a box slot first.")
            return
        try:
            existing = self.sav.get_box_slot(self.current_box, self.current_slot)
            pkm = self._build_pkm_from_form(existing)
        except (ValueError, tk.TclError) as exc:
            messagebox.showerror("Invalid field value", str(exc))
            return
        self.sav.set_box_slot(self.current_box, self.current_slot, pkm)
        self.refresh_slot_list()
        self._refresh_sprite(pkm.species)
        warning = "" if species.name_for(pkm.species) else "  [!] species not in the Z-A list -- verify it in-game"
        self.status_var.set(
            f"Applied to Box {self.current_box + 1} Slot {self.current_slot + 1} "
            f"(not written to disk yet -- use File > Save){warning}"
        )

    def make_shiny(self) -> None:
        if not self.sav or self.current_slot is None:
            messagebox.showwarning("No slot selected", "Select an occupied slot first.")
            return
        pkm = self.sav.get_box_slot(self.current_box, self.current_slot)
        if pkm.species == 0:
            messagebox.showwarning("Empty slot", "Apply a Pokemon to this slot before making it shiny.")
            return
        tsv = (pkm.tid16 ^ pkm.sid16) >> 4
        while True:
            pid = random.getrandbits(32)
            psv = ((pid >> 16) ^ (pid & 0xFFFF)) >> 4
            if psv == tsv:
                break
        pkm.pid = pid
        self.sav.set_box_slot(self.current_box, self.current_slot, pkm)
        self._load_form_from_pkm(pkm)
        self.status_var.set("Shiny-matching PID applied to this slot (not written to disk yet).")

    def clear_slot(self) -> None:
        if not self.sav or self.current_slot is None:
            return
        self.sav.set_box_slot(self.current_box, self.current_slot, PA9())
        self.refresh_slot_list()
        theme.draw_sprite_placeholder(self.sprite_canvas)
        self.status_var.set(f"Cleared Box {self.current_box + 1} Slot {self.current_slot + 1}")


def main() -> None:
    PokeHexApp().mainloop()


if __name__ == "__main__":
    main()
