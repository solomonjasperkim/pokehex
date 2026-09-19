"""Poke Ball names, keyed by item id.

Name/id reference data (game mechanics), sourced from PokeAPI's public
CSV dataset (https://github.com/PokeAPI/pokeapi, BSD-3-Clause) -- not artwork.

Known gap: several ball names have MULTIPLE different real item ids across
game generations (e.g. mainline games vs. Legends Arceus used different id
ranges for the same ball). Z-A is also a Legends-subtitled game and we do not
know which numbering it actually uses -- all historical candidates are kept
here rather than guessing one. Verify in-game which id is actually correct.
"""

from __future__ import annotations

BALLS: dict[int, str] = {
    1: "Master Ball",
    2: "Ultra Ball",
    3: "Great Ball",
    4: "Poké Ball",
    5: "Safari Ball",
    6: "Net Ball",
    7: "Dive Ball",
    8: "Nest Ball",
    9: "Repeat Ball",
    10: "Timer Ball",
    11: "Luxury Ball",
    12: "Premier Ball",
    13: "Dusk Ball",
    14: "Heal Ball",
    15: "Quick Ball",
    16: "Cherish Ball",
    449: "Lure Ball",
    450: "Level Ball",
    451: "Moon Ball",
    452: "Heavy Ball",
    453: "Fast Ball",
    454: "Friend Ball",
    455: "Love Ball",
    456: "Park Ball",
    457: "Sport Ball",
    617: "Dream Ball",
    887: "Beast Ball",
    2219: "Strange Ball",
    2220: "Poké Ball",
    2221: "Great Ball",
    2222: "Ultra Ball",
    2223: "Heavy Ball",
    2224: "Leaden Ball",
    2225: "Gigaton Ball",
    2226: "Feather Ball",
    2227: "Wing Ball",
    2228: "Jet Ball",
    2229: "Origin Ball",
}


def display_options() -> list[str]:
    return [f"{iid:04d}  {name}" for iid, name in sorted(BALLS.items())]


def name_for(item_id: int) -> str | None:
    return BALLS.get(item_id)


def parse_selection(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    head = text.split(None, 1)[0]
    if head.isdigit():
        return int(head)
    lowered = text.lower()
    for iid, name in BALLS.items():
        if name.lower() == lowered:
            return iid
    return 0
