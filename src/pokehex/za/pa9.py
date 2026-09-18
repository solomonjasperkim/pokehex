"""PA9: the Pokemon entity format used by Pokemon Legends: Z-A.

Field offsets ported from PKHeX.Core/PKM/PA9.cs (https://github.com/kwsch/PKHeX,
GPL-3.0). This covers the fields needed to build a functional Pokemon
(species/level/stats/moves/OT/IVs/EVs/met info) but intentionally omits
ribbons, marks, and TM record flags, which are cosmetic/optional and left
zeroed.

Known gap: `species_internal` is currently treated as equal to the national
dex number. PKHeX maintains a separate internal<->national species mapping
table for this game that has not been ported here -- for species affected by
that reordering, the written species will be wrong. Verify against a real
save before trusting species IDs outside of commonly-tested ones.
"""

from __future__ import annotations

from . import crypto

SIZE_STORED = crypto.SIZE_STORED  # 0x148
SIZE_PARTY = crypto.SIZE_PARTY  # 0x158


def _u16(data: bytes, offset: int) -> int:
    return data[offset] | (data[offset + 1] << 8)


def _set_u16(data: bytearray, offset: int, value: int) -> None:
    value &= 0xFFFF
    data[offset] = value & 0xFF
    data[offset + 1] = value >> 8


def _u32(data: bytes, offset: int) -> int:
    return data[offset] | (data[offset + 1] << 8) | (data[offset + 2] << 16) | (data[offset + 3] << 24)


def _set_u32(data: bytearray, offset: int, value: int) -> None:
    value &= 0xFFFFFFFF
    data[offset] = value & 0xFF
    data[offset + 1] = (value >> 8) & 0xFF
    data[offset + 2] = (value >> 16) & 0xFF
    data[offset + 3] = (value >> 24) & 0xFF


def _u64(data: bytes, offset: int) -> int:
    value = 0
    for i in range(8):
        value |= data[offset + i] << (8 * i)
    return value


def _set_u64(data: bytearray, offset: int, value: int) -> None:
    value &= 0xFFFFFFFFFFFFFFFF
    for i in range(8):
        data[offset + i] = (value >> (8 * i)) & 0xFF


def _get_string(data: bytes) -> str:
    raw = bytes(data)
    text = raw.decode("utf-16-le", errors="ignore")
    return text.split("\0", 1)[0]


def _set_string(data: bytearray, value: str, max_chars: int) -> None:
    value = value[:max_chars]
    encoded = value.encode("utf-16-le")
    for i in range(len(data)):
        data[i] = 0
    data[: len(encoded)] = encoded


class PA9:
    """Wraps a 0x158-byte (party format) PA9 buffer with field accessors."""

    def __init__(self, data: bytes | bytearray | None = None) -> None:
        if data is None:
            self.data = bytearray(SIZE_PARTY)
        else:
            buf = bytearray(data)
            if len(buf) not in (SIZE_STORED, SIZE_PARTY):
                raise ValueError(f"expected {SIZE_STORED} or {SIZE_PARTY} bytes, got {len(buf)}")
            if len(buf) == SIZE_STORED:
                buf.extend(bytes(SIZE_PARTY - SIZE_STORED))
            self.data = buf

    # -- crypto -----------------------------------------------------------
    @classmethod
    def from_encrypted(cls, data: bytes) -> "PA9":
        buf = bytearray(data)
        crypto.decrypt_if_encrypted8(buf)
        return cls(buf)

    def to_encrypted_bytes(self) -> bytes:
        self.refresh_checksum()
        buf = bytearray(self.data)
        crypto.encrypt8(buf)
        return bytes(buf)

    def calculate_checksum(self) -> int:
        total = 0
        for i in range(8, SIZE_STORED, 2):
            total = (total + _u16(self.data, i)) & 0xFFFF
        return total

    def refresh_checksum(self) -> None:
        self.checksum = self.calculate_checksum()

    @property
    def checksum_valid(self) -> bool:
        return self.calculate_checksum() == self.checksum

    # -- Header -------------------------------------------------------------
    @property
    def encryption_constant(self) -> int:
        return _u32(self.data, 0x00)

    @encryption_constant.setter
    def encryption_constant(self, value: int) -> None:
        _set_u32(self.data, 0x00, value)

    @property
    def sanity(self) -> int:
        return _u16(self.data, 0x04)

    @sanity.setter
    def sanity(self, value: int) -> None:
        _set_u16(self.data, 0x04, value)

    @property
    def checksum(self) -> int:
        return _u16(self.data, 0x06)

    @checksum.setter
    def checksum(self, value: int) -> None:
        _set_u16(self.data, 0x06, value)

    # -- Block A --------------------------------------------------------
    @property
    def species(self) -> int:
        return _u16(self.data, 0x08)

    @species.setter
    def species(self, value: int) -> None:
        _set_u16(self.data, 0x08, value)

    @property
    def held_item(self) -> int:
        return _u16(self.data, 0x0A)

    @held_item.setter
    def held_item(self, value: int) -> None:
        _set_u16(self.data, 0x0A, value)

    @property
    def tid16(self) -> int:
        return _u16(self.data, 0x0C)

    @tid16.setter
    def tid16(self, value: int) -> None:
        _set_u16(self.data, 0x0C, value)

    @property
    def sid16(self) -> int:
        return _u16(self.data, 0x0E)

    @sid16.setter
    def sid16(self, value: int) -> None:
        _set_u16(self.data, 0x0E, value)

    @property
    def exp(self) -> int:
        return _u32(self.data, 0x10)

    @exp.setter
    def exp(self, value: int) -> None:
        _set_u32(self.data, 0x10, value)

    @property
    def ability(self) -> int:
        return _u16(self.data, 0x14)

    @ability.setter
    def ability(self, value: int) -> None:
        _set_u16(self.data, 0x14, value)

    @property
    def ability_number(self) -> int:
        return self.data[0x16] & 7

    @ability_number.setter
    def ability_number(self, value: int) -> None:
        self.data[0x16] = (self.data[0x16] & ~7) | (value & 7)

    @property
    def pid(self) -> int:
        return _u32(self.data, 0x1C)

    @pid.setter
    def pid(self, value: int) -> None:
        _set_u32(self.data, 0x1C, value)

    @property
    def nature(self) -> int:
        return self.data[0x20]

    @nature.setter
    def nature(self, value: int) -> None:
        self.data[0x20] = value & 0xFF

    @property
    def gender(self) -> int:
        return (self.data[0x22] >> 1) & 0x3

    @gender.setter
    def gender(self, value: int) -> None:
        self.data[0x22] = (self.data[0x22] & 0xF9) | ((value & 0x3) << 1)

    @property
    def form(self) -> int:
        return self.data[0x24]

    @form.setter
    def form(self, value: int) -> None:
        _set_u16(self.data, 0x24, value)

    @property
    def ev_hp(self) -> int:
        return self.data[0x26]

    @ev_hp.setter
    def ev_hp(self, value: int) -> None:
        self.data[0x26] = value & 0xFF

    @property
    def ev_atk(self) -> int:
        return self.data[0x27]

    @ev_atk.setter
    def ev_atk(self, value: int) -> None:
        self.data[0x27] = value & 0xFF

    @property
    def ev_def(self) -> int:
        return self.data[0x28]

    @ev_def.setter
    def ev_def(self, value: int) -> None:
        self.data[0x28] = value & 0xFF

    @property
    def ev_spe(self) -> int:
        return self.data[0x29]

    @ev_spe.setter
    def ev_spe(self, value: int) -> None:
        self.data[0x29] = value & 0xFF

    @property
    def ev_spa(self) -> int:
        return self.data[0x2A]

    @ev_spa.setter
    def ev_spa(self, value: int) -> None:
        self.data[0x2A] = value & 0xFF

    @property
    def ev_spd(self) -> int:
        return self.data[0x2B]

    @ev_spd.setter
    def ev_spd(self, value: int) -> None:
        self.data[0x2B] = value & 0xFF

    # -- Block B ----------------------------------------------------------
    @property
    def nickname(self) -> str:
        return _get_string(self.data[0x58:0x72])

    @nickname.setter
    def nickname(self, value: str) -> None:
        buf = bytearray(self.data[0x58:0x72])
        _set_string(buf, value, 12)
        self.data[0x58:0x72] = buf

    def move(self, index: int) -> int:
        return _u16(self.data, 0x72 + index * 2)

    def set_move(self, index: int, move_id: int) -> None:
        _set_u16(self.data, 0x72 + index * 2, move_id)

    def move_pp(self, index: int) -> int:
        return self.data[0x7A + index]

    def set_move_pp(self, index: int, pp: int) -> None:
        self.data[0x7A + index] = pp & 0xFF

    def move_pp_ups(self, index: int) -> int:
        return self.data[0x7E + index]

    def set_move_pp_ups(self, index: int, value: int) -> None:
        self.data[0x7E + index] = value & 0xFF

    @property
    def iv32(self) -> int:
        return _u32(self.data, 0x8C)

    @iv32.setter
    def iv32(self, value: int) -> None:
        _set_u32(self.data, 0x8C, value)

    def _get_iv(self, shift: int) -> int:
        return (self.iv32 >> shift) & 0x1F

    def _set_iv(self, shift: int, value: int) -> None:
        value = min(value, 31) & 0x1F
        self.iv32 = (self.iv32 & ~(0x1F << shift)) | (value << shift)

    @property
    def iv_hp(self) -> int:
        return self._get_iv(0)

    @iv_hp.setter
    def iv_hp(self, value: int) -> None:
        self._set_iv(0, value)

    @property
    def iv_atk(self) -> int:
        return self._get_iv(5)

    @iv_atk.setter
    def iv_atk(self, value: int) -> None:
        self._set_iv(5, value)

    @property
    def iv_def(self) -> int:
        return self._get_iv(10)

    @iv_def.setter
    def iv_def(self, value: int) -> None:
        self._set_iv(10, value)

    @property
    def iv_spe(self) -> int:
        return self._get_iv(15)

    @iv_spe.setter
    def iv_spe(self, value: int) -> None:
        self._set_iv(15, value)

    @property
    def iv_spa(self) -> int:
        return self._get_iv(20)

    @iv_spa.setter
    def iv_spa(self, value: int) -> None:
        self._set_iv(20, value)

    @property
    def iv_spd(self) -> int:
        return self._get_iv(25)

    @iv_spd.setter
    def iv_spd(self, value: int) -> None:
        self._set_iv(25, value)

    # -- Block C ------------------------------------------------------------
    @property
    def language(self) -> int:
        return self.data[0xD5]

    @language.setter
    def language(self, value: int) -> None:
        self.data[0xD5] = value & 0xFF

    # -- Block D --------------------------------------------------------
    @property
    def original_trainer_name(self) -> str:
        return _get_string(self.data[0xF8:0x112])

    @original_trainer_name.setter
    def original_trainer_name(self, value: str) -> None:
        buf = bytearray(self.data[0xF8:0x112])
        _set_string(buf, value, 12)
        self.data[0xF8:0x112] = buf

    @property
    def met_location(self) -> int:
        return _u16(self.data, 0x122)

    @met_location.setter
    def met_location(self, value: int) -> None:
        _set_u16(self.data, 0x122, value)

    @property
    def ball(self) -> int:
        return self.data[0x124]

    @ball.setter
    def ball(self, value: int) -> None:
        self.data[0x124] = value & 0xFF

    @property
    def met_level(self) -> int:
        return self.data[0x125] & ~0x80

    @met_level.setter
    def met_level(self, value: int) -> None:
        self.data[0x125] = (self.data[0x125] & 0x80) | (value & 0x7F)

    @property
    def original_trainer_gender(self) -> int:
        return self.data[0x125] >> 7

    @original_trainer_gender.setter
    def original_trainer_gender(self, value: int) -> None:
        self.data[0x125] = (self.data[0x125] & ~0x80) | ((value & 1) << 7)

    # -- Party-only stats (last 0x10 bytes of the 0x158 party buffer) -------
    @property
    def stat_level(self) -> int:
        return self.data[0x148]

    @stat_level.setter
    def stat_level(self, value: int) -> None:
        self.data[0x148] = value & 0xFF

    @property
    def stat_hp_current(self) -> int:
        return _u16(self.data, 0x8A)

    @stat_hp_current.setter
    def stat_hp_current(self, value: int) -> None:
        _set_u16(self.data, 0x8A, value)

    @property
    def stat_hp_max(self) -> int:
        return _u16(self.data, 0x14A)

    @stat_hp_max.setter
    def stat_hp_max(self, value: int) -> None:
        _set_u16(self.data, 0x14A, value)

    @property
    def stat_atk(self) -> int:
        return _u16(self.data, 0x14C)

    @stat_atk.setter
    def stat_atk(self, value: int) -> None:
        _set_u16(self.data, 0x14C, value)

    @property
    def stat_def(self) -> int:
        return _u16(self.data, 0x14E)

    @stat_def.setter
    def stat_def(self, value: int) -> None:
        _set_u16(self.data, 0x14E, value)

    @property
    def stat_spe(self) -> int:
        return _u16(self.data, 0x150)

    @stat_spe.setter
    def stat_spe(self, value: int) -> None:
        _set_u16(self.data, 0x150, value)

    @property
    def stat_spa(self) -> int:
        return _u16(self.data, 0x152)

    @stat_spa.setter
    def stat_spa(self, value: int) -> None:
        _set_u16(self.data, 0x152, value)

    @property
    def stat_spd(self) -> int:
        return _u16(self.data, 0x154)

    @stat_spd.setter
    def stat_spd(self, value: int) -> None:
        _set_u16(self.data, 0x154, value)
