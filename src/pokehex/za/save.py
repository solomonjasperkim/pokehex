"""High-level access to a Pokemon Legends: Z-A save file's Pokemon boxes.

Box layout ported from PKHeX.Core/Saves/SAV9ZA.cs and
Saves/Access/SaveBlockAccessor9ZA.cs (https://github.com/kwsch/PKHeX,
GPL-3.0): 32 boxes of 30 slots, each slot occupying SIZE_BOXSLOT (0x198)
bytes within the "Box Data" block, of which the first 0x158 bytes are a
party-format PA9 entry.
"""

from __future__ import annotations

from . import swishcrypto
from .pa9 import SIZE_PARTY, PA9

KEY_BOX = 0x0D66012C
KEY_SAVE_REVISION = 0x0926555A  # 0 = Base, 1 = Mega Dimension, 2 = End of Life

BOX_COUNT = 32
SLOTS_PER_BOX = 30
GAP_BOX_SLOT = 0x40
SIZE_BOXSLOT = SIZE_PARTY + GAP_BOX_SLOT  # 0x198


class SAV9ZA:
    def __init__(self, blocks: list[swishcrypto.SCBlock]) -> None:
        self.blocks = blocks
        self._by_key = {b.key: b for b in blocks}
        if KEY_BOX not in self._by_key:
            raise ValueError("this save file has no Box Data block -- not a valid Legends Z-A save?")

    @classmethod
    def load(cls, path: str) -> "SAV9ZA":
        with open(path, "rb") as f:
            data = f.read()
        if not swishcrypto.get_is_hash_valid(data):
            raise ValueError("save file hash check failed -- file may be corrupt or not a Z-A save")
        return cls(swishcrypto.decrypt(data))

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            f.write(swishcrypto.encrypt(self.blocks))

    def _box_data(self) -> bytearray:
        return self._by_key[KEY_BOX].data

    @property
    def save_revision(self) -> int:
        block = self._by_key.get(KEY_SAVE_REVISION)
        if block is None or len(block.data) < 8:
            return 0
        return int.from_bytes(block.data[:8], "little")

    def _slot_offset(self, box: int, slot: int) -> int:
        if not 0 <= box < BOX_COUNT:
            raise ValueError(f"box {box} out of range 0-{BOX_COUNT - 1}")
        if not 0 <= slot < SLOTS_PER_BOX:
            raise ValueError(f"slot {slot} out of range 0-{SLOTS_PER_BOX - 1}")
        return SIZE_BOXSLOT * (box * SLOTS_PER_BOX + slot)

    def get_box_slot(self, box: int, slot: int) -> PA9:
        offset = self._slot_offset(box, slot)
        raw = self._box_data()[offset:offset + SIZE_PARTY]
        return PA9.from_encrypted(bytes(raw))

    def set_box_slot(self, box: int, slot: int, pkm: PA9) -> None:
        offset = self._slot_offset(box, slot)
        encoded = pkm.to_encrypted_bytes()
        box_data = self._box_data()
        box_data[offset:offset + SIZE_PARTY] = encoded
        # DLC save revisions (Mega Dimension / End of Life) use the gap byte
        # right after the party data as a slot-presence flag; on Base
        # revision saves this byte is unused padding.
        if self.save_revision != 0:
            box_data[offset + SIZE_PARTY] = 1

    def is_slot_empty(self, box: int, slot: int) -> bool:
        offset = self._slot_offset(box, slot)
        return all(b == 0 for b in self._box_data()[offset:offset + SIZE_PARTY])

    def find_empty_slot(self) -> tuple[int, int] | None:
        for box in range(BOX_COUNT):
            for slot in range(SLOTS_PER_BOX):
                if self.is_slot_empty(box, slot):
                    return box, slot
        return None
