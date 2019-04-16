import logging
import random
import yaml
from pathlib import Path

from discord import Colour, Embed, Member
from discord.ext.commands import Cog, command
from discord.utils import get

from utils.checks import is_tavern

GREET_FILE = Path('resources') / 'tavern' / 'greetings.txt'  # messages for new Tavern members
FAQ_FILE = Path('resources') / 'tavern' / 'faq.yaml'  # Tavern FAQ
RULES_FILE = Path('resources') / 'tavern' / 'rules.yaml'  # Tavern rules
RP_RULES_FILE = Path('resources') / 'tavern' / 'rp_rules.yaml'  # Tavern roleplaying rules
log = logging.getLogger('bot.' + __name__)


class TavernCog(Cog, name='Tavern'):
    """These are all of the commands used in The Tavern."""
    def __init__(self, bot):
        self.bot = bot
        self.announcement_role_id = bot.config['tavern']['announcement_role_id']
        self.all_faq = self.load_faq()
        self.rules = self.load_rules()
        self.rprules = self.load_rprules()

    def load_faq(self):
        with open(FAQ_FILE, encoding='utf-8') as faq_file:
            all_faq = yaml.safe_load(faq_file)
        return all_faq

    def load_rules(self):
        with open(RULES_FILE, encoding='utf-8') as faq_file:
            rules = yaml.safe_load(faq_file)
        return rules

    def load_rprules(self):
        with open(RP_RULES_FILE, encoding='utf-8') as faq_file:
            rprules = yaml.safe_load(faq_file)
        return rprules

    @Cog.listener()
    async def on_member_join(self, member: Member):
        """Send a custom greeting to new members of The Tavern."""
        if member.guild.id in self.bot.config['tavern']['guilds']:
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
        else:
            log.debug(f'Not sending greeting to new member {member} of {member.guild}')

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
        no_of_faq = [i for i in range(1, len(self.all_faq) + 1)]
        embed = Embed()
        embed.colour = Colour.blurple()
        if faq_num is None or faq_num not in no_of_faq:
            if faq_num is not None and faq_num not in no_of_faq:
                embed.title = f'FAQ no.{faq_num} does not exist!\nThe following FAQs are:'
            else:
                embed.title = "Frequently Asked Questions"

            embed.description = ''
            for index, faq in enumerate(self.all_faq, start=1):
                embed.description += f'**{index}**. {faq["q"]}\n'
            embed.set_footer(text='Use ;faq {faq_num} to get a specific FAQ')
        else:
            faq = self.all_faq[faq_num - 1]
            embed.title = faq['q']
            embed.description = ''
            for faq_desc in faq['a']:
                embed.description += faq_desc
        await ctx.send(embed=embed)

    @is_tavern()
    @command(name='rules', aliases=['rule'])
    async def rules(self, ctx, rule_num: int = None):
        """Command that contains a list of all the rules in the Tavern.
        It allows users to see a list of all the rules and it allows them to get their details."""
        rule_type = 'rules'
        title = 'The Tavern Rules'
        embed = self.any_rules_embed(rule_num, rule_type, title)
        await ctx.send(embed=embed)

    @is_tavern()
    @command(name='rprules', aliases=['rprule'])
    async def rp_rules(self, ctx, rule_num: int = None):
        """Command that contains a list of all the rprules for Eden.
        It allows users to see a list of all the rprules and it allows them to get their details."""
        rule_type = 'rprules'
        title = 'Roleplaying Rules for Eden'
        embed = self.any_rules_embed(rule_num, rule_type, title)
        await ctx.send(embed=embed)

    def any_rules_embed(self, rule_num, rule_type, title):
        embed = Embed()
        embed.colour = Colour.blurple()
        if rule_num is None or rule_num not in list(getattr(self, rule_type)):
            if rule_num is not None and rule_num not in list(getattr(self, rule_type).keys()):
                embed.title = f'{rule_type[0:-1].capitalize()} no.{rule_num} does not exist!\n'
                embed.title += 'The following {title} are:'
            else:
                embed.title = title
            embed.description = ''
            for key, value in getattr(self, rule_type).items():
                embed.description += f'**{key}**. {value["rule"]}\n'
            embed.set_footer(text='Use ;rules {rule_num} to get a specific rule')
        else:
            embed.title = list(getattr(self, rule_type).values())[rule_num - 1]['rule']
            embed.description = ''
            for exp in list(getattr(self, rule_type).values())[rule_num - 1]['explanation']:
                embed.description += exp
        return embed

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
                    f'**We do not allow pay to play services**' \

        final = str.casefold(formattype)
        if final == 'resources':
            await ctx.send(resources)
        if final == 'party-up':
            await ctx.send(partyup)

    @is_tavern()
    @command(name='sub', aliases=['subscribe'])
    async def add_role(self, ctx):
        """
        This command adds the announcement role.
        """
        user = ctx.author
        if self.announcement_role_id not in [role.id for role in ctx.message.author.roles]:
            announcement_role = get(ctx.guild.roles, id=self.announcement_role_id)
            await user.add_roles(announcement_role)
            await ctx.send("The Announcements role has been added.")
        else:
            await ctx.send("You already have the Announcements role.")

    @is_tavern()
    @command(name="unsub", aliases=['unsubscribe'])
    async def remove_role(self, ctx):
        """
        This command removes the announcements role.
        """
        user = ctx.author
        if self.announcement_role_id not in [role.id for role in ctx.message.author.roles]:
            await ctx.send("You do not have the Announcements role.")
        else:
            announcement_role = get(ctx.guild.roles, id=self.announcement_role_id)
            await user.remove_roles(announcement_role)
            await ctx.send("The Announcements role has been successfully removed.")


def setup(bot):
    bot.add_cog(TavernCog(bot))
    log.debug('Loaded')
