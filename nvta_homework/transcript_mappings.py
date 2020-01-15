# -*- coding: utf-8 -*-

import csv


class TranscriptMappings(object):
    """Model a set of  transcript mapping data."""

    def __init__(self):
        """Set up the object."""
        self.mappings = []

    _expected_columns = 4

    def read_tsv(self, filename):
        """Read a set of mappings from the tsv file."""
        with open(filename) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                if len(row) != self._expected_columns:
                    raise (Exception('Bad number of columns'))
                tm = TranscriptMapping(*row)
                self.mappings.append(tm)


class TranscriptMapping(object):
    """Model a single transcript mapping."""

    def __init__(self, t_name, c_name, pos, cigar):
        """Initialize the object (mandatory doc strings, you say?)."""
        # TODO: check that these are legal
        self.transcript_name = t_name
        self.chromosome_name = c_name
        self.start = int(pos)
        self.cigar = cigar
