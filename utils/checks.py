from discord.ext.commands import check

# TODO: move constants into config, and make config available here.
dev_team = (
    263560579770220554,
    391583287652515841,
    98529562597523456,
    98694745760481280
)
tavern_guilds = (
    362589385117401088,
    546007130902233088,
    546007130902233090
)


def is_tavern():
    def predicate(ctx):
        if ctx.guild.id not in tavern_guilds:
            return False
        return True
    return check(predicate)


def is_admin():
    def predicate(ctx):
        if ctx.author.id not in dev_team:
            return False
        return True
    return check(predicate)
