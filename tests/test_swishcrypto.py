from pokehex.za import swishcrypto as sc


def _sample_blocks() -> list[sc.SCBlock]:
    return [
        sc.SCBlock(key=0x1234ABCD, type=sc.OBJECT, sub_type=0, data=bytearray(range(50))),
        sc.SCBlock(key=0xDEADBEEF, type=10, sub_type=0, data=bytearray((42).to_bytes(4, "little"))),  # UInt32
        sc.SCBlock(key=0x0D66012C, type=sc.OBJECT, sub_type=0, data=bytearray(1000)),
        sc.SCBlock(key=0xCAFEF00D, type=sc.ARRAY, sub_type=8, data=bytearray([1, 2, 3, 4, 5])),  # Byte[]
        sc.SCBlock(key=0x00000001, type=sc.BOOL2, sub_type=0, data=bytearray()),
    ]


def test_block_round_trip_via_full_save_cycle() -> None:
    blocks = _sample_blocks()
    encoded = sc.encrypt(blocks)

    assert sc.get_is_hash_valid(encoded)

    decoded = sc.decrypt(encoded)
    assert len(decoded) == len(blocks)
    for original, restored in zip(blocks, decoded):
        assert original.key == restored.key
        assert original.type == restored.type
        assert original.sub_type == restored.sub_type
        assert bytes(original.data) == bytes(restored.data)


def test_tampered_hash_is_detected() -> None:
    blocks = _sample_blocks()
    encoded = bytearray(sc.encrypt(blocks))
    encoded[0] ^= 0xFF
    assert not sc.get_is_hash_valid(bytes(encoded))
