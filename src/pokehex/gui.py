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
from typing import Callable

from . import sprites, theme
from .za import abilities as abilities_mod, base_stats, moves as moves_mod, species
from .za import stats as stats_mod
from .za.pa9 import PA9
from .za.save import BOX_COUNT, SLOTS_PER_BOX, SAV9ZA

Validator = Callable[[str], bool]


def _range_check(lo: int, hi: int) -> Validator:
    def check(text: str) -> bool:
        try:
            return lo <= int(text) <= hi
        except ValueError:
            return False
    return check


def _set_check(values: set[int]) -> Validator:
    def check(text: str) -> bool:
        try:
            return int(text) in values
        except ValueError:
            return False
    return check


def _nonneg_check(text: str) -> bool:
    try:
        return int(text) >= 0
    except ValueError:
        return False


def _len_check(n: int) -> Validator:
    def check(text: str) -> bool:
        return len(text) <= n
    return check


# (key, label, is_string, validator). Fields marked "range-only" below have
# no ported legality data (we don't have ball/item tables) -- they only
# confirm "well-formed non-negative number," not true legality. Ability is
# handled separately by AbilityPicker, which does have real per-species data.
IDENTITY_FIELDS: list[tuple[str, str, bool, Validator | None]] = [
    ("form", "Form", False, _nonneg_check),
    ("level", "Level (1-100)", False, _range_check(1, 100)),
    ("nickname", "Nickname (<=12 ch)", True, _len_check(12)),
    ("original_trainer_name", "OT Name (<=12 ch)", True, _len_check(12)),
    ("tid16", "TID (0-65535)", False, _range_check(0, 65535)),
    ("sid16", "SID (0-65535)", False, _range_check(0, 65535)),
    ("nature", "Nature (0-24)", False, _range_check(0, 24)),
    ("gender", "Gender (0=M 1=F 2=N)", False, _set_check({0, 1, 2})),
    ("ball", "Ball id (range-only)", False, _nonneg_check),
    ("held_item", "Held Item id (range-only)", False, _nonneg_check),
]

IV_FIELDS = [("iv_hp", "HP"), ("iv_atk", "Atk"), ("iv_def", "Def"), ("iv_spa", "SpA"), ("iv_spd", "SpD"), ("iv_spe", "Spe")]
EV_FIELDS = [("ev_hp", "HP"), ("ev_atk", "Atk"), ("ev_def", "Def"), ("ev_spa", "SpA"), ("ev_spd", "SpD"), ("ev_spe", "Spe")]
MOVE_KEYS = ["move1", "move2", "move3", "move4"]
STAT_LABELS = [("HP", 0), ("Atk", 1), ("Def", 2), ("SpA", 3), ("SpD", 4), ("Spe", 5)]
EV_MAX_TOTAL = 510

SPECIES_SORT_MODES = [("dex", "Dex #"), ("alpha", "A-Z"), ("fillin", "Fill-in Order")]
MAX_LIST_RESULTS = 300


def _get_int(var: tk.StringVar, default: int = 0) -> int:
    text = var.get().strip()
    return default if not text else int(text)


class SearchableList(ttk.Frame):
    """A search box with an always-visible, live-filtered results list below
    it -- click or arrow-down-then-Enter to pick. Avoids ttk.Combobox's
    popdown, which is slow/fiddly to use on macOS."""

    def __init__(
        self, parent: tk.Widget, options: list[str], width: int = 26,
        list_height: int = 6, on_change: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(parent)
        self.all_options = options
        self.on_change = on_change
        self.var = tk.StringVar()

        self.entry = ttk.Entry(self, textvariable=self.var, width=width, style="Valid.TEntry")
        self.entry.grid(row=0, column=0, sticky="ew")
        self.listbox = tk.Listbox(
            self, height=list_height, width=width, font=theme.FONT_MONO,
            bg=theme.PANEL_ALT, fg=theme.FG, selectbackground=theme.ACCENT_DIM,
            selectforeground=theme.BG, highlightthickness=2, highlightbackground=theme.BORDER,
            relief="sunken", borderwidth=2, exportselection=False,
        )
        self.listbox.grid(row=1, column=0, sticky="ew")

        self._refresh_list(options)
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<Down>", self._move_to_list)
        self.entry.bind("<Return>", self._select_first)
        self.listbox.bind("<<ListboxSelect>>", self._on_listbox_select)
        self.listbox.bind("<Return>", self._on_listbox_select)

    def _refresh_list(self, options: list[str]) -> None:
        self.listbox.delete(0, "end")
        for option in options[:MAX_LIST_RESULTS]:
            self.listbox.insert("end", option)

    def _on_key(self, event: tk.Event) -> None:
        if event.keysym in ("Down", "Up", "Return", "Escape", "Tab"):
            return
        typed = self.var.get().strip().lower()
        filtered = self.all_options if not typed else [o for o in self.all_options if typed in o.lower()]
        self._refresh_list(filtered)

    def _move_to_list(self, _event: tk.Event) -> str:
        if self.listbox.size():
            self.listbox.focus_set()
            self.listbox.selection_clear(0, "end")
            self.listbox.selection_set(0)
            self.listbox.activate(0)
        return "break"

    def _select_first(self, _event: tk.Event) -> None:
        if self.listbox.size() == 1 or (self.listbox.size() and self.var.get().strip()):
            self.var.set(self.listbox.get(0))

    def _on_listbox_select(self, _event: tk.Event) -> None:
        selection = self.listbox.curselection()
        if not selection:
            return
        self.var.set(self.listbox.get(selection[0]))
        if self.on_change is not None:
            self.on_change()

    def set_options(self, options: list[str]) -> None:
        self.all_options = options
        self._refresh_list(options)

    def set_style(self, style_name: str) -> None:
        self.entry.configure(style=style_name)

    def set_value(self, text: str) -> None:
        """Sets the field text and scrolls the view back to the start, so a
        long value (e.g. '025  Pikachu') shows its number prefix instead of
        being scrolled to show the tail end."""
        self.var.set(text)
        self.entry.icursor(0)
        self.entry.xview_moveto(0)


class SpeciesPicker(ttk.Frame):
    """Search + always-visible results list over the ~232 species available
    in Legends Z-A, sortable by Dex #, A-Z, or Z-A's own Lumiose Pokedex
    fill-in order (icon buttons to the right of the search box). Also
    accepts a bare National Dex number typed directly, even outside the
    Z-A list -- there's no legality checker to stop you."""

    def __init__(self, parent: tk.Widget, on_change: Callable[[], None] | None = None) -> None:
        super().__init__(parent)
        self.sort_mode = "dex"
        self._on_change = on_change
        self._sort_buttons: dict[str, ttk.Button] = {}

        search_row = ttk.Frame(self)
        search_row.grid(row=0, column=0, sticky="w")

        self.picker = SearchableList(search_row, species.display_options(self.sort_mode), width=20, list_height=4, on_change=self._on_select)
        self.picker.pack(side="left")
        self.picker.var.trace_add("write", self._revalidate)

        sort_frame = ttk.Frame(search_row)
        sort_frame.pack(side="left", anchor="n", padx=(4, 0))
        for mode, icon in (("dex", "#"), ("alpha", "A-Z"), ("fillin", "✓")):
            btn = ttk.Button(sort_frame, text=icon, width=3, style="Toggle.TButton", command=lambda m=mode: self._set_sort_mode(m))
            btn.pack(side="left", padx=1)
            self._sort_buttons[mode] = btn
        self._update_sort_button_styles()

    def _set_sort_mode(self, mode: str) -> None:
        self.sort_mode = mode
        self.picker.set_options(species.display_options(self.sort_mode))
        self._update_sort_button_styles()

    def _update_sort_button_styles(self) -> None:
        for mode, btn in self._sort_buttons.items():
            btn.configure(style="ToggleOn.TButton" if mode == self.sort_mode else "Toggle.TButton")

    def _on_select(self) -> None:
        if self._on_change is not None:
            self._on_change()

    def _revalidate(self, *_args: object) -> None:
        num = self.get_species_number()
        ok = bool(num) and species.name_for(num) is not None
        self.picker.set_style("Valid.TEntry" if ok else "Invalid.TEntry")

    def get_species_number(self) -> int:
        return species.parse_selection(self.picker.var.get())

    def set_species_number(self, number: int) -> None:
        if not number:
            self.picker.set_value("")
            return
        name = species.name_for(number)
        self.picker.set_value(f"{number:03d}  {name}" if name else f"{number:03d}  (not in Z-A list)")


class MovePicker(ttk.Frame):
    """Search + results list over all real move names. Not filtered to what
    any particular species can actually learn -- we don't have per-species
    movepool data, so this confirms a move is real, not that this Pokemon
    can legally know it."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.picker = SearchableList(self, moves_mod.display_options(), width=16, list_height=4)
        self.picker.pack()
        self.picker.var.trace_add("write", self._revalidate)

    def _revalidate(self, *_args: object) -> None:
        num = self.get_move_id()
        ok = num == 0 or moves_mod.name_for(num) is not None
        self.picker.set_style("Valid.TEntry" if ok else "Invalid.TEntry")

    def get_move_id(self) -> int:
        return moves_mod.parse_selection(self.picker.var.get())

    def set_move_id(self, move_id: int) -> None:
        if not move_id:
            self.picker.set_value("")
            return
        name = moves_mod.name_for(move_id)
        self.picker.set_value(f"{move_id:03d}  {name}" if name else f"{move_id:03d}  (unknown move)")


class AbilityPicker(ttk.Frame):
    """Search + results list, filtered to the abilities the currently
    selected species can actually have (regular slots + hidden). This is the
    one field in PokeHex with real per-species legality checking -- unlike
    ball/item ids, which are range-only."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self._options_by_text: dict[str, tuple[int, int]] = {}
        self.picker = SearchableList(self, [], width=26, list_height=4)
        self.picker.pack()
        self.picker.var.trace_add("write", self._revalidate)

    def refresh_for_species(self, species_number: int) -> None:
        entries = abilities_mod.SPECIES_ABILITIES.get(species_number)
        self._options_by_text = {}
        options: list[str] = []
        if entries:
            for ability_id, slot in sorted(entries, key=lambda t: t[1]):
                name = abilities_mod.ABILITIES.get(ability_id, f"Ability {ability_id}")
                slot_label = "Hidden" if slot == 3 else f"Slot {slot}"
                text = f"{name} ({slot_label})"
                ability_number = 4 if slot == 3 else slot
                options.append(text)
                self._options_by_text[text] = (ability_id, ability_number)
        else:
            for ability_id in sorted(abilities_mod.ABILITIES):
                text = f"{abilities_mod.ABILITIES[ability_id]} (unknown slot)"
                options.append(text)
                self._options_by_text[text] = (ability_id, 0)
        self.picker.set_options(options)
        self._revalidate()

    def _revalidate(self, *_args: object) -> None:
        current = self.picker.var.get()
        ok = (not current) or current in self._options_by_text
        self.picker.set_style("Valid.TEntry" if ok else "Invalid.TEntry")

    def get_selection(self) -> tuple[int, int]:
        return self._options_by_text.get(self.picker.var.get(), (0, 0))

    def set_selection(self, ability_id: int, ability_number: int) -> None:
        if not ability_id:
            self.picker.set_value("")
            return
        for text, (aid, num) in self._options_by_text.items():
            if aid == ability_id and (num == ability_number or ability_number == 0):
                self.picker.set_value(text)
                return
        name = abilities_mod.ABILITIES.get(ability_id, f"Ability id {ability_id}")
        self.picker.set_value(f"{name} (not legal for this species)")


class PokeHexApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PokeHex")
        theme.apply(self)

        self.sav: SAV9ZA | None = None
        self.save_path: str | None = None
        self.current_box = 0
        self.current_slot: int | None = None
        self.fields: dict[str, tk.Variable] = {}
        self.field_widgets: dict[str, ttk.Entry] = {}
        self.move_pickers: list[MovePicker] = []
        self.stat_vars: dict[str, tk.StringVar] = {}
        self._sprite_image = None  # keep a reference so Tk doesn't garbage-collect it

        self._build_menu()
        self._build_header()
        self._build_toolbar()
        self._build_layout()
        self._fit_window()

    # -- window sizing ----------------------------------------------------
    def _fit_window(self) -> None:
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        x = max(0, (self.winfo_screenwidth() - width) // 2)
        y = max(0, (self.winfo_screenheight() - height) // 3)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(width, height)

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

    def _build_toolbar(self) -> None:
        toolbar = ttk.Frame(self, padding=(12, 6))
        toolbar.pack(side="top", fill="x")
        ttk.Button(toolbar, text="Open Save...", command=self.open_save).pack(side="left", padx=(0, 6))
        ttk.Button(toolbar, text="Save", command=self.save_in_place).pack(side="left", padx=6)
        ttk.Button(toolbar, text="Save As...", command=self.save_as).pack(side="left", padx=6)
        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x")

    def _build_layout(self) -> None:
        body = ttk.Frame(self, padding=8)
        body.pack(side="top", fill="both", expand=True)

        left = ttk.Frame(body, style="Panel.TFrame", padding=10)
        left.pack(side="left", fill="y", padx=(0, 8))

        ttk.Label(left, text="BOX (1-32)", style="Panel.TLabel", font=theme.FONT_MONO_BOLD).pack(anchor="w")
        self.box_var = tk.IntVar(value=1)
        ttk.Spinbox(
            left, from_=1, to=BOX_COUNT, textvariable=self.box_var, width=5, command=self.refresh_slot_list,
        ).pack(anchor="w", pady=(2, 8))

        slot_list_frame = ttk.Frame(left)
        slot_list_frame.pack(fill="both", expand=True)
        slot_scrollbar = ttk.Scrollbar(slot_list_frame, orient="vertical")
        self.slot_list = tk.Listbox(
            slot_list_frame, width=28, height=16, font=theme.FONT_MONO,
            bg=theme.PANEL_ALT, fg=theme.FG, selectbackground=theme.ACCENT_DIM,
            selectforeground=theme.BG, highlightthickness=2, highlightbackground=theme.BORDER,
            relief="sunken", borderwidth=2, yscrollcommand=slot_scrollbar.set,
        )
        slot_scrollbar.configure(command=self.slot_list.yview)
        self.slot_list.pack(side="left", fill="both", expand=True)
        slot_scrollbar.pack(side="left", fill="y")
        self.slot_list.bind("<<ListboxSelect>>", self.on_slot_select)

        right = ttk.Frame(body, padding=(4, 0))
        right.pack(side="left", fill="both", expand=True)

        top_row = ttk.Frame(right)
        top_row.pack(side="top", fill="x")

        self.sprite_canvas = tk.Canvas(top_row, width=72, height=72, highlightthickness=0)
        self.sprite_canvas.pack(side="left", anchor="n", padx=(0, 10), pady=(4, 0))
        theme.draw_sprite_placeholder(self.sprite_canvas, size=72)

        identity_frame = ttk.Labelframe(top_row, text="IDENTITY", padding=6)
        identity_frame.pack(side="left", fill="both", expand=True)

        ttk.Label(identity_frame, text="Species").grid(row=0, column=0, sticky="nw", padx=(0, 4), pady=1)
        self.species_picker = SpeciesPicker(identity_frame, on_change=self._on_species_changed)
        self.species_picker.grid(row=0, column=1, columnspan=3, sticky="w", padx=(0, 12), pady=1)

        ttk.Label(identity_frame, text="Ability").grid(row=0, column=4, sticky="nw", padx=(0, 4), pady=1)
        self.ability_picker = AbilityPicker(identity_frame)
        self.ability_picker.grid(row=0, column=5, sticky="w", pady=1)
        self.ability_picker.refresh_for_species(0)

        self._build_field_grid(identity_frame, IDENTITY_FIELDS, start_row=1, columns=3)

        mid_row = ttk.Frame(right)
        mid_row.pack(side="top", fill="x", pady=6)

        iv_frame = ttk.Labelframe(mid_row, text="IVs (0-31)", padding=6)
        iv_frame.pack(side="left", fill="both", expand=True, padx=(0, 4))
        self._build_stat_row(iv_frame, IV_FIELDS, _range_check(0, 31))

        ev_frame = ttk.Labelframe(mid_row, text="EVs (0-252 each)", padding=6)
        ev_frame.pack(side="left", fill="both", expand=True, padx=4)
        self._build_stat_row(ev_frame, EV_FIELDS, _range_check(0, 252))
        self.ev_total_var = tk.StringVar(value=f"Total: 0/{EV_MAX_TOTAL}")
        self.ev_total_label = ttk.Label(ev_frame, textvariable=self.ev_total_var)
        self.ev_total_label.grid(row=2, column=0, columnspan=len(EV_FIELDS), sticky="w", pady=(2, 0))

        stats_frame = ttk.Labelframe(mid_row, text="STATS (live)", padding=6)
        stats_frame.pack(side="left", fill="both", expand=True, padx=(4, 0))
        for col, (label, _idx) in enumerate(STAT_LABELS):
            r, c = divmod(col, 3)
            ttk.Label(stats_frame, text=label).grid(row=r * 2, column=c, padx=6)
            var = tk.StringVar(value="--")
            self.stat_vars[label] = var
            ttk.Label(stats_frame, textvariable=var, style="Header.TLabel").grid(row=r * 2 + 1, column=c, padx=6)

        for key, _ in IV_FIELDS + EV_FIELDS:
            self.fields[key].trace_add("write", self._on_stat_input_changed)

        move_frame = ttk.Labelframe(right, text="MOVES (real move names -- not filtered to this species' learnset)", padding=6)
        move_frame.pack(side="top", fill="x", pady=(0, 6))
        for i, key in enumerate(MOVE_KEYS):
            ttk.Label(move_frame, text=f"Move {i + 1}").grid(row=0, column=i, padx=6)
            picker = MovePicker(move_frame)
            picker.grid(row=1, column=i, padx=6)
            self.move_pickers.append(picker)

        btn_frame = ttk.Frame(right)
        btn_frame.pack(side="top", fill="x", pady=4)
        ttk.Button(btn_frame, text="Fill Smart Defaults", command=self.fill_smart_defaults).pack(side="left", padx=(0, 6))
        ttk.Button(btn_frame, text="Apply to Slot", command=self.apply_to_slot).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Make Shiny", command=self.make_shiny).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="Clear Slot", command=self.clear_slot).pack(side="left", padx=6)

        legend = ttk.Label(
            right,
            text="Blue = passes the check we run, red = fails it. Ability is checked for real; ball/item ids "
                 "and moves are range/existence checks only -- not full legality.",
            style="Dim.TLabel", wraplength=640, justify="left",
        )
        legend.pack(side="top", fill="x", pady=(0, 2))

        self.status_var = tk.StringVar(value="Open a save file to begin.")
        status_bar = tk.Label(
            self, textvariable=self.status_var, anchor="w", bg=theme.PANEL, fg=theme.FG_DIM,
            font=theme.FONT_MONO, padx=8, pady=4,
        )
        status_bar.pack(side="bottom", fill="x")

    def _make_entry(self, parent: ttk.Frame, key: str, var: tk.Variable, validator: Validator | None, width: int) -> ttk.Entry:
        entry = ttk.Entry(parent, textvariable=var, width=width, style="Valid.TEntry")
        self.field_widgets[key] = entry
        if validator is not None:
            def on_change(*_args: object, _var=var, _entry=entry, _check=validator) -> None:
                _entry.configure(style="Valid.TEntry" if _check(_var.get()) else "Invalid.TEntry")
            var.trace_add("write", on_change)
            on_change()
        return entry

    def _build_field_grid(
        self, parent: ttk.Frame, specs: list[tuple[str, str, bool, Validator | None]],
        start_row: int = 0, columns: int = 2,
    ) -> None:
        for i, (key, label, is_str, validator) in enumerate(specs):
            row, col = divmod(i, columns)
            row += start_row
            ttk.Label(parent, text=label).grid(row=row, column=col * 2, sticky="w", padx=(0, 3), pady=1)
            var: tk.Variable = tk.StringVar(value="") if is_str else tk.StringVar(value="0")
            self.fields[key] = var
            self._make_entry(parent, key, var, validator, width=10).grid(
                row=row, column=col * 2 + 1, sticky="w", padx=(0, 10), pady=1,
            )
            if key in ("level", "nature"):
                var.trace_add("write", self._on_stat_input_changed)

    def _build_stat_row(self, parent: ttk.Frame, specs: list[tuple[str, str]], validator: Validator) -> None:
        for i, (key, label) in enumerate(specs):
            ttk.Label(parent, text=label).grid(row=0, column=i, padx=4)
            var = tk.StringVar(value="0")
            self.fields[key] = var
            self._make_entry(parent, key, var, validator, width=5).grid(row=1, column=i, padx=4)

    def _on_species_changed(self) -> None:
        species_number = self.species_picker.get_species_number()
        self.ability_picker.refresh_for_species(species_number)
        self._recompute_stats()
        self._refresh_sprite(species_number)

    def _on_stat_input_changed(self, *_args: object) -> None:
        self._update_ev_total()
        self._recompute_stats()

    def _update_ev_total(self, *_args: object) -> None:
        total = 0
        for key, _ in EV_FIELDS:
            try:
                total += _get_int(self.fields[key])  # type: ignore[arg-type]
            except ValueError:
                pass
        self.ev_total_var.set(f"Total: {total}/{EV_MAX_TOTAL}")
        self.ev_total_label.configure(foreground=theme.VALID if total <= EV_MAX_TOTAL else theme.INVALID)

    def _current_computed_stats(self) -> tuple[int, int, int, int, int, int] | None:
        base = base_stats.BASE_STATS.get(self.species_picker.get_species_number())
        if base is None:
            return None
        try:
            ivs = tuple(_get_int(self.fields[k]) for k, _ in IV_FIELDS)  # type: ignore[arg-type]
            evs = tuple(_get_int(self.fields[k]) for k, _ in EV_FIELDS)  # type: ignore[arg-type]
            level = max(1, min(100, _get_int(self.fields["level"])))  # type: ignore[arg-type]
            nature = _get_int(self.fields["nature"])  # type: ignore[arg-type]
        except ValueError:
            return None
        return stats_mod.compute_stats(base, ivs, evs, level, nature)  # type: ignore[arg-type]

    def _recompute_stats(self) -> None:
        computed = self._current_computed_stats()
        if computed is None:
            for label, _ in STAT_LABELS:
                self.stat_vars[label].set("--")
            return
        for label, idx in STAT_LABELS:
            self.stat_vars[label].set(str(computed[idx]))

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

    def _refresh_sprite(self, species_number: int) -> None:
        image = sprites.load_sprite(species_number, size=96) if species_number else None
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
        self.ability_picker.refresh_for_species(pkm.species)
        self.ability_picker.set_selection(pkm.ability, pkm.ability_number)
        self.fields["form"].set(str(pkm.form))
        self.fields["level"].set(str(pkm.stat_level))
        self.fields["nickname"].set(pkm.nickname)
        self.fields["original_trainer_name"].set(pkm.original_trainer_name)
        self.fields["tid16"].set(str(pkm.tid16))
        self.fields["sid16"].set(str(pkm.sid16))
        self.fields["nature"].set(str(pkm.nature))
        self.fields["gender"].set(str(pkm.gender))
        self.fields["ball"].set(str(pkm.ball))
        self.fields["held_item"].set(str(pkm.held_item))
        self.fields["iv_hp"].set(str(pkm.iv_hp))
        self.fields["iv_atk"].set(str(pkm.iv_atk))
        self.fields["iv_def"].set(str(pkm.iv_def))
        self.fields["iv_spa"].set(str(pkm.iv_spa))
        self.fields["iv_spd"].set(str(pkm.iv_spd))
        self.fields["iv_spe"].set(str(pkm.iv_spe))
        self.fields["ev_hp"].set(str(pkm.ev_hp))
        self.fields["ev_atk"].set(str(pkm.ev_atk))
        self.fields["ev_def"].set(str(pkm.ev_def))
        self.fields["ev_spa"].set(str(pkm.ev_spa))
        self.fields["ev_spd"].set(str(pkm.ev_spd))
        self.fields["ev_spe"].set(str(pkm.ev_spe))
        for i, picker in enumerate(self.move_pickers):
            picker.set_move_id(pkm.move(i))
        self._recompute_stats()

    def fill_smart_defaults(self) -> None:
        """Fills the form with sensible, legally-shaped values you can then
        customize -- doesn't touch species/ability/moves, so you still choose those."""
        self.fields["form"].set("0")
        self.fields["level"].set("50")
        self.fields["nature"].set("0")
        self.fields["gender"].set("0")
        self.fields["ball"].set("4")  # Poke Ball
        self.fields["held_item"].set("0")
        for key, _ in IV_FIELDS:
            self.fields[key].set("31")
        for key, _ in EV_FIELDS:
            self.fields[key].set("0")
        self.status_var.set("Smart defaults filled in -- pick a species, ability, and moves, then customize as needed.")

    def _build_pkm_from_form(self, pkm: PA9) -> PA9:
        if pkm.pid == 0:
            pkm.pid = random.getrandbits(32)
        if pkm.encryption_constant == 0:
            pkm.encryption_constant = random.getrandbits(32)

        pkm.species = self.species_picker.get_species_number()
        ability_id, ability_number = self.ability_picker.get_selection()
        pkm.ability = ability_id
        pkm.ability_number = ability_number
        pkm.form = _get_int(self.fields["form"])  # type: ignore[arg-type]
        level = max(1, min(100, _get_int(self.fields["level"])))  # type: ignore[arg-type]
        pkm.stat_level = level
        pkm.met_level = level
        pkm.nickname = self.fields["nickname"].get()
        pkm.original_trainer_name = self.fields["original_trainer_name"].get()
        pkm.tid16 = _get_int(self.fields["tid16"])  # type: ignore[arg-type]
        pkm.sid16 = _get_int(self.fields["sid16"])  # type: ignore[arg-type]
        pkm.nature = _get_int(self.fields["nature"])  # type: ignore[arg-type]
        pkm.gender = _get_int(self.fields["gender"])  # type: ignore[arg-type]
        pkm.ball = _get_int(self.fields["ball"])  # type: ignore[arg-type]
        pkm.held_item = _get_int(self.fields["held_item"])  # type: ignore[arg-type]
        pkm.iv_hp = _get_int(self.fields["iv_hp"])  # type: ignore[arg-type]
        pkm.iv_atk = _get_int(self.fields["iv_atk"])  # type: ignore[arg-type]
        pkm.iv_def = _get_int(self.fields["iv_def"])  # type: ignore[arg-type]
        pkm.iv_spa = _get_int(self.fields["iv_spa"])  # type: ignore[arg-type]
        pkm.iv_spd = _get_int(self.fields["iv_spd"])  # type: ignore[arg-type]
        pkm.iv_spe = _get_int(self.fields["iv_spe"])  # type: ignore[arg-type]
        pkm.ev_hp = _get_int(self.fields["ev_hp"])  # type: ignore[arg-type]
        pkm.ev_atk = _get_int(self.fields["ev_atk"])  # type: ignore[arg-type]
        pkm.ev_def = _get_int(self.fields["ev_def"])  # type: ignore[arg-type]
        pkm.ev_spa = _get_int(self.fields["ev_spa"])  # type: ignore[arg-type]
        pkm.ev_spd = _get_int(self.fields["ev_spd"])  # type: ignore[arg-type]
        pkm.ev_spe = _get_int(self.fields["ev_spe"])  # type: ignore[arg-type]
        for i, picker in enumerate(self.move_pickers):
            pkm.set_move(i, picker.get_move_id())
        for i in range(4):
            if pkm.move(i) != 0 and pkm.move_pp(i) == 0:
                pkm.set_move_pp(i, 1)

        computed = self._current_computed_stats()
        if computed is not None:
            hp, atk, defense, spa, spd, spe = computed
            pkm.stat_hp_max = hp
            pkm.stat_atk = atk
            pkm.stat_def = defense
            pkm.stat_spa = spa
            pkm.stat_spd = spd
            pkm.stat_spe = spe
            pkm.stat_hp_current = hp  # full heal
        else:
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
        ev_total = pkm.ev_hp + pkm.ev_atk + pkm.ev_def + pkm.ev_spa + pkm.ev_spd + pkm.ev_spe
        warnings = []
        if not species.name_for(pkm.species):
            warnings.append("species not in the Z-A list")
        if ev_total > EV_MAX_TOTAL:
            warnings.append(f"EV total {ev_total} exceeds {EV_MAX_TOTAL}")
        if pkm.species not in base_stats.BASE_STATS:
            warnings.append("no base stats for this species -- battle stats left unchanged")
        self.sav.set_box_slot(self.current_box, self.current_slot, pkm)
        self.refresh_slot_list()
        self._refresh_sprite(pkm.species)
        suffix = f"  [!] {'; '.join(warnings)}" if warnings else ""
        self.status_var.set(
            f"Applied to Box {self.current_box + 1} Slot {self.current_slot + 1} "
            f"(not written to disk yet -- use File > Save){suffix}"
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
