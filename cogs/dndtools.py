import json
import logging

from backends.encounter_gen import calculate_xp, encounter_gen, final_encounter

from discord.ext.commands import Cog, command
from discord import Embed, Colour


log = logging.getLogger('bot.' + __name__)


class DndTools(Cog, name='D&D Tools'):
    """Various D&D tools."""
    def __init__(self, bot):
        self.bot = bot
        self.aiohttp_session = bot.aiohttp_session
        self.homebrew_url = 'https://www.dandwiki.com/w/api.php'

    @command(name='currency')
    async def currency_command(self, ctx, *coins):
        """Recalculates the given currency into the highest possible value.
        ;currency 500sp will recalculate it into 5pp.
        Multiple currencies can be given."""
        cp = sum([int(coin[:-2]) for coin in coins if coin[-2:] == "cp"])
        sp = sum([int(coin[:-2]) for coin in coins if coin[-2:] == "sp"])
        ep = sum([int(coin[:-2]) for coin in coins if coin[-2:] == "ep"])
        gp = sum([int(coin[:-2]) for coin in coins if coin[-2:] == "gp"])
        pp = sum([int(coin[:-2]) for coin in coins if coin[-2:] == "pp"])
        total = (cp * 1) + (sp * 10) + (ep * 50) + (gp * 100) + (pp * 1000)
        cp = total % 10
        total = total // 10
        sp = total % 10
        total = total // 10
        gp = total % 10
        total = total // 10
        pp = total
        return await ctx.send(f"Recalculated your currency into: {str(cp)}cp, {str(sp)}sp, {str(gp)}gp and {str(pp)}pp")

    @command(name='encounter')
    async def encounter_command(self, ctx, psize, plevel, difficulty, environment=None, dm=None):
        """Generates a random encounter based on the users inputs.
        The user can input: the size of the party, the average level of the party,
        the difficulty of the encounter and the environment it takes place in."""
        difficulties = ['easy', 'medium', 'difficult', 'deadly']
        environments = ['city', 'dungeon', 'forest', 'nature', 'other plane', 'underground', 'water']
        try:
            psize = int(psize)
            plevel = int(plevel)
        except ValueError:
            return await ctx.send('Party size and level must be numbers.')
        if psize < 1 or psize > 10:
            return await ctx.send('Party size must be a number between 1 and 10.')
        if plevel < 1 or plevel > 20:
            return await ctx.send('Party level must be a number between 1 and 20.')
        if difficulty in difficulties:
            diff_level = difficulties.index(difficulty) + 1
        else:
            return await ctx.send(f"\"{difficulty}\" is not a valid difficulty. Please choose one of: "
                                  f"**{' - '.join(difficulties)}**")
        if environment is not None:
            if environment not in environments:
                return await ctx.send(f"\"{environment}\" is not a valid environment. Please choose one of: "
                                      f"**{' - '.join(environments)}**")
        xp = calculate_xp(plevel, psize, diff_level)
        encounter = encounter_gen(environment, xp)
        final = final_encounter(encounter, xp)
        if dm is not None and dm.lower() in ('dm', 'pm'):
            await ctx.author.send(final)
            return await ctx.send("Sent results by DM.")
        return await ctx.send(final)

    @command('homebrew')
    async def homebrew_lookup(self, ctx, name):
        """Lookup homebrew content from dandwiki."""
        link = []
        params = {
            "action": "opensearch",
            "format": "json",
            "maxage": "0",
            "search": name
        }
        async with self.aiohttp_session.get(self.homebrew_url, params=params) as resp:
            log.debug(f"Issued homebrew API request to {resp.url}")
            data = json.loads(await resp.text())
        links = dict(zip(data[1], data[3]))
        for key in links:
            encoded_link = links[key].replace(')', '\\)').replace('(', '\\(')
            link.append(f"[{key}]({encoded_link})")
        homebrew_embed = Embed(title=name, description='\n'.join(link), colour=Colour.blurple())
        return await ctx.send(embed=homebrew_embed)


def setup(bot):
    bot.add_cog(DndTools(bot))
    log.debug('Loaded')
