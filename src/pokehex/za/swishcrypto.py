"""SwishCrypto: the block-based save-file container format used by SV/Z-A.

Ported from PKHeX.Core/Saves/Encryption/SwishCrypto/{SwishCrypto,SCBlock,
SCXorShift32,SCTypeCode}.cs (https://github.com/kwsch/PKHeX, GPL-3.0).

A save file is: [xor-obfuscated block stream][32-byte SHA-256 hash]. Each
block is individually keyed and "encrypted" with a tiny xorshift stream
cipher derived from its own key -- this is obfuscation, not real security.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

HASH_SIZE = 32

_INTRO_HASH_BYTES = bytes([
    0x9E, 0xC9, 0x9C, 0xD7, 0x0E, 0xD3, 0x3C, 0x44, 0xFB, 0x93, 0x03, 0xDC, 0xEB, 0x39, 0xB4, 0x2A,
    0x19, 0x47, 0xE9, 0x63, 0x4B, 0xA2, 0x33, 0x44, 0x16, 0xBF, 0x82, 0xA2, 0xBA, 0x63, 0x55, 0xB6,
    0x3D, 0x9D, 0xF2, 0x4B, 0x5F, 0x7B, 0x6A, 0xB2, 0x62, 0x1D, 0xC2, 0x1B, 0x68, 0xE5, 0xC8, 0xB5,
    0x3A, 0x05, 0x90, 0x00, 0xE8, 0xA8, 0x10, 0x3D, 0xE2, 0xEC, 0xF0, 0x0C, 0xB2, 0xED, 0x4F, 0x6D,
])

_OUTRO_HASH_BYTES = bytes([
    0xD6, 0xC0, 0x1C, 0x59, 0x8B, 0xC8, 0xB8, 0xCB, 0x46, 0xE1, 0x53, 0xFC, 0x82, 0x8C, 0x75, 0x75,
    0x13, 0xE0, 0x45, 0xDF, 0x32, 0x69, 0x3C, 0x75, 0xF0, 0x59, 0xF8, 0xD9, 0xA2, 0x5F, 0xB2, 0x17,
    0xE0, 0x80, 0x52, 0xDB, 0xEA, 0x89, 0x73, 0x99, 0x75, 0x79, 0xAF, 0xCB, 0x2E, 0x80, 0x07, 0xE6,
    0xF1, 0x26, 0xE0, 0x03, 0x0A, 0xE6, 0x6F, 0xF6, 0x41, 0xBF, 0x7E, 0x59, 0xC2, 0xAE, 0x55, 0xFD,
])

# Only the first 127 bytes matter -- the 128th is a trailing zero that makes
# the windowed C# implementation's overlap a no-op. The true period is 127.
_STATIC_XORPAD = bytes([
    0xA0, 0x92, 0xD1, 0x06, 0x07, 0xDB, 0x32, 0xA1, 0xAE, 0x01, 0xF5, 0xC5, 0x1E, 0x84, 0x4F, 0xE3,
    0x53, 0xCA, 0x37, 0xF4, 0xA7, 0xB0, 0x4D, 0xA0, 0x18, 0xB7, 0xC2, 0x97, 0xDA, 0x5F, 0x53, 0x2B,
    0x75, 0xFA, 0x48, 0x16, 0xF8, 0xD4, 0x8A, 0x6F, 0x61, 0x05, 0xF4, 0xE2, 0xFD, 0x04, 0xB5, 0xA3,
    0x0F, 0xFC, 0x44, 0x92, 0xCB, 0x32, 0xE6, 0x1B, 0xB9, 0xB1, 0x2E, 0x01, 0xB0, 0x56, 0x53, 0x36,
    0xD2, 0xD1, 0x50, 0x3D, 0xDE, 0x5B, 0x2E, 0x0E, 0x52, 0xFD, 0xDF, 0x2F, 0x7B, 0xCA, 0x63, 0x50,
    0xA4, 0x67, 0x5D, 0x23, 0x17, 0xC0, 0x52, 0xE1, 0xA6, 0x30, 0x7C, 0x2B, 0xB6, 0x70, 0x36, 0x5B,
    0x2A, 0x27, 0x69, 0x33, 0xF5, 0x63, 0x7B, 0x36, 0x3F, 0x26, 0x9B, 0xA3, 0xED, 0x7A, 0x53, 0x00,
    0xA4, 0x48, 0xB3, 0x50, 0x9E, 0x14, 0xA0, 0x52, 0xDE, 0x7E, 0x10, 0x2B, 0x1B, 0x77, 0x6E,
])[:127]


def _crypt_static_xorpad(data: bytearray) -> None:
    for i in range(len(data)):
        data[i] ^= _STATIC_XORPAD[i % 127]


def _compute_hash(payload: bytes) -> bytes:
    h = hashlib.sha256()
    h.update(_INTRO_HASH_BYTES)
    h.update(payload)
    h.update(_OUTRO_HASH_BYTES)
    return h.digest()


class SCXorShift32:
    """Self-mutating per-block xor keystream."""

    def __init__(self, seed: int) -> None:
        self._counter = 0
        self._state = self._initial_state(seed & 0xFFFFFFFF)

    @staticmethod
    def _advance(state: int) -> int:
        state &= 0xFFFFFFFF
        state ^= (state << 2) & 0xFFFFFFFF
        state ^= state >> 15
        state ^= (state << 13) & 0xFFFFFFFF
        return state & 0xFFFFFFFF

    @classmethod
    def _initial_state(cls, seed: int) -> int:
        state = seed
        for _ in range(bin(seed).count("1")):
            state = cls._advance(state)
        return state

    def next(self) -> int:
        result = (self._state >> (self._counter << 3)) & 0xFF
        if self._counter == 3:
            self._state = self._advance(self._state)
            self._counter = 0
        else:
            self._counter += 1
        return result

    def next32(self) -> int:
        return self.next() | (self.next() << 8) | (self.next() << 16) | (self.next() << 24)


# SCTypeCode values
BOOL1, BOOL2, BOOL3 = 1, 2, 3
OBJECT = 4
ARRAY = 5
_PRIMITIVE_SIZES = {8: 1, 9: 2, 10: 4, 11: 8, 12: 1, 13: 2, 14: 4, 15: 8, 16: 4, 17: 8}


@dataclass
class SCBlock:
    key: int
    type: int
    sub_type: int
    data: bytearray


def _read_block(buf: bytes, offset: int) -> tuple[SCBlock, int]:
    key = int.from_bytes(buf[offset:offset + 4], "little")
    offset += 4
    xk = SCXorShift32(key)
    block_type = buf[offset] ^ xk.next()
    offset += 1

    if block_type in (BOOL1, BOOL2, BOOL3):
        return SCBlock(key, block_type, 0, bytearray()), offset

    if block_type == OBJECT:
        length = int.from_bytes(buf[offset:offset + 4], "little") ^ xk.next32()
        offset += 4
        raw = bytearray(buf[offset:offset + length])
        offset += length
        for i in range(len(raw)):
            raw[i] ^= xk.next()
        return SCBlock(key, block_type, 0, raw), offset

    if block_type == ARRAY:
        count = int.from_bytes(buf[offset:offset + 4], "little") ^ xk.next32()
        offset += 4
        sub_type = buf[offset] ^ xk.next()
        offset += 1
        num_bytes = count * _PRIMITIVE_SIZES[sub_type]
        raw = bytearray(buf[offset:offset + num_bytes])
        offset += num_bytes
        for i in range(len(raw)):
            raw[i] ^= xk.next()
        return SCBlock(key, block_type, sub_type, raw), offset

    # single primitive value
    num_bytes = _PRIMITIVE_SIZES[block_type]
    raw = bytearray(buf[offset:offset + num_bytes])
    offset += num_bytes
    for i in range(len(raw)):
        raw[i] ^= xk.next()
    return SCBlock(key, block_type, 0, raw), offset


def _write_block(block: SCBlock) -> bytes:
    out = bytearray()
    out += block.key.to_bytes(4, "little")
    xk = SCXorShift32(block.key)
    out.append((block.type ^ xk.next()) & 0xFF)

    if block.type == OBJECT:
        out += ((len(block.data)) ^ xk.next32()).to_bytes(4, "little")
    elif block.type == ARRAY:
        entries = len(block.data) // _PRIMITIVE_SIZES[block.sub_type]
        out += (entries ^ xk.next32()).to_bytes(4, "little")
        out.append((block.sub_type ^ xk.next()) & 0xFF)

    for b in block.data:
        out.append((b ^ xk.next()) & 0xFF)
    return bytes(out)


def get_is_hash_valid(data: bytes) -> bool:
    payload, stored_hash = data[:-HASH_SIZE], data[-HASH_SIZE:]
    return _compute_hash(payload) == stored_hash


def decrypt(data: bytes) -> list[SCBlock]:
    """Decrypt raw save file bytes into a list of blocks."""
    payload = bytearray(data[:-HASH_SIZE])
    _crypt_static_xorpad(payload)

    blocks: list[SCBlock] = []
    offset = 0
    buf = bytes(payload)
    while offset < len(buf):
        block, offset = _read_block(buf, offset)
        blocks.append(block)
    return blocks


def encrypt(blocks: list[SCBlock]) -> bytes:
    """Serialize blocks back into a valid, freshly-hashed save file."""
    payload = bytearray()
    for block in blocks:
        payload += _write_block(block)

    _crypt_static_xorpad(payload)
    checksum = _compute_hash(bytes(payload))
    return bytes(payload) + checksum
