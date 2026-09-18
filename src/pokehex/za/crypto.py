"""Gen8/PA9 entity encryption.

Ported from PKHeX.Core/PKM/Util/PokeCrypto.cs (Encrypt8/Decrypt8 and the
block-shuffle tables), which is also what PA9 (the format used by
Pokemon Legends: Z-A) uses for its "stored" and "party" byte layout.
Source: https://github.com/kwsch/PKHeX (GPL-3.0) -- structure/algorithm
ported to Python; no original source code copied verbatim.
"""

from __future__ import annotations

BLOCK_COUNT = 4
BLOCK_SIZE = 80  # 0x50
SIZE_STORED = 8 + BLOCK_COUNT * BLOCK_SIZE  # 0x148 (328)
SIZE_PARTY = SIZE_STORED + 0x10  # 0x158 (344)

_BLOCK_POSITION = [
    0, 1, 2, 3, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 1, 2,
    0, 2, 3, 1, 0, 3, 2, 1, 1, 0, 2, 3, 1, 0, 3, 2,
    2, 0, 1, 3, 3, 0, 1, 2, 2, 0, 3, 1, 3, 0, 2, 1,
    1, 2, 0, 3, 1, 3, 0, 2, 2, 1, 0, 3, 3, 1, 0, 2,
    2, 3, 0, 1, 3, 2, 0, 1, 1, 2, 3, 0, 1, 3, 2, 0,
    2, 1, 3, 0, 3, 1, 2, 0, 2, 3, 1, 0, 3, 2, 1, 0,
    0, 1, 2, 3, 0, 1, 3, 2, 0, 2, 1, 3, 0, 3, 1, 2,
    0, 2, 3, 1, 0, 3, 2, 1, 1, 0, 2, 3, 1, 0, 3, 2,
]

_BLOCK_POSITION_INVERT = [
    0, 1, 2, 4,
    3, 5, 6, 7,
    12, 18, 13, 19,
    8, 10, 14, 20,
    16, 22, 9, 11,
    15, 21, 17, 23,
    0, 1, 2, 4,
    3, 5, 6, 7,
]


def _crypt_array(data: bytearray, seed: int) -> None:
    """XOR-stream cipher over 16-bit words using the games' LCG."""
    seed &= 0xFFFFFFFF
    for i in range(0, len(data) - 1, 2):
        seed = (0x41C64E6D * seed + 0x00006073) & 0xFFFFFFFF
        xor = seed >> 16
        word = data[i] | (data[i + 1] << 8)
        word ^= xor
        data[i] = word & 0xFF
        data[i + 1] = (word >> 8) & 0xFF


def _shuffle_blocks(data: bytearray, sv: int) -> None:
    """Rearrange the 4 data blocks according to permutation table index sv."""
    if sv == 0:
        return
    order = _BLOCK_POSITION[sv * BLOCK_COUNT: sv * BLOCK_COUNT + BLOCK_COUNT]
    blocks = [bytes(data[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE]) for i in range(BLOCK_COUNT)]
    for slot, original_index in enumerate(order):
        data[slot * BLOCK_SIZE:(slot + 1) * BLOCK_SIZE] = blocks[original_index]


def _read_u32le(data: bytes, offset: int) -> int:
    return data[offset] | (data[offset + 1] << 8) | (data[offset + 2] << 16) | (data[offset + 3] << 24)


def decrypt8(data: bytearray) -> None:
    """Decrypt a stored (0x148) or party (0x158) PA9/PK8/PK9-family buffer in place."""
    if len(data) not in (SIZE_STORED, SIZE_PARTY):
        raise ValueError(f"expected {SIZE_STORED} or {SIZE_PARTY} bytes, got {len(data)}")
    pv = _read_u32le(data, 0)
    sv = (pv >> 13) & 31

    block_region = data[8:SIZE_STORED]
    _crypt_array(block_region, pv)
    data[8:SIZE_STORED] = block_region

    if len(data) > SIZE_STORED:
        party_region = data[SIZE_STORED:]
        _crypt_array(party_region, pv)
        data[SIZE_STORED:] = party_region

    block_region = data[8:SIZE_STORED]
    _shuffle_blocks(block_region, sv)
    data[8:SIZE_STORED] = block_region


def encrypt8(data: bytearray) -> None:
    """Encrypt a stored (0x148) or party (0x158) PA9/PK8/PK9-family buffer in place."""
    if len(data) not in (SIZE_STORED, SIZE_PARTY):
        raise ValueError(f"expected {SIZE_STORED} or {SIZE_PARTY} bytes, got {len(data)}")
    pv = _read_u32le(data, 0)
    sv = (pv >> 13) & 31
    sv = _BLOCK_POSITION_INVERT[sv]

    block_region = data[8:SIZE_STORED]
    _shuffle_blocks(block_region, sv)
    _crypt_array(block_region, pv)
    data[8:SIZE_STORED] = block_region

    if len(data) > SIZE_STORED:
        party_region = data[SIZE_STORED:]
        _crypt_array(party_region, pv)
        data[SIZE_STORED:] = party_region


def is_encrypted8(data: bytes) -> bool:
    """Heuristic: the last two bytes of the (decrypted) nickname/OT name slots should be 0."""
    def u16(offset: int) -> int:
        return data[offset] | (data[offset + 1] << 8)

    return u16(0x70) != 0 or u16(0x110) != 0


def decrypt_if_encrypted8(data: bytearray) -> None:
    if is_encrypted8(data):
        decrypt8(data)
