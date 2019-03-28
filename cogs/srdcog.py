import logging

# from discord import Colour, Embed
from discord.ext.commands import Cog, command

from backends.srd import srd

log = logging.getLogger('bot.' + __name__)


class SRDCog(Cog, name='SRD Information'):
    def __init__(self, bot):
        self.bot = bot

    @command(name='spell')
    async def spell_command(self, ctx, *request):
        request = ' '.join(request).lower()
        log.debug(f'spell command called with request: {request}')
        if len(request) <= 2:
            return await ctx.send('Request too short.')
        matches, truncated = srd.search('spells', 'name', request)
        if len(matches) == 0:
            return await ctx.send(f'Couldn\'t find any spells that match \'{request}\'.')
        if len(matches) > 1:
            spell_names = [match['name'] for match in matches]
            return await ctx.send(f'Could be any of {spell_names}.')
        match = matches[0]
        spell_name = match['name']
        return await ctx.send(f'The spell you wanted is {spell_name}.')


def setup(bot):
    bot.add_cog(SRDCog(bot))
    log.debug('Loaded')
