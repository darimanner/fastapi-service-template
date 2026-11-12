import asyncio
import logging

from alembic import context
from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.settings import settings
from src.core.db.model import Base

# Import model modules above so autogenerate sees their tables in Base.metadata.

logging.basicConfig(format="%(levelname)s [%(name)s] %(message)s")
logging.getLogger("alembic").setLevel(logging.INFO)


def run_offline() -> None:
    context.configure(
        url=str(settings.database.url),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_with(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_online() -> None:
    engine = create_async_engine(str(settings.database.url), poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(run_with)
    await engine.dispose()


if context.is_offline_mode():
    run_offline()
elif connection := context.config.attributes.get("connection"):
    run_with(connection)
else:
    asyncio.run(run_online())
