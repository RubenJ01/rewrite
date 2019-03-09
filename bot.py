import random
from os import environ
from pathlib import Path

from discord import __version__ as discver, Activity, ActivityType
from discord.ext.commands import Bot
from discord.utils import get

from helpers.helpers import prefix

GREETFILE = Path('resources') / 'greetings.txt'  # messages for new members

bot = Bot(
    activity=Activity(
        name='.help | D&D 5e',
        type=ActivityType.watching
    ),
    command_prefix=prefix,
    pm_help=True
)


@bot.event
async def on_ready():
    print(f"I'm ready.\n{bot.user}\n{discver}")


@bot.event
async def on_member_join(member):
    if member.guild.id != "362589385117401088":  # The Tavern
        return
    with open(GREETFILE, 'r') as f:
        strings = f.readlines()
    greeting = random.choice(strings)
    message = "Welcome to The Tavern " + member.mention + ". " + greeting
    channel = get(member.guild.channels, name="general")
    await channel.send(message)

# bot.load_extension('cogs.rollingcog')
bot.load_extension('cogs.taverncog')

bot.run(environ.get('DISCORD_BOT_SECRET'))
