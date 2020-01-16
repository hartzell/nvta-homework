# -*- coding: utf-8 -*-

import csv
import re


class TranscriptMappings(object):
    """Model a set of  transcript mapping data."""

    def __init__(self):
        """Set up the object."""
        self.mappings = {}

    _expected_columns = 4

    def read_tsv(self, filename):
        """Read a set of mappings from the tsv file."""
        with open(filename) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                if len(row) != self._expected_columns:
                    raise (Exception('Bad number of columns'))
                tm = TranscriptMapping(*row)
                if tm.transcript_name in self.mappings:
                    raise (Exception('Multiple mappings for {0}'.format(
                        tm.transcript_name)))
                self.mappings[tm.transcript_name] = tm

    def lift(self, t_name, t_pos):
        """Lift the transcript location onto the genome."""
        mapping = self.mappings[t_name]
        chr_pos = self.translocate(t_pos, mapping.start, mapping.cigar)
        return mapping.chromosome_name, chr_pos

    def translocate(self, query_pos, cigar_start, cigar):  # noqa: C901, WPS231
        """Return the genomic location for a query transcript location."""
        alignment = self._cigar_to_alignment(cigar)
        chr_start = cigar_start - 1
        chr_end = chr_start - 1
        tr_pos = -1
        for i in range(0, len(alignment)):  # noqa: WPS111 I'd like to
            # break out when done, but then for loop doesn't complete
            # and coverage test fails.  Sigh....
            if tr_pos == query_pos:
                continue
            if alignment[i] == 'D':
                chr_start += 1
                chr_end = chr_start
            elif alignment[i] == 'I':
                tr_pos += 1
                chr_end = chr_start + 1
            elif alignment[i] == 'M':
                tr_pos += 1
                chr_start += 1
                chr_end = chr_start
            else:
                raise (Exception('Unexpected alignment character: {0}'.format(
                    alignment[i])))
        if chr_start == chr_end:
            return chr_start

        return '{0}^{1}'.format(chr_start, chr_end)

    def _cigar_to_alignment(self, cigar):
        pattern = re.compile(r'([0-9]+)([A-Z]+)')
        alignment = ''
        for (count, op) in re.findall(pattern, cigar):
            alignment += op * int(count)
        return alignment


class TranscriptMapping(object):
    """Model a single transcript mapping."""

    def __init__(self, t_name, c_name, pos, cigar):
        """Initialize the object (mandatory doc strings, you say?)."""
        # TODO: check that these are legal
        self.transcript_name = t_name
        self.chromosome_name = c_name
        self.start = int(pos)
        self.cigar = cigar
