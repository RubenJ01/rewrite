import asyncio
from datetime import datetime
import logging
import json
from pathlib import Path

from discord import Colour, Embed, File
from discord.ext.commands import Cog

import utils.database as tables
from utils.database.db_functions import db_edit, backup_database


log = logging.getLogger('bot.' + __name__)


class Events(Cog, name="Events"):
    """A cog to handle all events."""
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        self.used_commands = {}

    async def backup_background_task(self):
        """Backup database and send the backup file in channel every 24 hours"""
        await self.bot.wait_until_ready()
        while True:
            await self.send_file()
            await asyncio.sleep(24*60*60)

    async def send_file(self):
        """Sends backup db file to channel"""
        guild = self.bot.get_guild(546007130902233088)
        channel = guild.get_channel(622835562516054028)
        p = Path("utils", "database", "backup.txt")
        await backup_database()
        await channel.send(content=f"**{datetime.utcnow()} UTC**", file=File(fp=p.open()))

    @Cog.listener()
    async def on_guild_join(self, guild):
        """Run this function when the bot joins a guild."""
        code = tables.guild_settings.insert().values()
        data = {
            'guild_id': guild.id,
            'prefix': self.config["prefix"]
        }
        await db_edit(code, data)
        tavern_support = self.bot.get_guild(546007130902233088)
        channel = tavern_support.get_channel(573945620482490378)
        await channel.send(f'**{guild.name}** guild has invited the Tavern Bot.')

        embed = Embed(color=Colour.blue())
        embed.title = "Tavern bot"
        p = Path("resources", "json", "bot_join.json")
        with p.open() as file:
            json_data = json.load(file)
        join_message = json_data["join_message"]
        embed.description = join_message
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=embed)
                break

    @Cog.listener()
    async def on_guild_remove(self, guild):
        """Run this function when the bot has been removed from a guild."""
        table = tables.guild_settings
        guild_id = guild.id
        code = table.delete().where(table.c.guild_id == guild_id)
        await db_edit(code)
        tavern_support = self.bot.get_guild(546007130902233088)
        channel = tavern_support.get_channel(573945620482490378)
        await channel.send(f'**{guild.name}** guild has removed the Tavern Bot.')

    @Cog.listener()
    async def on_command(self, ctx):
        """A command tracker.Notifies the team when a command is used."""
        cmd = str(ctx.command)
        if cmd in self.used_commands:
            self.used_commands[cmd] += 1
        else:
            self.used_commands[cmd] = 1
        tavern_support = self.bot.get_guild(546007130902233088)
        channel = tavern_support.get_channel(620668994151776256)
        await channel.send(f"**{cmd}** used by **{ctx.author}** in guild **{ctx.guild.name}.**")


def setup(bot):
    loop = asyncio.get_event_loop()
    loop.create_task(Events(bot).backup_background_task())
    bot.add_cog(Events(bot))
    log.debug("Events cog loaded.")
