"""Retro-handheld-RPG-inspired visual theme for the PokeHex GUI.

Original design: a beveled-box, dialogue-window aesthetic in the general
spirit of classic handheld RPG UIs, built from plain ttk styling (no
trademarked colors, logos, fonts, or character art -- see draw_logo below).
"""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import ttk

BG = "#10141c"
PANEL = "#182030"
PANEL_ALT = "#1d2740"
BORDER = "#324058"
BEVEL_LIGHT = "#46587a"
BEVEL_DARK = "#080a10"
FG = "#eef1f7"
FG_DIM = "#8a97b0"
ACCENT = "#5be0d3"
ACCENT_DIM = "#2f8f86"
WARN = "#f0c14b"
VALID = "#5aa9ff"
INVALID = "#ff6161"

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
    style.configure("Panel.TFrame", background=PANEL, relief="ridge", borderwidth=3)
    style.configure("TLabel", background=BG, foreground=FG, font=FONT_MONO)
    style.configure("Panel.TLabel", background=PANEL, foreground=FG, font=FONT_MONO)
    style.configure("Dim.TLabel", background=BG, foreground=FG_DIM, font=FONT_MONO)
    style.configure("Header.TLabel", background=BG, foreground=ACCENT, font=FONT_MONO_BOLD)

    # Beveled "dialogue box" look: distinct light/dark bevel colors so the
    # groove relief actually reads as a raised console-style box frame.
    style.configure(
        "TLabelframe", background=BG, foreground=ACCENT, bordercolor=BORDER,
        darkcolor=BEVEL_DARK, lightcolor=BEVEL_LIGHT, relief="groove", borderwidth=3,
    )
    style.configure("TLabelframe.Label", background=BG, foreground=ACCENT, font=FONT_MONO_BOLD)

    style.configure(
        "TButton", background=PANEL_ALT, foreground=FG, font=FONT_MONO_BOLD,
        bordercolor=BORDER, darkcolor=BEVEL_DARK, lightcolor=BEVEL_LIGHT,
        focusthickness=1, focuscolor=ACCENT, relief="raised", borderwidth=3, padding=7,
    )
    style.map(
        "TButton",
        background=[("active", ACCENT_DIM), ("pressed", ACCENT_DIM)],
        foreground=[("active", BG)],
        relief=[("pressed", "sunken")],
    )

    style.configure(
        "TEntry", fieldbackground=PANEL_ALT, foreground=FG, insertcolor=ACCENT,
        bordercolor=BORDER, lightcolor=BEVEL_DARK, darkcolor=BEVEL_LIGHT, relief="sunken", borderwidth=2,
    )
    style.configure(
        "TSpinbox", fieldbackground=PANEL_ALT, foreground=FG, insertcolor=ACCENT,
        arrowcolor=ACCENT, bordercolor=BORDER, relief="sunken", borderwidth=2,
    )
    style.configure(
        "TCombobox", fieldbackground=PANEL_ALT, foreground=FG, insertcolor=ACCENT,
        arrowcolor=ACCENT, bordercolor=BORDER, relief="sunken", borderwidth=2,
    )
    style.configure("TSeparator", background=BORDER)

    style.configure("TNotebook", background=BG, bordercolor=BORDER, darkcolor=BEVEL_DARK, lightcolor=BEVEL_LIGHT, borderwidth=3)
    style.configure(
        "TNotebook.Tab", background=PANEL, foreground=FG_DIM, font=FONT_MONO_BOLD,
        padding=(14, 6), bordercolor=BORDER,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", PANEL_ALT)],
        foreground=[("selected", ACCENT)],
        expand=[("selected", (1, 1, 1, 0))],
    )

    # Live field validation: blue = passes the check we actually run, red =
    # fails it. For fields with no ported legality data (ball/item ids),
    # this only confirms "well-formed number" -- not true legality.
    style.configure("Valid.TEntry", fieldbackground=PANEL_ALT, foreground=VALID, insertcolor=VALID, bordercolor=VALID)
    style.configure("Invalid.TEntry", fieldbackground=PANEL_ALT, foreground=INVALID, insertcolor=INVALID, bordercolor=INVALID)


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
    canvas.configure(bg=PANEL_ALT, highlightthickness=2, highlightbackground=BORDER)
    cx = cy = size / 2
    r = size * 0.32
    points: list[float] = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        points.append(cx + r * math.cos(angle))
        points.append(cy + r * math.sin(angle))
    canvas.create_polygon(points, outline=FG_DIM, fill="", width=2)
    canvas.create_text(cx, cy, text="?", fill=FG_DIM, font=("Menlo", 20, "bold"))
