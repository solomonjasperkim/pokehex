import random

import pytest

from pokehex.za import crypto


@pytest.mark.parametrize("seed", range(20))
def test_encrypt_decrypt_stored_round_trip(seed: int) -> None:
    rng = random.Random(seed)
    data = bytearray(rng.getrandbits(8) for _ in range(crypto.SIZE_STORED))
    original = bytes(data)

    crypto.encrypt8(data)
    assert bytes(data) != original  # sanity: it actually changed something

    crypto.decrypt8(data)
    assert bytes(data) == original


@pytest.mark.parametrize("seed", range(20))
def test_encrypt_decrypt_party_round_trip(seed: int) -> None:
    rng = random.Random(seed)
    data = bytearray(rng.getrandbits(8) for _ in range(crypto.SIZE_PARTY))
    original = bytes(data)

    crypto.encrypt8(data)
    crypto.decrypt8(data)
    assert bytes(data) == original


def test_decrypt_if_encrypted_is_idempotent_on_plaintext() -> None:
    # A buffer with zeroed nickname/OT trash (as freshly-built plaintext has)
    # should be recognized as "not encrypted" and left untouched.
    data = bytearray(crypto.SIZE_STORED)
    before = bytes(data)
    crypto.decrypt_if_encrypted8(data)
    assert bytes(data) == before


def test_rejects_wrong_size() -> None:
    with pytest.raises(ValueError):
        crypto.encrypt8(bytearray(10))
