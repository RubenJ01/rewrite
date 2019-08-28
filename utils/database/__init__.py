from sqlalchemy import (
    Column, BigInteger, MetaData, Table, Text, String)

# Store all tables here.

metadata = MetaData()

guild_settings = Table(
    'guild_settings', metadata,
    Column('guild_id', BigInteger, primary_key=True),
    Column('prefix', String(10)),
)

subreddits = Table(
    'subreddits', metadata,
    Column('guild_id', BigInteger, primary_key=True),
    Column('subreddit_names', Text)
)
