"""Retro-terminal visual theme for the PokeHex GUI. Original design -- no
trademarked colors, marks, or character likenesses."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

BG = "#0d1117"
PANEL = "#161b22"
PANEL_ALT = "#1c2430"
BORDER = "#2c3644"
FG = "#e8dcc8"
FG_DIM = "#8a97a6"
ACCENT = "#4fd1c5"
ACCENT_DIM = "#2f8f86"
WARN = "#e3b23c"
VALID = "#4da6ff"
INVALID = "#ff5c5c"

FONT_MONO = ("Menlo", 11)
FONT_MONO_BOLD = ("Menlo", 11, "bold")
FONT_LOGO_TITLE = ("Menlo", 22, "bold")
FONT_LOGO_SUB = ("Menlo", 10)


def apply(root: tk.Tk) -> None:
    root.configure(bg=BG)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", background=BG, foreground=FG, font=FONT_MONO)
    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=PANEL)
    style.configure("TLabel", background=BG, foreground=FG, font=FONT_MONO)
    style.configure("Panel.TLabel", background=PANEL, foreground=FG, font=FONT_MONO)
    style.configure("Dim.TLabel", background=BG, foreground=FG_DIM, font=FONT_MONO)
    style.configure("Header.TLabel", background=BG, foreground=ACCENT, font=FONT_MONO_BOLD)

    style.configure(
        "TLabelframe", background=BG, foreground=ACCENT, bordercolor=BORDER,
        darkcolor=BORDER, lightcolor=BORDER, relief="groove",
    )
    style.configure("TLabelframe.Label", background=BG, foreground=ACCENT, font=FONT_MONO_BOLD)

    style.configure(
        "TButton", background=PANEL_ALT, foreground=FG, font=FONT_MONO_BOLD,
        bordercolor=ACCENT_DIM, focusthickness=1, focuscolor=ACCENT, relief="flat", padding=6,
    )
    style.map(
        "TButton",
        background=[("active", ACCENT_DIM), ("pressed", ACCENT_DIM)],
        foreground=[("active", BG)],
    )

    style.configure(
        "TEntry", fieldbackground=PANEL_ALT, foreground=FG, insertcolor=ACCENT,
        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
    )
    style.configure(
        "TSpinbox", fieldbackground=PANEL_ALT, foreground=FG, insertcolor=ACCENT,
        arrowcolor=ACCENT, bordercolor=BORDER,
    )

    # Live field validation: blue = passes the check we actually run, red =
    # fails it. For fields with no ported legality data (ability/ball/item/
    # move ids), this only confirms "well-formed number" -- not true legality.
    style.configure("Valid.TEntry", fieldbackground=PANEL_ALT, foreground=VALID, insertcolor=VALID, bordercolor=VALID)
    style.configure("Invalid.TEntry", fieldbackground=PANEL_ALT, foreground=INVALID, insertcolor=INVALID, bordercolor=INVALID)
    style.configure("Valid.TCombobox", fieldbackground=PANEL_ALT, foreground=VALID, arrowcolor=VALID, bordercolor=VALID)
    style.configure("Invalid.TCombobox", fieldbackground=PANEL_ALT, foreground=INVALID, arrowcolor=INVALID, bordercolor=INVALID)
    style.map("Valid.TCombobox", fieldbackground=[("readonly", PANEL_ALT)], foreground=[("readonly", VALID)])
    style.map("Invalid.TCombobox", fieldbackground=[("readonly", PANEL_ALT)], foreground=[("readonly", INVALID)])


def draw_logo(canvas: tk.Canvas) -> None:
    """Original PokeHex mark: a hexagon outline (nod to 'hex' editing) with
    a wordmark. No Poke Ball imagery, no character art, no trademarked font."""
    canvas.delete("all")
    canvas.configure(bg=BG, highlightthickness=0)

    cx, cy, r = 34, 32, 24
    points: list[float] = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        points.append(cx + r * math.cos(angle))
        points.append(cy + r * math.sin(angle))
    canvas.create_polygon(points, outline=ACCENT, fill="", width=2)

    inner: list[float] = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        inner.append(cx + (r - 8) * math.cos(angle))
        inner.append(cy + (r - 8) * math.sin(angle))
    canvas.create_polygon(inner, outline=ACCENT_DIM, fill="", width=1)

    canvas.create_text(cx, cy, text="0x", fill=ACCENT, font=("Menlo", 13, "bold"))

    canvas.create_text(76, cy - 8, text="POKE", fill=FG, font=FONT_LOGO_TITLE, anchor="w")
    canvas.create_text(158, cy - 8, text="HEX", fill=ACCENT, font=FONT_LOGO_TITLE, anchor="w")
    canvas.create_text(78, cy + 16, text="LEGENDS: Z-A SAVE EDITOR", fill=FG_DIM, font=FONT_LOGO_SUB, anchor="w")


def draw_sprite_placeholder(canvas: tk.Canvas, size: int = 96) -> None:
    """Original placeholder icon shown when no user-supplied sprite is found."""
    canvas.delete("all")
    canvas.configure(bg=PANEL_ALT, highlightthickness=1, highlightbackground=BORDER)
    cx = cy = size / 2
    r = size * 0.32
    points: list[float] = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        points.append(cx + r * math.cos(angle))
        points.append(cy + r * math.sin(angle))
    canvas.create_polygon(points, outline=FG_DIM, fill="", width=2)
    canvas.create_text(cx, cy, text="?", fill=FG_DIM, font=("Menlo", 20, "bold"))
