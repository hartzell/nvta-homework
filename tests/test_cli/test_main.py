# -*- coding: utf-8 -*-

from nvta_homework.main import main


def test_cli(cli_runner):
    """Test simple invocation of lift subcommand."""
    result = cli_runner.invoke(main, ['lift', '--mf', 'foo', '--qf', 'bar'])
    assert result.exit_code == 0
