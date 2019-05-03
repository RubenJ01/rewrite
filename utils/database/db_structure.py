import asyncio

from sqlalchemy_aio import ASYNCIO_STRATEGY

from sqlalchemy import (
    Column, BigInteger, MetaData, Table, String, create_engine)
from sqlalchemy.schema import CreateTable


metadata = MetaData()

guild_settings = Table(
    'guild_settings', metadata,
    Column('guild_id', BigInteger, primary_key=True),
    Column('prefix', String(10)),
)


async def main():
    engine = create_engine(
        # In-memory sqlite database cannot be accessed from different
        # threads, use file.
        'sqlite:///tavern.db', strategy=ASYNCIO_STRATEGY
    )

    # Create the table
    await engine.execute(CreateTable(guild_settings))

    conn = await engine.connect()

    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
