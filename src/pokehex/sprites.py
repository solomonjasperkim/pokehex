"""Optional sprite loading.

PokeHex ships no Pokemon artwork -- it's copyrighted. If you drop your own
legally-obtained sprite images into the `sprites/` folder at the project
root, named by national dex number (e.g. `sprites/6.png` for species #6),
the GUI will display them. Without that folder populated, an original
placeholder icon is drawn instead.
"""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image, ImageTk
    _PIL_AVAILABLE = True
except ImportError:
    _PIL_AVAILABLE = False

SPRITE_DIR = Path(__file__).resolve().parent.parent.parent / "sprites"
_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif")


def find_sprite_path(species: int) -> Path | None:
    if not SPRITE_DIR.is_dir():
        return None
    for ext in _EXTENSIONS:
        candidate = SPRITE_DIR / f"{species}{ext}"
        if candidate.is_file():
            return candidate
    return None


def load_sprite(species: int, size: int = 96):
    """Returns a Tk-compatible image for the given species, or None if
    unavailable (no Pillow, or no matching file in sprites/)."""
    if not _PIL_AVAILABLE:
        return None
    path = find_sprite_path(species)
    if path is None:
        return None
    try:
        img = Image.open(path).convert("RGBA")
        img.thumbnail((size, size), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None
