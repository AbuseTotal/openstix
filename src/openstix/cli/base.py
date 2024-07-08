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
@click.option("--dataset", default=None, help="Download the specified dataset from the provider.")
@click.option("--all", "download_all", is_flag=True, default=False, help="Download all available providers.")
@click.pass_context
def download(ctx, provider, dataset, download_all):
    if not (provider or download_all):
        click.echo("Error: You must specify either --provider or --all.")
        click.echo()
        click.echo(ctx.get_help())
        ctx.exit(1)

    if dataset and not provider:
        click.echo("Error: You must specify --provider when using --dataset.")
        click.echo()
        click.echo(ctx.get_help())
        ctx.exit(1)

    utils.process(provider, dataset)


@datasets.command(help="Sync datasets to a TAXII server or a directory.")
@click.option("--source", required=True, help="The source dataset to sync.")
@click.option("--sink", required=True, help="The TAXII server or directory to sync to.")
def sync(source, sink):
    utils.sync(source, sink)


cli.add_command(datasets)
