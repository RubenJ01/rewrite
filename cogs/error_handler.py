import logging
import math

from discord.ext import commands


log = logging.getLogger('bot.' + __name__)


class CommandErrorHandler(commands.Cog, name='ErrorHandler'):
    """A error handler for the tavern bot!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Activates when a command opens an error"""
        if isinstance(error, commands.CommandNotFound):
            log.debug(f'{ctx.author} used {ctx.message.content} but no command was found.')
            await ctx.send("The command does not exist!")

        elif isinstance(error, commands.UserInputError):
            log.debug(f'{ctx.author} used {ctx.command} but arguments passed were invalid.')
            await ctx.send("Invalid arguments! please try again.")

        elif isinstance(error, commands.CommandOnCooldown):
            log.debug(f'{ctx.author} used {ctx.command} but was on cooldown.')
            remaining_minutes, remaining_seconds = divmod(error.retry_after, 60)
            return await ctx.send(
                "This command is on cooldown, please retry in "
                f"{int(remaining_minutes)} minutes {math.ceil(remaining_seconds)} seconds."
            )

        elif isinstance(error, commands.TooManyArguments):
            log.debug(f'{ctx.author} used {ctx.command} but arguments passed were many.')
            await ctx.send("Too many arguments were passed! Please try again.")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
    log.debug("CommandErrorHandler cog loaded")
