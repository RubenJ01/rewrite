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
