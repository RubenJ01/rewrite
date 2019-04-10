import re
from random import randint
from re import findall

from discord.ext.commands import when_mentioned_or


def prefix(bot, message):
    prefixes = '.', '/t'
    if not message.guild:
        return prefixes[0]

    return when_mentioned_or(*prefixes)(bot, message)


def roll_dice(dice: str = '1d20'):
    dice = findall(r'\d+d\d+', dice)
    if not dice:
        # TODO This should stop the command and raise an error if it can't find dice. Do later.
        return
    total_dice = {}
    for die in dice:
        dice_vars = [int(x) for x in die.split('d')]
        total_dice[die] = [str(randint(1, dice_vars[1])) for _ in range(dice_vars[0])]
    return total_dice


async def api_request(ctx, endpoint, value):
    async with ctx.bot._http.session.get(f'http://dnd5eapi.co/api/{endpoint}/{value}') as req:
        return await req.json()


def split_text(text: str, length: int) -> list:
    """Split text into strings of at most 'length' characters.

    Returns a list of strings.
    """
    if len(text) <= length:
        return [text]
    splits = []
    while len(text) > length:
        splits.append(text[:length])
        text = text[length:]
    if len(text) > 0:
        splits.append(text)
    return splits


def dice_roller(dice: str):
    if not isinstance(dice, str):
        raise TypeError(f'Parameter `dice` must be of type `str`, not of {type(dice)}.')
    dice.replace(',', '')
    mdice = re.findall(r'\d+d\d+\s?[+-]\d+', dice)
    for result in mdice:
        dice = dice.replace(result, '')
    nmdice = re.findall(r'\d+d\d+', dice)
    dice = nmdice + mdice

    if not dice:
        raise TypeError('Either dice were not passed, or invalid dice were passed to the function.')
    total_dice = {}
    for die in dice:
        dice_vars = [int(x) for x in re.split(r'[d, \s\+]', die) if x]
        if dice_vars[1] == 1:
            if len(dice) == 1:
                raise TypeError('Rolling D1s are not allowed.')
            else:
                continue
        total_dice[die] = {'rolls': [str(randint(1, dice_vars[1])) for _ in range(dice_vars[0])],
                           'modifier': None}
        if len(dice_vars) > 2:
            total_dice[die]['modifier'] = dice_vars[2]

    return total_dice
