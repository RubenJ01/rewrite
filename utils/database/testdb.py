import asyncio

from sqlalchemy import update

from utils.database.db_functions import db_query, db_edit
import utils.database as tables


async def query():
    table = tables.guild_settings
    result = await db_query(table.select())
    print(result)


async def edit():
    table = tables.guild_settings
    guild_id = 426566445124812813
    # code = table.insert().values()
    code = table.delete().where(table.c.guild_id == guild_id)
    data = {
        'guild_id': guild_id,
    }
    # bool = await db_edit(update(table).where(table.c.guild_id == gid).values(), data)
    result_bool = await db_edit(code)
    print(result_bool)
    await query()

table = tables.guild_settings
code = table.insert().values()
data = {
    'guild_id': 32402486,
    'prefix': 'iceman'
}

loop = asyncio.get_event_loop()
# loop.run_until_complete(edit(code, data))
loop.run_until_complete(edit())