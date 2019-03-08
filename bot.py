from os import environ

from discord import __version__ as discver, Activity, ActivityType
from discord.ext.commands import Bot

from helpers.helpers import prefix

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


#bot.load_extension('cogs.rollingcog')
bot.load_extension('cogs.taverncog')

bot.run(environ.get('DISCORD_BOT_SECRET'))
