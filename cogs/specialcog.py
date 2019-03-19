import datetime
import logging

from discord.ext.commands import Bot, Cog, command

log = logging.getLogger('bot.' + __name__)


class SpecialCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='invite')
    async def invite_command(self, ctx):
        """Invite the bot to your discord server."""
        log.debug('Sending an invite link for the bot')
        invite = 'https://discordapp.com/oauth2/authorize?client_id=506541896630403080&scope=bot&permissions=0'
        await ctx.send(invite)

    @command(name='status')
    async def status_command(self, ctx):
        """Get the current status of the bot."""
        log.debug('Sending the bot status.')
        members = len(list(self.bot.get_all_members()))
        guilds = len(self.bot.guilds)
        uptime = datetime.datetime.now() - self.bot.start_time
        uptime = datetime.timedelta(days=uptime.days, seconds=uptime.seconds)
        message = f'Bot up and running in {guilds} guilds with {members} members.'
        message += f'\nUptime: {uptime}'
        log.debug(message)
        await ctx.send(message)


def setup(bot):
    bot.add_cog(SpecialCog(bot))
    log.debug('Loaded')
