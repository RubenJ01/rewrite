import logging
import random

from discord import Colour, Embed
from discord.ext.commands import Cog, command
from utils.helpers import dice_roller

log = logging.getLogger('bot.' + __name__)


class RollingCog(Cog, name='Dice Rolling'):
    """These are all the commands that are used to roll dice and stats in d&d."""
    def __init__(self, bot):
        self.bot = bot

    @command(name='rngstat')
    async def rng_stat(self, ctx, amount=None):
        """Command that rolls up to 10 ability scores at a time"""
        rngstat_embed = Embed(colour=Colour.blurple())
        rngstat_embed.title = "Ability Scores"
        counter = 0
        desc = ''
        if amount is None:
            amount = 1  # rolls 1 ability score by default
        try:
            iamount = int(amount)
        except ValueError:
            return await ctx.send(f'{amount} is not a valid number of ability scores to generate.')
        if not 1 <= iamount <= 10:
            return await ctx.send(f'Please choose a number of ability scores between 2 and 10.')
        log.debug(f'roll ability scores with amount={amount}')
        for _ in range(int(amount)):
            rolls = random.choices(range(1, 7), k=4)
            total = sum(rolls) - min(rolls)
            counter = counter + 1
            for rank, (position, roll) in enumerate(sorted(enumerate(rolls), reverse=True, key=lambda item: item[1])):
                rolls[position] = f"**{roll}**" if rank < 3 else f"{roll}"
            desc += f'Roll {counter}' + " (" + ", ".join(rolls) + ") " + "= " + str(total) + "\n"
        rngstat_embed.description = desc
        rngstat_embed.set_footer(text='Use ;rngstat {optional amount} to roll up to 10 ability scores.')
        return await ctx.send(embed=rngstat_embed)

    @command(name='roll')
    async def roll_command(self, ctx, *request):
        """Roll a numerous amount of dices. Format like: ;roll {dicetype} {modifier}.
        For example: ;roll 4d10 3d6 + 7. Multiple dices can be given."""
        try:
            request = ' '.join(request)
            values = dice_roller(request)
            total = 0
            output = []
            for inner_dict in values.values():
                rolls = inner_dict['rolls']
                mod = inner_dict['modifier']
                total += sum(int(roll) for roll in rolls)
                if mod is not None:
                    total += mod
                    output.extend(rolls + [str(mod)])
                if mod is None:
                    output.extend(rolls)
            return await ctx.send(
                f"That dice expression resulted in: {', '.join(output)} which sums to {total}")
        except TypeError as InvalidDice:
            return await ctx.send(InvalidDice)


def setup(bot):
    bot.add_cog(RollingCog(bot))
    log.debug('Loaded')
