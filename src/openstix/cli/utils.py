import inspect

from openstix import providers


def get_configs():
    configs = []

    for _, provider in inspect.getmembers(providers, inspect.ismodule):
        if not hasattr(provider, "config"):
            continue

        configs.append(provider.config.CONFIG)

    return configs


def process(provider=None, dataset=None):
    for config in get_configs():
        if provider and provider != config.name:
            continue

        for dataset_config in config.datasets:
            if dataset and dataset != dataset_config.name:
                continue

            for source in dataset_config.sources:
                downloader = providers.SOURCE_CONFIGS_MAPPING.get(source.type)
                downloader(config.name, source).process()
