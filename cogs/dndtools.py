import logging
import requests

from backends.encounter_gen import calculate_xp, load_monsters, create_monster_list, encounter_gen, final_encounter

from discord.ext.commands import Cog, command
from discord import Embed, Colour


log = logging.getLogger('bot.' + __name__)


class DndTools(Cog, name='D&D Tools'):
    """Various D&D tools."""
    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://www.dandwiki.com//w/api.php?'

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
    async def encounter_command(self, ctx, psize, plevel, difficulty, environment=None):
        """Generates a random encounter based on the users inputs.
        The user can input: the size of the party, the average level of the party,
        the difficulty of the encounter and the environment it takes place in."""
        check = 0
        difficulties = ['easy', 'medium', 'difficult', 'deadly']
        environments = ['city', 'dungeon', 'forest', 'nature', 'other plane', 'underground', 'water']
        try:
            psize = int(psize)
            plevel = int(plevel)
        except ValueError:
            return await ctx.send('Party size and level must be numbers.')
        if plevel > 20:
            return await ctx.send('Party level must be a number between 1 and 20.')
        if psize > 10:
            return await ctx.send('Party size must be a number between 1 and 20.')
        if difficulty in difficulties:
            if difficulty == 'easy':
                difficulty = 1
            if difficulty == 'medium':
                difficulty = 2
            if difficulty == 'difficult':
                difficulty = 3
            if difficulty == 'deadly':
                difficulty = 4
        else:
            return await ctx.send(f"{difficulty} is not a valid difficulty. Please choose from 1 of the following "
                                  f"difficulties: **{' - '.join(difficulties)}**")
        if environment is None:
            check = 1
        else:
            if environment not in environments:
                return await ctx.send(f"{environment} is not a valid environment. Please choose from 1 of the following"
                                      f" environments: **{' - '.join(environments)}**")
        xp = calculate_xp(plevel, difficulty, psize)
        monsterdata = load_monsters()
        possiblemonsters = create_monster_list(monsterdata, environment, check)
        encounter = encounter_gen(possiblemonsters, xp)
        final = final_encounter(encounter, xp)
        return await ctx.send(final)

    @command('homebrew')
    async def homebrew_lookup(self, ctx, name):
        link = []
        session = requests.Session()
        params = {
            "action": "opensearch",
            "format": "json",
            "maxage": "0",
            "search": name
        }
        request = session.get(url=self.url, params=params)
        data = request.json()
        links = dict(zip(data[1], data[3]))
        for key in links:
            encoded_link = links[key].replace(')', '\)').replace('(', '\(')
            link.append(f"[{key}]({encoded_link})")
        homebrew_embed = Embed(title=name, description='\n'.join(link), colour=Colour.blurple())
        return await ctx.send(embed=homebrew_embed)


def setup(bot):
    bot.add_cog(DndTools(bot))
    log.debug('Reddit cog loaded.')
