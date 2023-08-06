from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from wilddog import config as c
from wilddog.models import metadata  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from wilddog.models.base import BaseEntity

config = context.config  # type: ignore
postgres_uri = c.wild_dog.database["url"]

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseEntity.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run alembic in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = postgres_uri
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run alembic in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = config.attributes.get("connection", None)
    if connectable is None:
        cfg = config.get_section(config.config_ini_section)
        cfg["sqlalchemy.url"] = postgres_uri
        connectable = engine_from_config(cfg, prefix="sqlalchemy.", poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
