import logging
import random
from pathlib import Path

from backends.npc_gen import final_output
from backends.name_gen import name_gen

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
    "backstory": Path('resources') / 'backstorys.txt',  # list of backstory's
}


class GeneratorCog(Cog, name='Generator'):
    """Information generators.

    These commands allow for users to generate information from pre-determined files."""

    def __init__(self, bot):
        self.bot = bot

    @command(name='generate')
    async def generator_command(self, ctx, generate=None, amount: int = None, dm=None):
        """All of the generate commands that are used to generate things, such as:
        characters, NPCs and names."""
        log.debug(f'generate request with type={generate} and amount={amount}')
        generator_embed = Embed(colour=Colour.blurple())
        commands = ['backstory', 'bond', 'flaw', 'ideal', 'quest', 'townname', 'trait']
        commands.sort()
        desc = ''
        num = 0
        if generate not in commands:  # user requested an invalid option; show help
            generator_embed.title = 'All of the Generator Commands'
            for _ in commands:
                desc += f'**{commands[num]}** \n'
                num = num + 1
            generator_embed.description = desc
            help = 'Use ;generate {command} {optional amount} to use one of the above commands.'
            generator_embed.set_footer(text=help)
            return await ctx.send(embed=generator_embed)

        final = str.casefold(generate)
        with open(paths[final], 'r', encoding='utf-8') as f:
            strings = f.readlines()
        if amount is None:
            message = random.choice(strings)
            return await ctx.send(random.choice(strings))
        try:
            iamount = int(amount)
        except ValueError:
            return await ctx.send(f'{amount} is not a valid number of {final}s to generate.')
        else:
            if not 1 < iamount <= 5:
                return await ctx.send(f'Please choose a number of {final}s between 2 and 5.')
            message = ''.join(random.choices(strings, k=iamount))
        if dm is not None:
            dm = dm.lower()
            if dm.startswith('d') or dm.startswith('p'):
                await ctx.send("Sended the results your dm.")
                return await ctx.author.send(message)
        await ctx.send(message)

    @command(name='npc')
    async def npc_command(self, ctx):
        """Generates a random npc, based on P.89 of the Dungeon Masters Guide."""
        desc = final_output()
        embed = Embed(colour=Colour.blurple())
        embed.add_field(name='Randomly generated npc.', value=desc, inline=True)
        return await ctx.send(embed=embed)

    @command(name='name')
    async def name_generator(self, ctx, race, gender):
        """Generates a random name for the race and gender the user submitted."""
        result = name_gen(race, gender)
        return await ctx.send(result)


def setup(bot):
    bot.add_cog(GeneratorCog(bot))
    log.debug('Loaded')
