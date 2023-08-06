from os import path
from pathlib import Path

import pytest
from _pytest import fixtures

from wilddog.alembic import migration
from wilddog.models import transactions

here = Path(path.abspath(path.dirname(__file__)))
root = here.parent


@pytest.fixture(scope="session")
def settings_file() -> str:
    return f"{root}/wilddog.toml"


@pytest.fixture(scope="session")
def database_init(request: fixtures.SubRequest) -> None:
    engine = transactions.sql_engine()
    migration.upgrade(engine)

    def tear_down():
        migration.downgrade(engine)

    request.addfinalizer(tear_down)
