"""The standard Pokemon stat formula (stable since Generation 3, still used
today) plus the 25-nature boost/hindrance table. Game-mechanics reference
data, not copyrighted expression.

Stat order used throughout: (hp, atk, def, spa, spd, spe).
"""

from __future__ import annotations

# nature id -> (boosted_stat_index, lowered_stat_index), using 1=atk 2=def
# 3=spa 4=spd 5=spe (0/hp is never affected by nature); None means neutral.
NATURE_MODIFIERS: dict[int, tuple[int | None, int | None]] = {
    0: (None, None),   # Hardy
    1: (1, 2),          # Lonely: +Atk -Def
    2: (1, 5),          # Brave: +Atk -Spe
    3: (1, 3),          # Adamant: +Atk -SpA
    4: (1, 4),          # Naughty: +Atk -SpD
    5: (2, 1),           # Bold: +Def -Atk
    6: (None, None),   # Docile
    7: (2, 5),           # Relaxed: +Def -Spe
    8: (2, 3),           # Impish: +Def -SpA
    9: (2, 4),           # Lax: +Def -SpD
    10: (5, 1),          # Timid: +Spe -Atk
    11: (5, 2),          # Hasty: +Spe -Def
    12: (None, None),  # Serious
    13: (5, 3),          # Jolly: +Spe -SpA
    14: (5, 4),          # Naive: +Spe -SpD
    15: (3, 1),          # Modest: +SpA -Atk
    16: (3, 2),          # Mild: +SpA -Def
    17: (3, 5),          # Quiet: +SpA -Spe
    18: (None, None),  # Bashful
    19: (3, 4),          # Rash: +SpA -SpD
    20: (4, 1),          # Calm: +SpD -Atk
    21: (4, 2),          # Gentle: +SpD -Def
    22: (4, 5),          # Sassy: +SpD -Spe
    23: (4, 3),          # Careful: +SpD -SpA
    24: (None, None),  # Quirky
}

NATURE_NAMES: dict[int, str] = {
    0: "Hardy", 1: "Lonely", 2: "Brave", 3: "Adamant", 4: "Naughty",
    5: "Bold", 6: "Docile", 7: "Relaxed", 8: "Impish", 9: "Lax",
    10: "Timid", 11: "Hasty", 12: "Serious", 13: "Jolly", 14: "Naive",
    15: "Modest", 16: "Mild", 17: "Quiet", 18: "Bashful", 19: "Rash",
    20: "Calm", 21: "Gentle", 22: "Sassy", 23: "Careful", 24: "Quirky",
}


def _nature_multiplier(nature: int, stat_index: int) -> float:
    boosted, lowered = NATURE_MODIFIERS.get(nature, (None, None))
    if stat_index == boosted:
        return 1.1
    if stat_index == lowered:
        return 0.9
    return 1.0


def compute_stats(
    base: tuple[int, int, int, int, int, int],
    ivs: tuple[int, int, int, int, int, int],
    evs: tuple[int, int, int, int, int, int],
    level: int,
    nature: int,
) -> tuple[int, int, int, int, int, int]:
    """Returns (hp, atk, def, spa, spd, spe) using the standard formula."""
    hp_base, hp_iv, hp_ev = base[0], ivs[0], evs[0]
    hp = ((2 * hp_base + hp_iv + hp_ev // 4) * level) // 100 + level + 10

    out = [hp]
    for i in range(1, 6):
        core = ((2 * base[i] + ivs[i] + evs[i] // 4) * level) // 100 + 5
        out.append(int(core * _nature_multiplier(nature, i)))
    return tuple(out)  # type: ignore[return-value]
