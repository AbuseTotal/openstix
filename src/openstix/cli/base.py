import click

from openstix.cli import utils


@click.group()
def cli():
    """Command line interface for OpenSTIX."""
    pass


@click.group(help="Datasets operations.")
def datasets():
    pass


@datasets.command(help="Download datasets from STIX providers.")
@click.option("--provider", default=None, help="Download the specified provider.")
@click.option("--all", "download_all", is_flag=True, default=False, help="Download all available providers.")
@click.pass_context
def download(ctx, provider, download_all):
    if not (provider or download_all):
        click.echo("Error: You must specify either --provider or --all.")
        click.echo()
        click.echo(ctx.get_help())
        ctx.exit(1)

    utils.download(provider)


cli.add_command(datasets)
