from discord import Colour, Embed
from discord.ext.commands import Cog, command

from helpers.checks import is_tavern


class TavernCog(Cog, name='Tavern'):

	def __init__(self, bot):
		self.bot = bot
		self.faq = {
			1: (
				"I'm new to Dungeons and Dragons. Where should I start?",
				"Typically, you won't be able to find one-on-one help through DMs. However, the "
				"public #player-help and #dm-help channels to ask any questions you may have. "
				"Youtube series' can also help you out. Several content creators have dedicated "
				"entire playlists to the topic. The Lords recommend the How to Play D&D 5e series "
				"from Don’t Stop Thinking: https://www.youtube.com/watch?v=OoW2CDgztKY&list=PLJmF"
				"JXf3BXjwXkNFo_-iwtHb24AuJcXqx\n"
				"There are also multiple resources listed in #resources, which can be searched "
				"through."
			),
			2: (
				"Where can I find a session to join? Do you run games here?",
				"Yes, we do run our own sessions. You can find requests posted under #party-up, "
				"along with a format for those advertisements found within #party-up-talk.\n"
				"Currently, we are in the process of recruiting official DMs, known as the "
				"Queen's Guard, with the intention of establishing a regular weekly session.\n"
				"If you would like to interview for the Guard, please PM a Captain."
			),
			3: (
				"Is there anything else that you do here?",
				"Yes! Despite most of our traffic being related to 5th Edition D&D, all tabletop "
				"games, and most video games, are welcome as well. For now, you can find these in "
				"#other-rpgs-talk and #video-gaming."
			),
			4: (
				"Why can't I post images or embed links?",
				"Due to malicious user activity, links and images have been heavily restricted in "
				"many parts of the server. If you want to post a relevant link, ask a member of "
				"Staff and we will be happy to assist you."
			),
			5: (
				"Where can I find [thing]? What is [channel] for?",
				"You can find most relevant information within #tavern-menu."
			),
			6: (
				"Can I run a game here?",
				"Of course! You may advertise your games in #party-up, no permissions necessary. "
				"Just follow the format provided within the pins and you're home free. However, we "
				"we do recommend that you apply for the Queen's Guard, the group of our approved "
				"DMs within the Tavern server. You can apply for this position by PMing a Captain "
				"of the Queen's Guard."
			),
			7: (
				"...how do I apply for staff here?",
				"Staff applications are currently closed.\n"
				# split is intentionally done so that it can be spotted in a crowd to change quickly
				"As most rosters often do, the Staff roster is prone to change. If you would like "
				"to show your interest in becoming a staff member, feel free to fill out the "
				"application for the Advisors role, which can be found within #announcements.\n"
				"Remember, we always are on the lookout for those with regular activity in the "
				"server who show kindness, consideration, and helpfulness "
			),
			8: (
				"What is the Hall of Fame?",
				"The Hall of Fame is just that - a hall of fame for those users who have "
				"distinguished themselves from the crowd in some way. Users who are particularly "
				"funny, helpful, knowledgeable, clearheaded, or otherwise may one day find that "
				"the staff have voted to give them a golden hero’s crest."
			),
		}

	@command(name='tavern_help', aliases=['thelp'])
	async def tavern_help(self, ctx, cmd: str = "None"):
		"""Enables users to request help for the various server-specific commands.
		This command should return all commands with basic descriptions on each if another isn't
		called, or should return helpful information for the command that is."""
		thelp_embed = Embed(
			colour=Colour.blurple()
		)
		cmd = self.bot.get_command(cmd)
		if not cmd:
			tavern_cog = self.bot.get_cog('Tavern')
			for _command in tavern_cog.get_commands():
				thelp_embed.add_field(
					name=_command.name,
					# ugly because library errors
					value=_command.help.split('\n\n')[0],
					inline=False)
			return await ctx.send(embed=thelp_embed)

		thelp_embed.title = cmd.name
		thelp_embed.description = cmd.help
		thelp_embed.add_field(name='Usage', value=cmd.usage)
		if cmd.aliases:
			thelp_embed.add_field(name='Aliases', value=', '.join(cmd.aliases))
		return await ctx.send(embed=thelp_embed)

	@is_tavern()
	@command(name='faq')
	async def faq_command(self, ctx, faq_num: int = None):
		faq_embed = Embed(colour=Colour.blurple())
		desc = ''
		if not faq_num or faq_num not in self.faq.keys():
			faq_embed.title = 'Frequently Asked Questions'
			for num, value in enumerate(self.faq.values()):
				desc += f'**{num + 1}**: {value[0]}\n'
			faq_embed.description = desc
			faq_embed.set_footer(text='Use ;faq {faq_num} to get a specific FAQ')
			return await ctx.send(embed=faq_embed)
		faq_embed.title = self.faq[faq_num][0]
		faq_embed.description = self.faq[faq_num][1]
		return await ctx.send(embed=faq_embed)


def setup(bot):
	bot.add_cog(TavernCog(bot))
