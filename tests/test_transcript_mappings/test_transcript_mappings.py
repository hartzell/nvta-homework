# -*- coding: utf-8 -*-

import pytest

from nvta_homework.transcript_mappings import TranscriptMappings


# Table driven test, each entry in the table includes:
# - the name of the transcript mapping file to read
# - the count of expected transcript mappings
# - a list of lists of transcript mapping values (names, pos, cigar string)
@pytest.mark.parametrize(('mapping_file', 'count', 'expected'), [
    (
        'sample_data/transcript_mapping.tsv',
        2,
        [['TR1', 'CHR1', 3, '8M7D6M2I2M11D7M'], ['TR2', 'CHR2', 10, '20M']],
    ),
    ('/dev/null', 0, []),
])
def test_successful_loading(mapping_file, count, expected):
    """Test the mapping reader."""
    mappings = TranscriptMappings()
    mappings.read_tsv(mapping_file)
    assert len(mappings.mappings) == count
    for tr_name in mappings.mappings.keys():
        tm = expected.pop(0)
        assert mappings.mappings[tr_name].transcript_name == tm[0]
        assert mappings.mappings[tr_name].chromosome_name == tm[1]
        assert mappings.mappings[tr_name].start == tm[2]
        assert mappings.mappings[tr_name].cigar == tm[3]


@pytest.mark.parametrize(('mapping_file', 'exception'), [
    (
        'nonexistent.tsv',
        r'^.*No such file or directory.*$',
    ),
    (
        'sample_data/transcript_mapping_bad_rows.tsv',
        r'^.*Bad number of columns.*$',
    ),
    (
        'sample_data/transcript_mapping_bad_cigar.tsv',
        r'^.*Unexpected alignment character: Q.*$',
    ),
    (
        'sample_data/tm_multiple_mapping.tsv',
        r'^.*Multiple mappings for TR1.*$',
    ),
])
def test_failures_while_loading(mapping_file, exception):
    """Test the mapping reader with bad data."""
    mappings = TranscriptMappings()
    with pytest.raises(Exception) as e_info:
        mappings.read_tsv(mapping_file)
        assert e_info.match(exception)
