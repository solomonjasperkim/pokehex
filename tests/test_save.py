from pokehex.za import swishcrypto as sc
from pokehex.za.pa9 import PA9
from pokehex.za.save import BOX_COUNT, KEY_BOX, SIZE_BOXSLOT, SLOTS_PER_BOX, SAV9ZA


def _blank_save() -> SAV9ZA:
    box_block = sc.SCBlock(
        key=KEY_BOX,
        type=sc.OBJECT,
        sub_type=0,
        data=bytearray(SIZE_BOXSLOT * BOX_COUNT * SLOTS_PER_BOX),
    )
    return SAV9ZA([box_block])


def test_new_save_all_slots_empty() -> None:
    sav = _blank_save()
    assert sav.is_slot_empty(0, 0)
    assert sav.find_empty_slot() == (0, 0)


def test_set_and_get_box_slot_round_trip() -> None:
    sav = _blank_save()
    pkm = PA9()
    pkm.species = 25  # Pikachu
    pkm.stat_level = 10
    pkm.pid = 0xAAAABBBB
    pkm.encryption_constant = 0xAAAABBBB

    sav.set_box_slot(0, 5, pkm)

    assert not sav.is_slot_empty(0, 5)
    restored = sav.get_box_slot(0, 5)
    assert restored.species == 25
    assert restored.stat_level == 10

    # other slots remain untouched
    assert sav.is_slot_empty(0, 4)
    assert sav.is_slot_empty(0, 6)
    assert sav.is_slot_empty(1, 5)


def test_full_load_save_cycle(tmp_path) -> None:
    sav = _blank_save()
    pkm = PA9()
    pkm.species = 150
    pkm.stat_level = 70
    pkm.pid = 0x11112222
    pkm.encryption_constant = 0x11112222
    sav.set_box_slot(3, 10, pkm)

    path = tmp_path / "save.bin"
    sav.save(str(path))

    reloaded = SAV9ZA.load(str(path))
    restored = reloaded.get_box_slot(3, 10)
    assert restored.species == 150
    assert restored.stat_level == 70


def test_out_of_range_box_rejected() -> None:
    sav = _blank_save()
    try:
        sav.get_box_slot(BOX_COUNT, 0)
        assert False, "expected ValueError"
    except ValueError:
        pass
