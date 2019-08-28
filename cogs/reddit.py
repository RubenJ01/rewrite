import asyncio
import logging
import random
from collections import deque

import discord
from discord.ext import commands

from utils.database.db_functions import guild_subreddits

log = logging.getLogger('bot.' + __name__)


class DndReddit(commands.Cog, name='D&D Reddit'):
    """Fetches reddit posts."""
    def __init__(self, bot):
        self.bot = bot
        self.subreddits = bot.config['reddit']['subreddits']
        self.img_cache = deque(maxlen=10)
        self.cache_clear_task = bot.loop.create_task(self.clear_cache())

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
        embed.url = post['data']['url']

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DndReddit(bot))
    log.debug('Loaded')
