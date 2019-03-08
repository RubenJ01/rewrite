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
        self.rules = {
            1: (
                "No Malicious Behavior.",
                "Do not enter the server with the intent to raid, brigade, or troll. Intentionally malicious users "
                "will be immediately and permanently banned. Come on, people, it’s common sense. "
            ),
            2: (
                "No Obscene Content.",
                "This is a SFW server. Any form of porn/hentai/etc, including links or pics, is forbidden. Erotic "
                "roleplay (ERP) is also strictly prohibited. If you must, take it to PMs and fade to black. "
            ),
            3: (
                "No Spam.",
                "Posting large numbers of superfluous messages for the purposes of cluttering a channel or "
                "artificially boosting server rank is prohibited. Express yourself with quality, not by volume. "
            ),
            4: (
                "No Links.",
                "Posting of outside links has been disabled in most channels due to malicious user behaviour.  If you "
                "would like to post a link and cannot, ping (@) an online member of Staff and we will be happy to "
                "assist. "
            ),
            5: (
                "No Advertising.",
                "Refrain from advertising your own content (YouTube, Twitch, Discord, Social Media, etc) in a public "
                "channel without written permission from the Staff. Exceptions may be made if it is specifically "
                "related to the channel and discussion you are in (e.g.: if you are an artist in #music-arts-crafts; "
                "answering a question in #player-help; if you have been approved for #streaming, etc). That said, "
                "PMing links to other users who have asked for them is permitted. "
            ),
            6: (
                "Be Civil.",
                "You are free to engage in polite discussions and intellectual debates; in fact, we encourage it - "
                "passionate users are the best! However, avoid sliding into public arguments that distract from the "
                "topic. Do not insult or harangue other users, and do not return fire if you are insulted. Do not "
                "engage with trolls: ignore trolling attempts and report them to staff.* "
            ),
            7: (
                "No Bullying.",
                "Banter and teasing are fine, as long as it’s in good fun. However, discrimination or hate speech "
                "based on race, sex, gender, age, or sexuality is unacceptable. Racial slurs are specifically "
                "prohibited. If you are being bullied/harassed (even in PMs), feel free to report it to any member of "
                "Staff.* "
            ),
            8: (
                "Complaints Are Welcome.",
                "If you have a complaint about Staff or user behaviour, you are welcome to PM any online Staff at any "
                "level. If your complaint pertains to a member of Staff, take it one level higher to a Bartender, "
                "Innkeeper or Lord, as appropriate. If possible, bring evidence of misconduct, such as a screenshot, "
                "since it will make our job significantly easier! If the evidence is edited/deleted, contact a Lord, "
                "who can check the Deleted Messages Archive.* "
            ),
            9: (
                "Respect Staff Decisions.",
                "The Staff reserve the right to make decisions at their own discretion. Do not attempt to have one or "
                "more other uninvolved Staff members change or reverse that decision. That said, if you are being "
                "unfairly treated, please bring it to the attention of a higher Staff member, as per Rule 8. Not even "
                "Staff are above the law.* "
            ),
            10: (
                "No Impersonation.",
                "Do not attempt to impersonate server Staff. The job is thankless and the Innkeeper pays us in Copper "
                "Pieces, if at all. Don’t make our lives harder.* "
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
        """Command that contains a list of all the frequently asked questions in the Tavern.
        It allows users to see a list of all the faq questions and it allows them to get their details."""
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

    @is_tavern()
    @command(name='rules')
    async def rules_command(self, ctx, rules_num: int = None):
        """Command that contains a list of all the rules in the Tavern.
        It allows users to see a list of all the rules and it allows them to get their details."""
        rules_embed = Embed(colour=Colour.blurple())
        desc = ''
        if not rules_num or rules_num not in self.rules.keys():
            rules_embed.title = 'The Tavern Rules'
            for num, value in enumerate(self.rules.values()):
                desc += f'**{num + 1}**: {value[0]}\n'
            rules_embed.description = desc
            rules_embed.set_footer(text='Use ;rules {rule_num} to get a specific rule')
            return await ctx.send(embed=rules_embed)
        rules_embed.title = self.rules[rules_num][0]
        rules_embed.description = self.rules[rules_num][1]
        return await ctx.send(embed=rules_embed)


def setup(bot):
    bot.add_cog(TavernCog(bot))
