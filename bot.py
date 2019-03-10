import datetime
import logging
import random
from os import environ
from pathlib import Path

from discord import __version__ as discver, Activity, ActivityType
from discord.ext.commands import Bot
from discord.utils import get

from helpers.helpers import prefix

GREETFILE = Path('resources') / 'greetings.txt'  # messages for new members
LOGDIR = Path('logs')


def setup_logger() -> logging.Logger:
    """Create and return the master Logger object."""
    LOGDIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logfile = LOGDIR / f'{timestamp}.log'
    logger = logging.getLogger(__name__)  # the actual logger instance
    logger.setLevel(logging.DEBUG)  # capture all log levels
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)  # log levels to be shown at the console
    file_log = logging.FileHandler(logfile)
    file_log.setLevel(logging.INFO)  # log levels to be written to file
    formatter = logging.Formatter('{asctime} - {name} - {levelname} - {message}', style='{')
    console_log.setFormatter(formatter)
    file_log.setFormatter(formatter)
    logger.addHandler(console_log)
    logger.addHandler(file_log)
    return logger


log = setup_logger()
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
    log.info(f"Connected as {bot.user}, using discord.py {discver}")


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
