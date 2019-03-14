import logging
import random

from discord import Colour, Embed
from discord.ext.commands import Cog, command

log = logging.getLogger('bot.' + __name__)


class RollingCog(Cog, name='Roller'):

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
        if not 1 < iamount <= 10:
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
        rngstat_embed.set_footer(text='Use ;rngstat {optional amount}to roll up to 10 ability scores.')
        return await ctx.send(embed=rngstat_embed)


def setup(bot):
    bot.add_cog(RollingCog(bot))
    log.debug('Loaded')
