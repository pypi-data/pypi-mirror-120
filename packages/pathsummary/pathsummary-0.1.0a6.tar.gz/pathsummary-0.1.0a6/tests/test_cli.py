from pathlib import Path

from click.testing import CliRunner
from pathsummary import cli
import pytest


def test_basic_summary():
    """
    Test against the work dir, as a basic run.
    """
    cli_runner = CliRunner()
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0


def test_empty_path(tmpdir):
    """
    Test a directory leading to no result to avoid getting
    error messages from the bottom functions, which cannot
    handle emtpy content.
    """
    empty_temporary_dir = Path(tmpdir).joinpath("empty")
    empty_temporary_dir.mkdir()
    cli_runner = CliRunner()
    result = cli_runner.invoke(cli, [str(empty_temporary_dir)])
    assert result.exit_code == 0
    assert result.output == ""


    result = cli_runner.invoke(cli, [str(empty_temporary_dir), "-c"])
    assert result.exit_code == 0
    assert result.output == ""
