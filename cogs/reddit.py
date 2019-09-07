import asyncio
import logging
import random
import discord

from collections import deque

from discord.ext import commands

from sqlalchemy import update
from utils.database.db_functions import guild_subreddits, db_edit, db_query, cache_subreddits
import utils.database as tables


log = logging.getLogger('bot.' + __name__)


class DndReddit(commands.Cog, name='D&D Reddit'):
    """Fetches reddit posts."""
    def __init__(self, bot):
        self.bot = bot
        self.subreddits = bot.config['reddit']['subreddits']
        self.img_cache = deque(maxlen=10)
        self.cache_clear_task = bot.loop.create_task(self.clear_cache())
        self.default_subreddits = bot.config['reddit']['subreddits']

    async def clear_cache(self):
        self.img_cache.clear()
        await asyncio.sleep(43200)  # clear cache every 12 hours

    async def fetch(self, session, url):
        params = {
            'limit': 50
        }
        headers = {
            'User-Agent': 'Iceman'
        }

        async with session.get(url=url, params=params, headers=headers) as response:
            return await response.json()

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

    @commands.command(name='reddit')
    async def get_reddit(self, ctx, subreddit='dndmemes'):
        """
        Fetch reddit posts by using this command.
        Gets a post from r/dndmemes by default.
        """
        subreddit_list = []
        subreddit = subreddit.lower()
        for guild in guild_subreddits:
            if guild["guild_id"] == ctx.guild.id:
                current_guild = guild
                subreddits = current_guild["subreddits"]
                subreddit_list = subreddits.split(",")
                break

        if subreddit not in self.subreddits and subreddit not in subreddit_list:
            await ctx.send("Subreddit forbidden")
            await ctx.send("Use the subreddit view command to see avilable subreddits.")
            return await ctx.send_help("subreddit")

        session = self.bot.aiohttp_session
        data = await self.fetch(session, f'https://www.reddit.com/r/{subreddit}/hot/.json')

        try:
            posts = data["data"]["children"]
        except KeyError:
            return await ctx.send('Subreddit not found!')
        if not posts:
            return await ctx.send('No posts available!')

        upvote = self.bot.get_emoji(self.bot.config['reddit']['upvote_emoji_id'])
        downvote = self.bot.get_emoji(self.bot.config['reddit']['downvote_emoji_id'])
        comment = self.bot.get_emoji(self.bot.config['reddit']['comment_emoji_id'])
        while True:
            post = random.choice(posts)
            imageURL = post['data']['url']
            if imageURL in self.img_cache:
                continue
            self.img_cache.append(imageURL)
            break
        embed = discord.Embed()
        embed.colour = 0xf9f586
        embed.title = post['data']['title']
        embed.description = post['data']['selftext'][0:50]
        embed.set_image(url=imageURL)

        embed.description += f'\n**{post["data"]["ups"]}** {upvote} '
        embed.description += f'**{post["data"]["downs"]}** {downvote} '
        embed.description += f'\n**{post["data"]["num_comments"]}** {comment} '

        embed.set_footer(text=f'Posted by {post["data"]["author"]} in r/{subreddit}.')
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        embed.url = post['data']['url']

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DndReddit(bot))
    log.debug('Loaded')
