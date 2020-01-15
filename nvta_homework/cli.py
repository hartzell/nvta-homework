# -*- coding: utf-8 -*-

import csv
from sys import stdout

from nvta_homework.queries import Queries
from nvta_homework.transcript_mappings import TranscriptMappings


def lift_cli(mapping_file, query_file):
    """Lift the transcript locations onto the genome.

    Lifts the transcript locations from the query file onto the
    genome, using the mappings from the mapping file and print the
    results in Invitae Standard Homework Format(tm).
    """
    tm = TranscriptMappings()
    tm.read_tsv(mapping_file)
    queries = Queries()
    queries.read_tsv(query_file)
    tsv_writer = csv.writer(stdout, delimiter='\t')
    for query in queries.queries:
        genome_location = tm.lift(query.transcript_name, query.pos)
        tsv_writer.writerow([
            query.transcript_name,
            query.pos,
            genome_location[0],
            genome_location[1],
        ])
