import datetime
import logging
from sqlalchemy import update

from discord import Colour, Embed
from discord.ext import buttons
from discord.ext.commands import Bot, Cog, command, has_permissions, MissingPermissions

from utils.checks import is_admin
from utils.database.db_functions import db_edit, cache_prefixes
import utils.database as tables

log = logging.getLogger('bot.' + __name__)


class Paginator(buttons.Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SpecialCog(Cog, name='Special'):
    """Miscellaneous commands."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = self.bot.config

    @command(name='invite')
    async def invite_command(self, ctx):
        """Invite the bot to your discord server."""
        log.debug('Sending an invite link for the bot to {ctx.guild}.')
        invite_embed = Embed(
            title='Invite link for The Tavern Bot',
            description=self.config['invite'],
            colour=Colour.blurple())
        invite_embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        invite_embed.set_footer(text='Use ;help to get a list of available commands.')
        await ctx.send(embed=invite_embed)

    @command(name='status')
    async def status_command(self, ctx):
        """Get the current status of the bot."""
        status_embed = Embed(
            title='Status',
            colour=Colour.blurple())
        members = len(list(self.bot.get_all_members()))
        uptime = datetime.datetime.now() - self.bot.start_time
        uptime = datetime.timedelta(days=uptime.days, seconds=uptime.seconds)
        date = 'Created on 18-11-2018'
        status_embed.description = '\n'.join(
            [f'Bot up and running in {len(self.bot.guilds)} guilds with {members} members.',
             f'Uptime: {uptime}\n{date}'
             ]
        )
        status_embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        status_embed.set_footer(text='Use ;help to get a list of available commands.')
        await ctx.send(embed=status_embed)

    @command(name='basic', aliases=['srd'])
    async def basic_rules(self, ctx):
        """Link to the basic rulebook for D&D 5e."""
        basic_embed = Embed(
            description='**The basic rules for Dungeons and Dragons can be found at the following link:**\n'
                        'http://media.wizards.com/2018/dnd/downloads/DnD_BasicRules_2018.pdf',
            colour=Colour.blurple())
        basic_embed.set_footer(text='Use ;help to get a list of available commands.')
        await ctx.send(embed=basic_embed)

    @is_admin()
    @command(name='dbappend', hidden=True)
    async def append_to_db(self, ctx):
        """
        Ensures all guilds that the Bot is currently in are added to the Guilds database..
        """
        guilds_added = 0
        db_code = tables.guild_settings.insert().values()
        for g in self.bot.guilds:
            data = {
                'guild_id': g.id,
                'prefix': self.config['prefix']
            }
            db_is_edited = await db_edit(db_code, data)
            if db_is_edited:
                guilds_added += 1
            else:
                pass  # An error is already passed by the db_edit function
        await ctx.send(f'{guilds_added} guilds added to the Guilds database.')

    @has_permissions(manage_guild=True)
    @command(name='prefix')
    async def change_prefix(self, ctx, new_prefix):
        """Use this command to change the prefix of your bot."""
        table = tables.guild_settings
        data = {'prefix': new_prefix}
        db_is_edited = await db_edit(update(table).where(table.c.guild_id == ctx.guild.id).values(), data)
        if db_is_edited:
            await cache_prefixes()
            await ctx.send(f"Prefix has been changed to {new_prefix}")
        else:
            await ctx.send(f"Prefix could not be changed to {new_prefix}")

    @change_prefix.error
    async def on_change_prefix_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            return await ctx.send(f'Could not change the prefix for the server.\n{error}')

    @command(name='help')
    async def help_(self, ctx, second_help: str = None):
        cogs = sorted([cog for cog in self.bot.cogs.keys() if cog not in ['ErrorHandler', 'Tavern']])
        pages = []
        page = 1
        cmd_names = [cmd.name for cmd in self.bot.commands]
        if not second_help:
            for cog_name in cogs:
                cog = self.bot.get_cog(cog_name)
                commands = [cmd for cmd in cog.get_commands() if not cmd.hidden or cmd.name == 'help']
                message = cog.description + '\n'
                for cmd in commands:
                    if cmd.name == 'subreddit':
                        for sub_cmd in cmd.walk_commands():
                            message += f' \n  **{self.config["prefix"]}{sub_cmd}** \n *{sub_cmd.help}*'
                    else:
                        message += f' \n  **{self.config["prefix"]}{cmd}** \n *{cmd.help}*'
                help_embed = Embed(title=cog_name, colour=Colour.blurple(), description=message)
                help_embed.set_footer(text=f'Page: {page}/{len(cogs)}')
                help_embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                pages.append(help_embed)
                page = page + 1
            embed = Paginator(embed=False, timeout=90, use_defaults=True,
                              extra_pages=pages, length=1)
            await embed.start(ctx)
        else:
            if second_help.lower() in cmd_names:
                cmd = self.bot.get_command(second_help)
                embed = Embed(title=cmd.name, colour=Colour.blurple())
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
                embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            else:
                return await ctx.send(f"{str(second_help)} command does not exist!")

    @is_admin()
    @command(name='hiddencmds', aliases=['hiddens'], hidden=True)
    async def show_hidden_commands(self, ctx):
        """View hidden commands."""
        embed = Embed(
            title='Hidden Commands',
            description='\n'.join([f'**{c.name}** - {c.help}' for c in self.bot.commands if c.hidden]),
            colour=0x68c290)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SpecialCog(bot))
    log.debug('Loaded')
