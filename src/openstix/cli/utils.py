from pathlib import Path

import requests

from openstix import OPENSTIX_PATH, providers
from openstix.toolkit.exceptions import DataSourceError
from openstix.toolkit.sinks import FileSystemSink
from openstix.utils import parse


def get_datasets():
    datasets = []

    for provider_name in dir(providers):
        if provider_name.startswith("_"):
            continue

        provider = getattr(providers, provider_name)

        for dataset_name in dir(provider):
            if dataset_name.startswith("_") or dataset_name.islower():
                continue

            dataset = getattr(provider, dataset_name)
            datasets.append(dataset)

    return datasets


def download(provider=None):
    for dataset in get_datasets():
        if provider and dataset.config.provider != provider:
            continue

        for url in dataset.config.urls:
            response = requests.get(url)

            print(f"Processing {url}")

            if not response.ok:
                print(f"Failed to download {url}")
                continue

            bundle = parse(response.text, allow_custom=True)

            path = Path(OPENSTIX_PATH) / dataset.config.provider / dataset.config.name
            path.mkdir(parents=True, exist_ok=True)

            repository = FileSystemSink(
                stix_dir=path,
                allow_custom=True,
            )

            for stix_object in bundle.objects:
                if isinstance(stix_object, dict):
                    continue

                try:
                    repository.add(stix_object)
                except DataSourceError as e:
                    print(f"{e}. Skipping ...")
