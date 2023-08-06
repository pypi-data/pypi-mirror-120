from click.testing import CliRunner
from pkg_resources import get_distribution

import wilddog
from wilddog import cli

VERSION = get_distribution(wilddog.__name__).version


def test_get_version(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli.script, ["--version"])
    assert result.exit_code == 0
    assert f"version {VERSION}" in result.output
