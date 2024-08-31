import click

from . import datasets


@click.group()
def cli():
    """Command line interface for OpenSTIX."""
    pass


cli.add_command(datasets.cli)
