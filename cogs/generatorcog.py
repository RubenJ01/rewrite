import logging
import random
from pathlib import Path

from discord import Colour, Embed
from discord.ext.commands import Cog, command

log = logging.getLogger('bot.' + __name__)

paths = {
    "bond": Path('resources') / 'bonds.txt',  # list of bonds
    "flaw": Path('resources') / 'flaws.txt',  # list of flaws
    "ideal": Path('resources') / 'ideals.txt',  # list of ideals
    "trait": Path('resources') / 'traits.txt',  # list of traits
    "townname": Path('resources') / 'townnames.txt',  # list of town names
    "quest": Path('resources') / 'quests.txt',  # list of quests
}


class GeneratorCog(Cog, name='Generator'):

    def __init__(self, bot):
        self.bot = bot

    @command(name='generate')
    async def generator_command(self, ctx, generate=None, amount=None):
        """All of the generate commands that are used to generate things, such as:
        characters, NPCs and names."""
        log.debug(f'generate request with type={generate} and amount={amount}')
        generator_embed = Embed(colour=Colour.blurple())
        commands = ['bond', 'flaw', 'ideal', 'quest', 'townname', 'trait']
        desc = ''
        num = 0
        if generate not in commands:  # user requested an invalid option; show help
            generator_embed.title = 'All of the Generator Commands'
            for _ in commands:
                desc += f'**{commands[num]}** \n'
                num = num + 1
            generator_embed.description = desc
            generator_embed.set_footer(text='Use ;generate {command} {optional amount} to use one of the above commands.')
            return await ctx.send(embed=generator_embed)

        final = str.casefold(generate)
        with open(paths[final], 'r', encoding='utf-8') as f:
            strings = f.readlines()
        if amount is None:
            return await ctx.send(random.choice(strings))
        try:
            iamount = int(amount)
        except ValueError:
            return await ctx.send(f'{amount} is not a valid number of {final}s to generate.')
        else:
            if not 1 < iamount <= 5:
                return await ctx.send(f'Please choose a number of {final}s between 2 and 5.')
            return await ctx.send(''.join(random.choices(strings, k=iamount)))


def setup(bot):
    bot.add_cog(GeneratorCog(bot))
    log.debug('Loaded')
