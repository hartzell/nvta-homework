# -*- coding: utf-8 -*-

import click

from nvta_homework.cli import lift_cli


@click.group()
def main():
    """Invitae homework CLI."""
    pass  # noqa: WPS420


@main.command()
@click.option('--mf',
              required=True,
              help='The filename of the transcript mapping file')
@click.option('--qf', required=True, help='The filename of the query file')
def lift(mf, qf):
    """Lift transcript locations onto genome.

    Lift the transcript locations in the query_file onto the
    genome, using the transcript<->genome mappings defined in the
    mapping_file.
    """
    lift_cli(mf, qf)


if __name__ == '__main__':
    main()
