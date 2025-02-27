import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
# from core.config import get_settings  # Import database settings
from db.database import Base , DATABASE_URL # Import your SQLAlchemy models
# from domains.blog_management.models import Blog, BlogCategory, BlogTag

# Alembic Config object, which provides access to values in .ini file
config = context.config

print(f"\n\nAlembic is using database URL: {DATABASE_URL}\n\n")


config.set_main_option("sqlalchemy.url", DATABASE_URL)  # Set DB URL

# Set up logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Import models for autogenerate support
target_metadata = Base.metadata

print(f"\n\nTarget Metadata: {target_metadata.tables.keys()}\n\n")


# Create an async database engine
engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(sync_conn):
    """Configure context and run migrations with a sync connection."""
    context.configure(connection=sync_conn, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode using the existing async engine."""
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations) 

    await engine.dispose()





# async def run_migrations_online():
#     """Run migrations in 'online' mode with async support."""
#     async with engine.begin() as conn:
#         await conn.run_sync(context.run_migrations)

#     await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())  # Run migrations asynchronously
