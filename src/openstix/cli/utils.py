from pathlib import Path

import requests

from openstix import OPENSTIX_PATH, providers
from openstix.providers._base import Dataset
from openstix.toolkit.exceptions import DataSourceError
from openstix.toolkit.sinks import FileSystemSink
from openstix.utils import parse


def get_datasets() -> list[Dataset]:
    datasets: list[Dataset] = []

    for provider_name in dir(providers):
        if provider_name.startswith("_"):
            continue

        provider = getattr(providers, provider_name)

        for dataset_name in dir(provider):
            if dataset_name.startswith("_") or dataset_name.islower():
                continue

            dataset: Dataset = getattr(provider, dataset_name)
            datasets.append(dataset)

    return datasets


def download(provider=None, dataset=None):
    for ds in get_datasets():
        if provider and ds.config.provider != provider:
            continue

        if dataset and ds.config.name != dataset:
            continue

        urls = resolve_urls(ds.config.urls)

        for url in urls:
            response = requests.get(url)
            print(f"Processing {url}")

            if not response.ok:
                print(f"Failed to download {url}")
                continue

            bundle = parse(response.text, allow_custom=True)
            save_to_repository(bundle, ds)


def resolve_urls(urls: list[str]) -> list[str]:
    """Resolve URLs, handling potential redirects and API responses."""
    resolved_urls: list[str] = []
    for url in urls:
        if url.startswith("https://raw."):
            resolved_urls.append(url)
        else:
            response = requests.get(url)
            if response.ok:
                for item in response.json():
                    resolved_urls.append(item["download_url"])

    return resolved_urls


def save_to_repository(bundle, dataset: Dataset):
    """Save the STIX objects to the local repository."""
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
