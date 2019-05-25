"""Pytests for encounter_gen.py"""

import encounter_gen as m


def test_calculate_xp():
    # parameters: average level, party size, difficulty
    assert m.calculate_xp(4, 6, 1) == 750
    assert m.calculate_xp(18, 4, 3) == 25200


def test_encounter_gen():
    # parameters: environment (or None), XP cap
    assert m.encounter_gen(None, 0) == []
    assert len(m.encounter_gen(None, 10)) == 1
    monsters = m.encounter_gen(None, 1000)
    xp = sum(int(monster[4]) for monster in monsters)
    assert xp > 0
    assert xp <= 1000
    for environ in ('city', 'dungeon', 'forest', 'nature', 'other plane', 'underground', 'water'):
        monsters = m.encounter_gen(environ, 1000)
        assert len(monsters) > 0
        for monster in monsters:
            assert all(monster[1] == environ for monster in monsters)
