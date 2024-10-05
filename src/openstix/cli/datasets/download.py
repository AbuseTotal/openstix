import inspect

from openstix import providers

from .models import DatasetConfig


def get_dataset_configs(providers):
    configs = []

    for _, provider in inspect.getmembers(providers, inspect.ismodule):
        if not hasattr(provider, "datasets"):
            continue

        for item in provider.datasets.CONFIG:
            config = DatasetConfig(**item)
            configs.append(config)

    return configs


def process(directory, provider=None, datasets=None):
    for config in get_dataset_configs(providers):
        if provider and provider != config.provider:
            continue

        if datasets and config.name not in datasets:
            continue

        print(f"Start processing dataset '{config.name}' from provider '{config.provider}'")
        for source in config.sources:
            source.type.downloader(config.provider, source, directory).run()


def get_providers_names(provider=None):
    configs = get_dataset_configs(providers)
    return list({item.provider for item in configs})


def get_datasets_names(provider=None):
    configs = get_dataset_configs(providers)
    return list({item.name for item in configs if provider is None or provider == item.provider})
