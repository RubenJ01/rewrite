import logging

from discord.ext.commands import Cog, command

log = logging.getLogger('bot.' + __name__)


class SpecialCog(Cog, name='Special'):

    def __init__(self, bot):
        self.bot = bot

    @command(name='invite')
    async def invite_command(self, ctx):
        """Invite the bot to your discord server."""
        log.debug('Sending an invite link for the bot')
        await ctx.send('https://discordapp.com/oauth2/authorize?client_id=506541896630403080&scope=bot&permissions=0')

    @command(name='status')
    async def status_command(self, ctx):
        """Get the current status of the bot."""
        log.debug('Sending the bot status.')
        members = len(list(self.bot.get_all_members()))
        servers = len(self.bot.servers)
        strmembers = str(members)
        strservers = str(servers)
        await ctx.send(f'Bot up and running in {strservers} servers with {strmembers} members.')


def setup(bot):
    bot.add_cog(SpecialCog(bot))
    log.debug('Loaded')
