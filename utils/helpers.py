import re
from random import randint

import re
from random import randint
from discord.ext.commands import when_mentioned_or


def prefix(bot, message):
    prefixes = '.', '/t'
    if not message.guild:
        return prefixes[0]

    return when_mentioned_or(*prefixes)(bot, message)


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


def _normalize_dice(dice_list: list):
    new_list = {}
    for die in dice_list:
        amount, die_type, *modifier = re.split(r'd|\s?[+-]', die)
        print(amount, die_type, modifier)
        die_type = int(die_type)
        modifier = re.findall(r'[+-]\d+', die)
        if die_type == 1:
            continue
        if not die_type in new_list:
            new_list[die_type] = {'amount': int(amount)}
            if modifier:
                new_list[die_type]['modifiers'] = [int(modifier[0])]
            else:
                new_list[die_type]['modifiers'] = []
            continue
        new_list[die_type]['amount'] += int(amount)
        if new_list[die_type]['amount'] > 20:
            new_list[die_type]['amount'] = 20
        if modifier:
            new_list[die_type]['modifiers'].append(int(modifier[0]))
    return new_list


def roll_dice(dice: str):
    if not isinstance(dice, str):
        raise TypeError(f'Parameter `dice` must be of class `str`, not of {type(dice)}.')
    dice.replace(',', '')
    mdice = re.findall(r'\d+d\d+\s?[+-]\d+', dice)
    for result in mdice:
        dice = dice.replace(result, '')
    nmdice = re.findall(r'\d+d\d+', dice)
    dice = nmdice + mdice

    if not dice:
        raise TypeError('Either dice were not passed, or invalid dice were passed to the function.')
    total_dice = _normalize_dice(dice)
    for k, v in total_dice.items():
        temp_list = [[randint(1, k) for _ in range(v['amount'])]]
        temp_list.append(v['modifiers'])
        total_dice[k] = temp_list
    return total_dice
