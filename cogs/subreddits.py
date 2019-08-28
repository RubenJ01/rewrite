import logging

from sqlalchemy import update

from discord.ext import commands
import discord

from utils.database.db_functions import db_edit, db_query, cache_subreddits
import utils.database as tables


logger = logging.getLogger('bot.' + __name__)


class SubredditList(commands.Cog, name="Subreddit List"):
    """A cog for managing subreddit access in the server."""

    def __init__(self, bot):
        self.bot = bot
        self.default_subreddits = bot.config['reddit']['subreddits']

    @commands.group(name="subreddit", invoke_without_command=True)
    async def subreddit(self, ctx):
        pass

    @subreddit.command(name="enable")
    async def enable_feature(self, ctx):
        """A command to enable specific subreddits feature."""

        code = tables.subreddits.insert().values()
        data = {
            'guild_id': ctx.guild.id,
            'subreddit_names': ""
        }
        result = await db_edit(code, data)
        if result:
            await ctx.send("Feature has been enabled!")
        else:
            await ctx.send("Feature has already been enabled!")

    @subreddit.command(name="add")
    async def add_subreddit(self, ctx, subreddit: str):
        """Add a subreddit so users in the guild can get posts from it."""
        table = tables.subreddits
        row_data = await db_query(table.select().where(table.c.guild_id == ctx.guild.id))
        try:
            subreddits_string = row_data[0][1]
        except IndexError:
            return await ctx.send("This feature is not enabled!")

        if subreddits_string == "":
            new_subreddits = subreddits_string + subreddit + ","

        else:
            subreddit_list = subreddits_string.split(',')
            if subreddit in subreddit_list:
                return await ctx.send(f"Subreddit **{subreddit}** is already present!")
            new_subreddits = subreddits_string + subreddit + ","

        data = {
            'subreddit_names': new_subreddits
        }

        result = await db_edit(update(table).where(table.c.guild_id == ctx.guild.id).values(), data)
        if result:
            await cache_subreddits()
            await ctx.send(f"Subreddit **{subreddit}** has been added!")
        else:
            await ctx.send("fail")

    @subreddit.command(name="remove")
    async def remove_subreddit(self, ctx, subreddit: str):
        """Remove a subreddit from the list of accessible subreddits on the server."""
        table = tables.subreddits
        row_data = await db_query(table.select().where(table.c.guild_id == ctx.guild.id))
        try:
            subreddits_string = row_data[0][1]
        except IndexError:
            return await ctx.send("This feature is not enabled!")

        if subreddits_string == "":
            return await ctx.send("Nothing to remove, list is empty.")

        else:
            subreddit_list = subreddits_string.split(',')
            if subreddit not in subreddit_list:
                return await ctx.send(f"Cannot find subreddit **{subreddit}** in the list!")
            subreddit_list.remove(subreddit)
            new_subreddits = ",".join(subreddit_list)

        data = {
            'subreddit_names': new_subreddits
        }

        result = await db_edit(update(table).where(table.c.guild_id == ctx.guild.id).values(), data)
        if result:
            await cache_subreddits()
            await ctx.send(f"Subreddit **{subreddit}** has been removed!")
        else:
            await ctx.send("fail")

    @subreddit.command(name="view")
    async def view_subreddits(self, ctx):
        """View all avilable subreddits."""
        table = tables.subreddits
        row_data = await db_query(table.select().where(table.c.guild_id == ctx.guild.id))
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = "Accessable Subreddits"

        try:
            subreddits_string = row_data[0][1]
        except IndexError:
            return await ctx.send("This feature is not enabled!")

        if subreddits_string == "":
            embed.description = "There are no added subreddits."

        else:
            subreddit_list = subreddits_string.split(",")
            subreddit_list.pop()

            embed.description = ""
            for i, sr in enumerate(subreddit_list):
                embed.description += f"{i+1}.{sr}\n"

        embed.description += "\n**Default subreddits are:**\n"
        for sr in self.default_subreddits:
            embed.description += f"{sr}\n"
        await ctx.send(embed=embed)


def setup(bot):
    """Load the cog."""
    bot.add_cog(SubredditList(bot))
    logger.debug('Loaded')
