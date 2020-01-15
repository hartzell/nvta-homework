# -*- coding: utf-8 -*-


def lift_cli(mapping_file, query_file):
    """Lift the transcript locations onto the genome.

    Lifts the transcript locations from the query file onto the
    genome, using the mappings from the mapping file and print the
    results in Invitae Standard Homework Format(tm).
    """
    print('Mapping queries in {0} using mapping in {1}'.format(
        query_file, mapping_file))
