import logging
import random
from pathlib import Path

from discord import Colour, Embed, Member
from discord.ext.commands import Cog, command
from discord.utils import get

from helpers.checks import is_tavern

GREET_FILE = Path('resources') / 'tavern_greetings.txt'  # messages for new Tavern members

log = logging.getLogger('bot.' + __name__)


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
        self.rprules = {
            1: (
                "No ERP.",
                "Any evidence of erotic roleplay will be punished, to allow as many players as possible to take part "
                "in and enjoy the roleplaying experience here, we need to keep this age appropriate; any descriptions "
                "of characters based purely on sexual characteristics are deemed inappropriate. Sexual harassment or "
                "misbehaviour will result in an instant RP Ban. "
            ),
            2: (
                "Respect.",
                "Just treat fellow players with common decency, don't be cruel to anyone, especially if they're "
                "asking for advice, at the same time, we understand that debates can break out but when they do keep "
                "in mind that you are on a public platform and it's disrespectful to other players to be having large "
                "debates. "
            ),
            3: (
                "Keep OOC, OOC.",
                "Out of character content should stay limited to the out of character channel, any content posted in "
                "main hall and the other roleplaying channels should be deleted, and if you have to declare the "
                "result from a roll or request another player make a roll just use the recommended format laid out "
                "later on in the document. "
            ),
            4: (
                "Approved Characters.",
                "Please understand that in order to avoid any chaos created from having waves of unbalanced or unfair "
                "characters you need to wait to have your character sheet approved by a Roleplay DM. To get your "
                "character approved make sure you follow the character creation rules as laid out later on in the "
                "document. "
            ),
            5: (
                "Leave the DMing to the DMs.",
                "Unless you ask a Roleplay DM, please leave DMing to the DMs; If there is an arc event going on and "
                "you need a DM to help keep things going or make an event occur, just hop into an out of character "
                "channel and ping the Roleplay DM you need or do a role ping for any Roleplay DM to come in. "
            ),
            6: (
                "Avoid Spotlighting.",
                "We understand you want your character to have a strong personality and that you want your character "
                "to have character, but to keep things fair please avoid spotlighting (Trying to steal all the focus "
                "on a scene) unless it's a specific arc that really is all about you, and even then, best to stay "
                "respectful of your fellow players. "
            ),
            7: (
                "Common Sense.",
                "Unless any events spark new rules to be written here, that should be all the basic rules we need, "
                "just use your common sense, be respectful, and remember to enjoy yourself while keeping things "
                "enjoyable for others! "
            ),
            8: (
                "RTFM.",
                "Head on over here to the Public Google Drive for The Tavern and read the Player's Manual, "
                "known as Rosegrove's Journal of Eden, once you've done that check out our stuff in the Rules, "
                "Homebrew, and Resources folders, including such hits as Poisons, Mousefolk, Alchemists, "
                "and much much more! https://drive.google.com/open?id=1IwfCygfjoQXQ5flXxeWbeG6pSgkBKC-V "
            ),
        }

    @is_tavern()
    @Cog.listener()
    async def on_member_join(self, member: Member):
        """Send a custom greeting to new members of The Tavern."""
        log.debug(f'Sending greeting to new Tavern member {member}')
        with open(GREET_FILE, 'r', encoding='utf-8') as f:
            strings = f.readlines()
        greeting = random.choice(strings)
        message = 'Welcome to The Tavern, ' + member.mention + '. ' + greeting
        channel = get(member.guild.channels, name='general')
        if channel is not None:
            await channel.send(message)
        else:
            log.warning(f'Could not send greeting to {member} in guild {member.guild}: no #general')

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
            thelp_embed.set_footer(text='Use ;tavern_help {command} to get info on a specific command.')
            return await ctx.send(embed=thelp_embed)

        thelp_embed.title = cmd.name
        thelp_embed.description = cmd.help
        thelp_embed.add_field(name='Usage', value=cmd.usage)
        thelp_embed.set_footer(text='Use ;tavern_help {command} to get info on a specific command.')
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

    @is_tavern()
    @command(name='rprules')
    async def rprules_command(self, ctx, rprules_num: int = None):
        """Command that contains a list of all the rprules for Eden.
        It allows users to see a list of all the rprules and it allows them to get their details."""
        rprules_embed = Embed(colour=Colour.blurple())
        desc = ''
        if not rprules_num or rprules_num not in self.rprules.keys():
            rprules_embed.title = 'Roleplaying Rules for Eden'
            for num, value in enumerate(self.rprules.values()):
                desc += f'**{num + 1}**: {value[0]}\n'
            rprules_embed.description = desc
            rprules_embed.set_footer(text='Use ;rprules {rprule_num} to get a specific rule')
            return await ctx.send(embed=rprules_embed)
        rprules_embed.title = self.rprules[rprules_num][0]
        rprules_embed.description = self.rprules[rprules_num][1]
        return await ctx.send(embed=rprules_embed)

    @is_tavern()
    @command(name='format')
    async def format_command(self, ctx, formattype=None):
        """Command that contains the formatting for some of the channels such as party-up."""
        log.debug(f'loading format for {formattype}')
        format_embed = Embed(colour=Colour.blurple())
        formats = ['party-up', 'resources']
        desc = ''
        num = 0
        if formattype not in formats:
            format_embed.title = 'All of the format Commands'
            for _ in formats:
                desc += f'**{formats[num]}** \n'
                num = num + 1
            format_embed.description = desc
            format_embed.set_footer(text='Use ;format {command} to use one of the above commands.')
            return await ctx.send(embed=format_embed)

        partyup = f'**Format for when posting in #party-up, always stick to this when posting here:** \n' \
                  f'```' \
                  f'Type: lfp (looking for players), lfg (looking for group), lfdm (looking for DM). \n' \
                  f'Game: the game type you are playing in or looking to play in: 3.5e, 5e etc. \n' \
                  f'Platform: platform used to play d&d on such as: discord, roll20 etc... \n' \
                  f'Date and time: time, date and availability for either the player or the dm. \n' \
                  f'Info: a brief campaign description or some information about your character and anything in ' \
                  f'between. \n' \
                  f'```' \

        resources = f'**Format for when posting in #resources, always stick to this when posting here:** \n' \
                    f'```' \
                    f'Creator: who created the resource? \n' \
                    f'Geared for: for who is this resource helpfull? \n' \
                    f'Format: what is the format of the resource? (blog, website etc..) \n' \
                    f'Name: what is the name of the resource? \n' \
                    f'Link: a link to the resource. \n' \
                    f'```' \

        final = str.casefold(formattype)
        if final == 'resources':
            await ctx.send(resources)
        if final == 'party-up':
            await ctx.send(partyup)

    @is_tavern()
    @command(name='role')
    async def role_command(self, ctx):
        role_embed = Embed(colour=Colour.blurple())
        guild = '546007130902233088'
        role_names = [i.name for i in ctx.guild.roles]
        num = 0
        desc = 0
        for _ in role_names:
            desc = f'{role_names[num]} \n'
            num = num + 1
        role_embed.description = desc
        role_embed.title = 'All of the server roles.'
        await ctx.send(embed=role_embed)





def setup(bot):
    bot.add_cog(TavernCog(bot))
    log.debug('Loaded')
