"""Pytest tests for helpers.py"""

import helpers as m


def test_split_text():
    text = 'testtesttest'
    split = m.split_text(text, 3)
    assert split == ['tes', 'tte', 'stt', 'est']
    split = m.split_text(text, 7)
    assert split == ['testtes', 'ttest']


def test_dice_roller():
    roll = m.roll_dice('10d1')
    assert roll == {}
    roll = m.roll_dice('50d2')
    dice = roll[2][0]
    assert all(die in dice for die in (1, 2))
