import datetime
import logging

from discord import Colour, Embed
from discord.ext.commands import Bot, Cog, command

from utils.checks import is_admin

log = logging.getLogger('bot.' + __name__)


class SpecialCog(Cog, name='Special'):
    """These are all the commands that don't fit into any of the other categories."""
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='invite')
    async def invite_command(self, ctx):
        """Invite the bot to your discord server."""
        log.debug('Sending an invite link for the bot.')
        invite_embed = Embed(colour=Colour.blurple())
        invite_embed.title = 'Invite link for The Tavern Bot'
        invite = self.bot.config['invite']
        invite_embed.description = invite
        invite_embed.set_footer(text='Use ;help to get a list of available commands.')
        await ctx.send(embed=invite_embed)

    @is_admin()
    @command(name='status')
    async def status_command(self, ctx):
        """Get the current status of the bot."""
        log.debug('Sending the bot status.')
        status_embed = Embed(colour=Colour.blurple())
        status_embed.title = 'Status'
        members = len(list(self.bot.get_all_members()))
        guilds = self.bot.guilds
        ids = self.bot.config['adminIDs']
        if ctx.author.id in ids:
            guild_names = 'The Bot is running in the following Guilds:\n'
            for guild in guilds:
                guild_names += '**' + str(guild) + '** , '
            guild_names = guild_names[:-3] + '.'
        else:
            guild_names = ''
        uptime = datetime.datetime.now() - self.bot.start_time
        uptime = datetime.timedelta(days=uptime.days, seconds=uptime.seconds)
        date = 'Created on 18-11-2018'
        status_embed.description = f'Bot up and running in {len(guilds)} guilds with {members} members.\n'
        status_embed.description += f'\nUptime: {uptime}\n{date}'
        status_embed.description += '\n\n' + guild_names
        status_embed.set_footer(text='Use ;help to get a list of available commands.')
        log.debug(status_embed.description)
        await ctx.send(embed=status_embed)

    @command(name='basic')
    async def basic_rules(self, ctx):
        """Link to the basic rulebook for d&d 5e."""
        log.debug('Sending the basic rules.')
        basic_embed = Embed(colour=Colour.blurple())
        basic_embed.title = 'Basic rulebook for d&d 5e.'
        basic_embed.description = 'http://media.wizards.com/2018/dnd/downloads/DnD_BasicRules_2018.pdf'
        basic_embed.set_footer(text='Use ;help to get a list of available commands.')
        await ctx.send(embed=basic_embed)

    @command(name='help')
    async def new_help(self, ctx, second_help: str = None):
        """
        Show this message
        """
        embed = Embed()
        embed.title = ':regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p: '
        embed.colour = 0x68c290
        cmd_names = []
        for cmd in self.bot.commands:
            cmd_names.append(cmd.name)

        cogs = []
        cogs_dict = self.bot.cogs
        for k in cogs_dict.keys():
            cogs.append(k)
        cogs.sort()
        cogs.remove('Tavern')
        cogs.remove('ErrorHandler')
        if second_help is None:
            for cog_name in cogs:
                cog = self.bot.get_cog(cog_name)
                commands = cog.get_commands()
                message = f'{cog.description}\nCommands under this category:\n**'
                for cmd in commands:
                    message += ';' + cmd.name + '\n'
                embed.add_field(name=cog_name, value=message + '**', inline=False)
            embed.set_footer(text="Use .help {category}/{command} for more information.")
        else:
            cogs_lowercase = [cog.lower() for cog in cogs]
            if second_help in cogs_lowercase:
                index = cogs_lowercase.index(second_help)
                cog = self.bot.get_cog(cogs[index])
                commands = cog.get_commands()
                message = f'{cog.description}\nCommands under this category:\n**'
                for cmd in commands:
                    message += '.' + cmd.name + '\n'
                embed.add_field(name=cogs[index], value=message + '**', inline=False)
            elif second_help.lower() in cmd_names:
                cmd = self.bot.get_command(second_help)
                embed.add_field(name=cmd.name, value=cmd.help, inline=False)
                value = ''
                if cmd.aliases:
                    for alias in cmd.aliases:
                        value += f'{str(alias)}, '
                    value = value[0:-2]
                    value = value + '.'
                else:
                    value = None
                embed.add_field(name="Aliases", value=f'*{value}*', inline=False)
                params_list = list(cmd.params.keys())
                req_params = []
                for value in params_list:
                    req_params.append(value)
                req_params.remove('self')
                req_params.remove('ctx')
                param_message = 'Required parameters are:\n**'
                if req_params:
                    for parm in req_params:
                        param_message += parm + '\n'
                    embed.add_field(name='Usage', value=param_message + '**', inline=False)
                else:
                    embed.add_field(name='Usage', value=param_message + 'None**', inline=False)

            else:
                return await ctx.send(f"{str(second_help)} command/category does not exist!")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SpecialCog(bot))
    log.debug('Loaded')
