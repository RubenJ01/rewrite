import logging

from discord import Colour, Embed
from discord.ext.commands import Cog, command

from backends.srd_json import srd, get_spell_info

log = logging.getLogger('bot.' + __name__)

PHB_COLOUR = Colour(0xeeeea0)


class SRDCog(Cog, name='SRD Information'):
    def __init__(self, bot):
        self.bot = bot

    @command(name='spell')
    async def spell_command(self, ctx, *request):
        # TODO: Handle spells that exceed Discord embed size limits, like Imprisonment
        """Give information on a spell by name."""
        request = ' '.join(request).lower()
        log.debug(f'spell command called with request: {request}')
        if len(request) <= 2:
            return await ctx.send('Request too short.')
        matches, truncated = srd.search('spells', 'name', request, trunc=0)
        if len(matches) == 0:
            return await ctx.send(f'Couldn\'t find any spells that match \'{request}\'.')
        if len(matches) > 1:
            spell_names = [match['name'] for match in matches]
            return await ctx.send(f'Could be: {", ".join(spell_names)}.')
        spell = matches[0]
        info = get_spell_info(spell)
        embed = Embed(title=info.name,
                      colour=PHB_COLOUR,
                      description=f'*{info.subhead}*\n{info.description}')
        embed.add_field(name="Casting Time", value=info.casting_time, inline=True)
        embed.add_field(name="Range", value=info.casting_range, inline=True)
        embed.add_field(name="Components", value=info.components, inline=True)
        embed.add_field(name="Duration", value=info.duration, inline=True)
        embed.set_footer(text=f'Player\'s Handbook, page {info.page}.')
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SRDCog(bot))
    log.debug('Loaded')
