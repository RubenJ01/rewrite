from sqlalchemy import (
    Column, BigInteger, MetaData, Table, String)

# Store all tables here.

metadata = MetaData()

guild_settings = Table(
    'guild_settings', metadata,
    Column('guild_id', BigInteger, primary_key=True),
    Column('prefix', String(10)),
)
