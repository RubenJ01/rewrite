import asyncio

from sqlalchemy_aio import ASYNCIO_STRATEGY

from sqlalchemy import create_engine, exc
from sqlalchemy.schema import CreateTable

from utils.database import guild_settings, subreddits


async def main():
    engine = create_engine(
        # In-memory sqlite database cannot be accessed from different
        # threads, use file.
        'sqlite:///tavern.db', strategy=ASYNCIO_STRATEGY
    )

    # Create the table

    # await engine.execute(CreateTable(guild_settings))
    await engine.execute(CreateTable(subreddits))

    conn = await engine.connect()

    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
