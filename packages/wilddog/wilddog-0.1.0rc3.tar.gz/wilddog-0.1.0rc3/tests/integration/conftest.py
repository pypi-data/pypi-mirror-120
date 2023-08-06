from typing import List

import flask
import pytest
from _pytest import fixtures
from click.testing import CliRunner

from tests import helpers
from wilddog.api import app as w
from wilddog.models import metadata


@pytest.fixture()
def app() -> flask.Flask:
    return w.make_app()


@pytest.fixture()
def projects_list(database_init, request: fixtures.SubRequest) -> List[int]:
    fix = helpers.TestDataResourceFixture("projects/list_1.csv", metadata.Project)
    prs: List[int] = fix.pre()
    request.addfinalizer(fix.post)
    return prs


@pytest.fixture(scope="session")
def cli_runner():
    return CliRunner()
