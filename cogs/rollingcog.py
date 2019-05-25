import logging
import random
from functools import partial

from discord import Colour, Embed
from discord.ext.commands import Cog, command

from utils.helpers import roll_dice

log = logging.getLogger('bot.' + __name__)


class RollingCog(Cog, name='Dice Rolling'):
    """Rolls dice. Allows for other dice-based outputs to be received."""
    def __init__(self, bot):
        self.bot = bot

    @command(name='rngstat')
    async def rng_stat(self, ctx, amount=None, dm=None):
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
        if dm is not None:
            dm = dm.lower()
            if dm.startswith('d') or dm.startswith('p'):
                await ctx.send("Sended the results your dm.")
                return await ctx.author.send(embed=rngstat_embed)
        await ctx.send(embed=rngstat_embed)

    @command(name='roll')
    async def roll_command(self, ctx, *, request='1d20'):
        """Roll a numerous amount of dices. Format like: ;roll {dicetype} {modifier}.
        For example: ;roll 4d10 3d6 + 7. Multiple dices can be given."""

        try:
            values = await self.bot.loop.run_in_executor(None, partial(roll_dice, request))
        except TypeError as InvalidDice:
            return await ctx.send(InvalidDice)
        desc = ''
        total_roll = 0
        for i, x in enumerate(values):
            total = values[x][0] + values[x][1]
            total_roll += sum(total)
            desc += f'**{len(values[x][0])} D{x}**: {values[x][0]}' \
                f'{" + **" + ", ".join([str(val) for val in values[x][1]]) + "**" if values[x][1] else ""}' \
                f' = **__{sum(total)}__**\n'
        roll_embed = Embed(
            title=f'🎲 {ctx.author} rolled! 🎲',
            description=desc,
            color=Colour.blurple())
        roll_embed.set_thumbnail(url=ctx.author.avatar_url)
        roll_embed.set_footer(text=f'Total of all dice: {total_roll} 🎲')
        return await ctx.send(embed=roll_embed)


def setup(bot):
    bot.add_cog(RollingCog(bot))
    log.debug('Loaded')
