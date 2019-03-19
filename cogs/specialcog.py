import datetime
import logging

from discord import Colour, Embed
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
        status_embed = Embed(colour=Colour.blurple())
        status_embed.title = 'Status'
        members = len(list(self.bot.get_all_members()))
        guilds = len(self.bot.guilds)
        uptime = datetime.datetime.now() - self.bot.start_time
        uptime = datetime.timedelta(days=uptime.days, seconds=uptime.seconds)
        message = f'Bot up and running in {guilds} guilds with {members} members.'
        message += f'\nUptime: {uptime}'
        status_embed.description = message
        status_embed.set_footer(text='Use ;help to get a list of available commands.')
        log.debug(message)
        await ctx.send(embed=status_embed)


def setup(bot):
    bot.add_cog(SpecialCog(bot))
    log.debug('Loaded')
