# -*- coding: utf-8 -*-

import pytest
from click.testing import CliRunner

from nvta_homework.main import main


def test_cli():
    """Test simple invocation of lift subcommand."""
    mf = 'sample_data/transcript_mapping.tsv'
    qf = 'sample_data/queries_exhaustive.tsv'
    runner = CliRunner()
    result = runner.invoke(main, ['lift', '--mf', mf, '--qf', qf])
    assert result.exit_code == 0
    with open('sample_data/exhaustive_result.tsv') as the_file:
        expected = the_file.read()
        assert result.output == expected


def test_cli_bad_cigar():
    """Test simple invocation of lift subcommand."""
    mf = 'sample_data/transcript_mapping_bad_cigar.tsv'
    qf = 'sample_data/queries_exhaustive.tsv'
    runner = CliRunner()
    with pytest.raises(Exception) as e_info:
        runner.invoke(main, ['lift', '--mf', mf, '--qf', qf])
        assert e_info.match(r'^.*Unexpected alignment character: Q.*$')
