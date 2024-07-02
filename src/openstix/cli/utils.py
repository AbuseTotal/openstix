import inspect

from openstix import providers
from openstix.providers._base import Dataset


def get_dataset_classes():
    dataset_classes = []
    for _, provider in inspect.getmembers(providers, inspect.ismodule):
        if not hasattr(provider, "datasets"):
            continue

        for _, dataset in inspect.getmembers(provider.datasets):
            if inspect.isclass(dataset) and issubclass(dataset, Dataset) and dataset is not Dataset:
                dataset_classes.append(dataset)

    return dataset_classes


def process(provider=None, dataset=None):
    for dataset_class in get_dataset_classes():
        if not hasattr(dataset_class, "config"):
            continue

        if provider and provider != dataset_class.config.provider:
            continue

        if dataset and dataset != dataset_class.config.name:
            continue

        for downloader in dataset_class.config.downloaders:
            downloader.process()
