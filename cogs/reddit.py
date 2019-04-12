import logging
import random

import aiohttp

import discord
from discord.ext import commands

log = logging.getLogger('bot.' + __name__)

DND_SUBREDDITS = [
    'dndmemes',
    'dndiy',
    'dungeons_and_dragons',
    'roll20',
    'unearthedarcana',
    'dndnext',
    'dnd'
]


class DndReddit(commands.Cog, name='D&D Reddit'):
    """These are all the commands that have to do with the reddit part of the bot."""
    def __init__(self, bot):
        self.bot = bot

    async def fetch(self, session, url):
        params = {
            'limit': 25
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
        subreddit = subreddit.lower()

        if subreddit not in DND_SUBREDDITS:
            embed = discord.Embed()
            embed.title = 'Please choose from this list of subreddits:'
            embed.colour = discord.Colour.blue()
            embed.description = '```'

            for sr in DND_SUBREDDITS:
                embed.description += sr + '\n'

            embed.description += '```'
            return await ctx.send(embed=embed)

        session = self.bot.http_session
        data = await self.fetch(session, f'https://www.reddit.com/r/{subreddit}/hot/.json')

        try:
            posts = data["data"]["children"]
        except KeyError:
            return await ctx.send('Subreddit not found!')
        if not posts:
            return await ctx.send('No posts available!')

        upvote = self.bot.get_emoji(565550541137117194)
        downvote = self.bot.get_emoji(565550586146324500)
        comment = self.bot.get_emoji(565577972812349498)
        post = random.choice(posts)

        embed = discord.Embed()
        embed.colour = 0xf9f586
        embed.title = post['data']['title']
        embed.description = post['data']['selftext'][0:50]
        imageURL = post['data']['url']
        embed.set_image(url=imageURL)

        embed.description += f'\n**{post["data"]["ups"]}** {upvote} '
        embed.description += f'**{post["data"]["downs"]}** {downvote} '
        embed.description += f'\n**{post["data"]["num_comments"]}** {comment} '

        embed.set_footer(text=f'Posted by {post["data"]["author"]} in r/{subreddit}.')
        embed.url = post['data']['url']

        await ctx.send(embed=embed)


def setup(bot):
    bot.http_session = aiohttp.ClientSession()
    bot.add_cog(DndReddit(bot))
    log.debug('Reddit cog loaded.')
