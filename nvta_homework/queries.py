# -*- coding: utf-8 -*-

import csv


class Queries(object):
    """Model a set of homework queries."""

    def __init__(self):
        """Set up the object."""
        self.queries = []

    _expected_columns = 2

    def read_tsv(self, filename):
        """Read a set of mappings from the tsv file."""
        with open(filename) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                if len(row) != self._expected_columns:
                    raise (Exception('Bad number of columns'))
                query = Query(*row)
                self.queries.append(query)


class Query(object):
    """Model a single homework query."""

    def __init__(self, t_name, pos):
        """Initialize the object (mandatory doc strings, you say?)."""
        # TODO: check that these are legal
        self.transcript_name = t_name
        self.pos = int(pos)
