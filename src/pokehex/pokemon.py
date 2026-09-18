"""Game-agnostic in-memory representation of a single Pokemon.

This is deliberately independent of any one game's on-disk/in-memory binary
format. Encoding/decoding to a specific game's format (e.g. Legends Z-A)
belongs in a separate module once that format is known.
"""

from __future__ import annotations

from dataclasses import dataclass, field

STATS = ("hp", "atk", "def", "spa", "spd", "spe")


@dataclass
class StatBlock:
    hp: int = 0
    atk: int = 0
    def_: int = 0
    spa: int = 0
    spd: int = 0
    spe: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "hp": self.hp,
            "atk": self.atk,
            "def": self.def_,
            "spa": self.spa,
            "spd": self.spd,
            "spe": self.spe,
        }


@dataclass
class IVs(StatBlock):
    def __post_init__(self) -> None:
        for stat, value in self.as_dict().items():
            if not 0 <= value <= 31:
                raise ValueError(f"IV {stat}={value} out of range 0-31")


@dataclass
class EVs(StatBlock):
    def __post_init__(self) -> None:
        total = sum(self.as_dict().values())
        for stat, value in self.as_dict().items():
            if not 0 <= value <= 252:
                raise ValueError(f"EV {stat}={value} out of range 0-252")
        if total > 510:
            raise ValueError(f"EV total {total} exceeds max of 510")


@dataclass
class Move:
    id: int
    pp_ups: int = 0


@dataclass
class Pokemon:
    species: int
    level: int = 1
    nickname: str = ""
    nature: int = 0
    ability: int = 0
    gender: int = 0  # 0=male, 1=female, 2=genderless
    is_shiny: bool = False
    pid: int = 0
    experience: int = 0
    friendship: int = 0
    held_item: int = 0
    ball: int = 4  # Poke Ball
    forme: int = 0
    language: int = 2  # English
    ot_name: str = ""
    ot_id: int = 0
    ot_secret_id: int = 0
    met_location: int = 0
    met_level: int = 1
    ivs: IVs = field(default_factory=IVs)
    evs: EVs = field(default_factory=EVs)
    moves: list[Move] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 1 <= self.level <= 100:
            raise ValueError(f"level {self.level} out of range 1-100")
        if len(self.moves) > 4:
            raise ValueError("a Pokemon cannot know more than 4 moves")
