from discord.ext.commands import check


def is_tavern():
    def predicate(ctx):
        # TODO: move constants into config, and make config available here.
        if ctx.guild.id not in (362589385117401088, 546007130902233088, 546007130902233090):
            return False
        return True
    return check(predicate)
