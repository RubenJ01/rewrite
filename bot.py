import datetime
import logging
import yaml

from pathlib import Path

from discord import __version__ as discver, Activity, ActivityType
from discord.ext.commands import Bot

CONFIG_FILE = Path('config.yaml')
LOGDIR = Path('logs')

startup_extensions = ['cogs.taverncog',
                      'cogs.generatorcog',
                      'cogs.rollingcog',
                      'cogs.specialcog',
                      'cogs.srdcog',
                      'cogs.reddit'
                      ]


# Set up logging
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


# Load configuration
try:
    with open(CONFIG_FILE, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)
except:  # noqa: E722
    log.exception(f'Could not load configuration from {CONFIG_FILE}')

# Use configuration to start the bot
# TODO: dynamic per-server prefixes using utils.helpers.prefix
bot = Bot(
    activity=Activity(
        name=f'{config["prefix"]}help | D&D 5e',
        type=ActivityType.watching
    ),
    command_prefix=config['prefix'],
    pm_help=True
)

bot.remove_command('help')
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

    bot.run(config['token'])


if __name__ == '__main__':
    main()
