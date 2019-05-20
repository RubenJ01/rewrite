import pytest

from helpers import split_text, roll_dice


def test_split_text():
    text = 'testtesttest'
    split = split_text(text, 3)
    assert split == ['tes', 'tte', 'stt', 'est']
    split = split_text(text, 7)
    assert split == ['testtes', 'ttest']


def test_dice_roller():
    roll = roll_dice('10d1')
    assert roll == {}
    roll = roll_dice('50d2')
    dice = roll[2][0]
    assert all(die in dice for die in (1, 2))
