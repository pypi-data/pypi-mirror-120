import logging

import click
import waitress

from wilddog import VERSION, config
from wilddog.alembic import migration
from wilddog.api import app

logger: logging.Logger = logging.getLogger(__name__)


@click.group()
@click.version_option(VERSION)
def script() -> None:
    """Entry script"""
    logger.info("Welcome to Wild Dog command line")


@script.command(name="echo", help="Simple ping functionality")
def echo() -> None:
    logger.info("Echo requested")


@script.command(name="start", help="Start application server")
def start_server() -> None:
    flask_app = app.make_app()

    # migrate database
    migration.migrate_to_head()
    waitress.serve(
        flask_app,
        host=config.wild_dog.server["host"],
        port=config.wild_dog.server["port"],
        url_scheme=config.wild_dog.server["scheme"],
        threads=config.wild_dog.server["threads"],
    )
