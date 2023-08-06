import pkg_resources
from alembic import command, config
from sqlalchemy.engine import Engine

from wilddog.models import transactions


def _alembic_config() -> config.Config:
    """special script for running migration"""

    cfg = config.Config()
    cfg.set_section_option(section="formatters", name="keys", value="generic")
    cfg.set_main_option("script_location", pkg_resources.resource_filename("wilddog", "alembic/"))
    return cfg


def upgrade(engine: Engine, tag: str = "head") -> None:
    """special script for running migration"""

    cfg = _alembic_config()
    with engine.connect() as conn:
        cfg.attributes["connection"] = conn
        command.upgrade(cfg, tag)


def downgrade(engine: Engine, tag: str = "-1") -> None:
    """special script for running migration"""

    cfg = _alembic_config()
    with engine.connect() as conn:
        cfg.attributes["connection"] = conn
        command.downgrade(cfg, tag)


def migrate_to_head() -> None:
    with transactions.Session():
        upgrade(transactions.sql_engine())
