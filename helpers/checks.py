from discord.ext.commands import check


def is_tavern():
    def predicate(ctx):
        if not ctx.guild.id in (362589385117401088, 546007130902233088):
            return False
        return True
    return check(predicate)
