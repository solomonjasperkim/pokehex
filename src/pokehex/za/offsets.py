"""Pokemon Legends: Z-A RAM offsets.

Ported from SysBot.Pokemon/LZA/Vision/PokeDataOffsetsLZA.cs in
https://github.com/kwsch/SysBot.NET (AGPL-3.0). Pointer chains are relative
to the main NSO module base address. These are tied to a specific game
version and will break on game updates until re-derived upstream.
"""

from __future__ import annotations

LZA_GAME_VERSION = "2.0.2"
LEGENDS_ZA_TITLE_ID = "0100F43008C44000"

BOX_START_POKEMON_POINTER = [0x610A710, 0xB0, 0x978, 0x0]
TEXT_SPEED_POINTER = [0x610A710, 0xD8, 0x40]
MY_STATUS_POINTER = [0x610A710, 0xA0, 0x40]
PARTY_POINTER = [0x610A710, 0x18, 0x1B0, 0xF0, 0x50, 0x30, 0x0]
CURRENT_BOX_POINTER = [0x610A710, 0xA8, 0x596]

OVERWORLD_OFFSET = 0x610C858
MENU_OFFSET = 0x612DA80
CONNECTED_OFFSET = 0x6133458

BOX_FORMAT_SLOT_SIZE = 0x148
