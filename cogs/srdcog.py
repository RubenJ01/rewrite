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
        """Give information on a spell by name."""
        # TODO: Handle spells that exceed Discord embed size limits, like Imprisonment
        request = ' '.join(request).lower()
        log.debug(f'spell command called with request: {request}')
        if len(request) <= 2:
            return await ctx.send('Request too short.')
        matches, truncated = srd.search('spells', 'name', request, trunc=0)
        if len(matches) == 0:
            return await ctx.send(f'Couldn\'t find any spells that match \'{request}\'.')
        spell_names = [match.name for match in matches]
        spell_names_lower = [match.name.lower() for match in matches]
        # guard against instances where request is an exact match of one result but also
        # part of another match, e.g. 'mass heal' and 'mass healing word'
        if len(matches) > 1 and request not in spell_names_lower:
            return await ctx.send(f'Could be: {", ".join(spell_names)}.')
        if request not in spell_names_lower:
            spell = matches[0]
        else:
            spell = matches[spell_names_lower.index(request)]
        description = f'*{spell.subhead}*\n{spell.description}'
        if spell.higher_levels is not None:
            description += f'\n\u2001**At Higher Levels. **' + spell.higher_levels
        embed = Embed(title=spell.name,
                      colour=PHB_COLOUR,
                      description=description)
        embed.add_field(name="Casting Time", value=spell.casting_time, inline=True)
        embed.add_field(name="Range", value=spell.casting_range, inline=True)
        embed.add_field(name="Components", value=spell.components, inline=True)
        embed.add_field(name="Duration", value=spell.duration, inline=True)
        embed.set_footer(text=f'Player\'s Handbook, page {spell.page}.')
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SRDCog(bot))
    log.debug('Loaded')
