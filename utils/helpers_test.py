import pytest

from helpers import split_text, dice_roller


def test_split_text():
    text = 'testtesttest'
    split = split_text(text, 3)
    assert split == ['tes', 'tte', 'stt', 'est']
    split = split_text(text, 7)
    assert split == ['testtes', 'ttest']


def test_dice_roller():
    with pytest.raises(TypeError):
        roll = dice_roller('10d1')
    roll = dice_roller('50d2')
    dice = roll['50d2']['rolls']
    assert all(die in dice for die in ('1', '2'))
