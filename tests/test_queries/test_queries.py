# -*- coding: utf-8 -*-

import pytest

from nvta_homework.queries import Queries


# Table driven test, each entry in the table includes:
# - the name of the query file
# - the number of queries expected in that file
# - the expected values for that sample (transcript name, position)
@pytest.mark.parametrize(('queries_file', 'count', 'expected'), [
    (
        'sample_data/queries.tsv',
        4,
        [
            ['TR1', 4],
            ['TR2', 0],
            ['TR1', 13],
            ['TR2', 10],
        ],
    ),
    ('/dev/null', 0, []),
])
def test_successful_loading(queries_file, count, expected):
    """Test the query reader."""
    queries = Queries()
    queries.read_tsv(queries_file)
    assert len(queries.queries) == count
    for query in queries.queries:
        exp = expected.pop(0)
        assert query.transcript_name == exp[0]
        assert query.pos == exp[1]


@pytest.mark.parametrize(('queries_file', 'exception'), [
    (
        'nonexistent.tsv',
        r'^.*No such file or directory.*$',
    ),
    (
        'sample_data/queries_bad_rows.tsv',
        r'^.*Bad number of columns.*$',
    ),
])
def test_loading(queries_file, exception):
    """Test the query reader with bad data."""
    queries = Queries()
    with pytest.raises(Exception) as e_info:
        queries.read_tsv(queries_file)
        assert e_info.match(exception)
