import datetime
import logging
import yaml

from pathlib import Path
from os import environ

from discord import __version__ as discver, Activity, ActivityType
from discord.ext.commands import Bot

from utils.helpers import prefix

CONFIG_FILE = Path('config.yaml')
LOGDIR = Path('logs')

startup_extensions = ['cogs.taverncog',
                      'cogs.generatorcog',
                      'cogs.rollingcog',
                      'cogs.specialcog',
                      'cogs.srdcog',
                      ]


def setup_logger() -> logging.Logger:
    """Create and return the root Logger object for the bot."""
    LOGDIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    logfile = LOGDIR / f'{timestamp}.log'
    logger = logging.getLogger('bot')  # the actual logger instance
    logger.setLevel(logging.DEBUG)  # capture all log levels
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)  # log levels to be shown at the console
    file_log = logging.FileHandler(logfile)
    file_log.setLevel(logging.DEBUG)  # log levels to be written to file
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

bot.start_time = datetime.datetime.now()


@bot.event
async def on_ready():
    log.info(f"Connected as {bot.user}, using discord.py {discver}")


def main():
    """Load cogs, configuration, and start the bot."""
    for extension in startup_extensions:
        try:
            log.debug(f'Loading extension: {extension}')
            bot.load_extension(extension)
        except:  # noqa: E722
            log.exception(f'Failed to load extension: {extension}')

    try:
        with open(CONFIG_FILE, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
        bot.run(config['token'])
    except:  # noqa: E722
        log.exception(f'Could not load configuration from {CONFIG_FILE}')
        log.debug(f'Falling back to environment variable for token')
        bot.run(environ.get('DISCORD_BOT_SECRET'))


if __name__ == '__main__':
    main()
