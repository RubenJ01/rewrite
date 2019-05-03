import logging

from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy import create_engine

import utils.database as tables


logger = logging.getLogger('bot.'+__name__)


async def db_query(query):
    engine = create_engine(
        'sqlite:///tavern.db', strategy=ASYNCIO_STRATEGY
    )

    conn = await engine.connect()
    try:
        db_query = await conn.execute(query)
        results = await db_query.fetchall()
    except Exception as e:
        logger.error(f'{str(e)} FOR {query}')
        results = None
        return results
    else:
        await conn.close()
        logger.info(f'Db Query: {query}')
        return results


async def db_edit(db_code, data=None):
    engine = create_engine(
        # In-memory sqlite database cannot be accessed from different
        # threads, use file.
        'sqlite:///tavern.db', strategy=ASYNCIO_STRATEGY
    )
    bool = True
    conn = await engine.connect()
    try:
        if data is not None:
            await conn.execute(db_code, data)
        else:
            await conn.execute(db_code)
    except Exception as e:
        bool = False
        logger.error(f'{str(e)} CODE : {db_code} + {data}')
        return bool
    else:
        await conn.close()
        logger.info(f'DbCode: {db_code} + {data}')
        return bool


guild_ids = []
guild_prefixes = []


async def cache_prefixes():
    """Caches all the prefix of all guilds from the database"""
    logger.info("caching prefixes from database...")
    guild_ids.clear()
    guild_prefixes.clear()
    table = tables.guild_settings
    guilds = await db_query(table.select())
    for guild in guilds:
        guild_ids.append(guild[0])
        guild_prefixes.append(guild[1])
    logger.info("caching prefixes from database...DONE")
