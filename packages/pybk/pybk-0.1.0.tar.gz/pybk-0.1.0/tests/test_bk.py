import pytest

from click.testing import CliRunner

from bk import cli


@pytest.fixture
def fix():
    return "Fixture"


def test_1(fix):
    print(fix)


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "Starting bookmarks..." in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
