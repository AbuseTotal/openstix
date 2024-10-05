from pathlib import Path

import click

from openstix.constants import DEFAULT_OPENSTIX_PATH

from .download import get_datasets_names, get_providers_names


@click.group(name="datasets", help="Datasets operations.")
def cli():
    pass


@cli.command(help="Download datasets from STIX providers.")
@click.option(
    "--provider",
    default=None,
    type=click.Choice(get_providers_names()),
    help="Download the specified provider.",
)
@click.option(
    "--datasets",
    default=None,
    type=click.Choice(get_datasets_names()),
    multiple=True,
    help="Download the specified datasets.",
)
@click.option(
    "-d",
    "--directory",
    required=False,
    default=DEFAULT_OPENSTIX_PATH,
    type=click.Path(),
    help="Directory to store the datasets downloaded",
)
@click.pass_context
def download(ctx, provider, datasets, directory):
    if datasets and provider is None:
        click.echo("Error: You must specify --provider when using --datasets.")
        click.echo()
        click.echo(ctx.get_help())
        ctx.exit(1)

    directory = Path(directory)

    if datasets and provider:
        valid_datasets = get_datasets_names(provider)

        for dataset in datasets:
            if dataset not in valid_datasets:
                raise click.BadParameter(
                    f"Dataset '{dataset}' is not available for provider '{provider}'. "
                    f"Available datasets: {', '.join(valid_datasets)}"
                )

    from .download import process

    process(directory, provider, datasets)


@cli.command(
    help="Sync datasets to a TAXII server or a directory.",
)
@click.option(
    "--source",
    required=True,
    help="The source dataset to sync.",
)
@click.option(
    "--sink",
    required=True,
    help="The TAXII server or directory to sync to.",
)
@click.option(
    "--send-bundle", is_flag=True, help="Send all objects as a single bundle to the sink instead of individual objects."
)
def sync(source, sink, send_bundle):
    from .sync import process

    process(source, sink, send_bundle)
