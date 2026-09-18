import pytest

from pokehex.pokemon import EVs, IVs, Pokemon


def test_default_pokemon_is_valid() -> None:
    mon = Pokemon(species=6, level=50, nickname="Charizard")
    assert mon.species == 6
    assert mon.level == 50
    assert mon.ivs.hp == 0
    assert mon.evs.hp == 0


def test_invalid_level_rejected() -> None:
    with pytest.raises(ValueError):
        Pokemon(species=6, level=0)
    with pytest.raises(ValueError):
        Pokemon(species=6, level=101)


def test_iv_out_of_range_rejected() -> None:
    with pytest.raises(ValueError):
        Pokemon(species=6, ivs=IVs(hp=32))


def test_ev_total_over_max_rejected() -> None:
    with pytest.raises(ValueError):
        Pokemon(species=6, evs=EVs(hp=252, atk=252, def_=252))


def test_too_many_moves_rejected() -> None:
    from pokehex.pokemon import Move

    with pytest.raises(ValueError):
        Pokemon(species=6, moves=[Move(id=i) for i in range(5)])
