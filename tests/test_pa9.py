from pokehex.za.pa9 import PA9


def _sample_pkm() -> PA9:
    pkm = PA9()
    pkm.encryption_constant = 0xDEADBEEF
    pkm.pid = 0x12345678
    pkm.species = 6  # Charizard
    pkm.form = 0
    pkm.stat_level = 50
    pkm.nickname = "Blaze"
    pkm.original_trainer_name = "Solomon"
    pkm.tid16 = 12345
    pkm.sid16 = 6789
    pkm.nature = 3
    pkm.ability = 22
    pkm.ability_number = 1
    pkm.gender = 0
    pkm.ball = 4
    pkm.held_item = 0
    pkm.iv_hp = 31
    pkm.iv_atk = 20
    pkm.iv_def = 15
    pkm.iv_spa = 31
    pkm.iv_spd = 5
    pkm.iv_spe = 0
    pkm.ev_hp = 252
    pkm.ev_atk = 0
    pkm.ev_def = 4
    pkm.ev_spa = 252
    pkm.ev_spd = 0
    pkm.ev_spe = 0
    pkm.set_move(0, 7)
    pkm.set_move(1, 52)
    pkm.set_move(2, 0)
    pkm.set_move(3, 0)
    pkm.stat_hp_max = 150
    pkm.stat_atk = 100
    pkm.stat_def = 90
    pkm.stat_spa = 120
    pkm.stat_spd = 95
    pkm.stat_spe = 105
    pkm.stat_hp_current = 150
    return pkm


def test_encrypt_decrypt_round_trip_preserves_fields() -> None:
    pkm = _sample_pkm()
    encoded = pkm.to_encrypted_bytes()

    restored = PA9.from_encrypted(encoded)

    assert restored.species == 6
    assert restored.form == 0
    assert restored.stat_level == 50
    assert restored.nickname == "Blaze"
    assert restored.original_trainer_name == "Solomon"
    assert restored.tid16 == 12345
    assert restored.sid16 == 6789
    assert restored.nature == 3
    assert restored.ability == 22
    assert restored.ability_number == 1
    assert restored.ball == 4
    assert (restored.iv_hp, restored.iv_atk, restored.iv_def, restored.iv_spa, restored.iv_spd, restored.iv_spe) == (
        31, 20, 15, 31, 5, 0,
    )
    assert (restored.ev_hp, restored.ev_atk, restored.ev_def, restored.ev_spa, restored.ev_spd, restored.ev_spe) == (
        252, 0, 4, 252, 0, 0,
    )
    assert restored.move(0) == 7
    assert restored.move(1) == 52
    assert restored.stat_atk == 100
    assert restored.stat_spe == 105
    assert restored.checksum_valid


def test_iv_clamped_to_31() -> None:
    pkm = PA9()
    pkm.iv_hp = 99
    assert pkm.iv_hp == 31


def test_blank_pokemon_is_zeroed() -> None:
    pkm = PA9()
    assert pkm.species == 0
    assert pkm.nickname == ""
