from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path
from typing import DefaultDict
from zipfile import ZipFile

import requests
from stix2 import Bundle
from tqdm import tqdm

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
    grouped_urls = defaultdict(list)

    for item in get_datasets():
        if provider and item.config.provider != provider:
            continue

        if dataset and item.config.name != dataset:
            continue

        for url in item.config.urls:
            if url.startswith("https://raw.github"):
                bundle = process_json_url(url)
                save_to_repository(bundle, item)
            else:
                process_grouped_url(url, grouped_urls)

    for repo_url, target_dirs in grouped_urls.items():
        print(f"Processing {repo_url}")

        bundle = process_url(repo_url, target_dirs)

        save_to_repository(bundle, item)


def process_grouped_url(url: str, grouped_urls: DefaultDict) -> Bundle:
    base_url, repo_and_path = url.split("/repos/", 1)
    repo_url = f"{base_url}/repos/{repo_and_path.split('/contents/')[0]}/zipball/main"
    target_dir = repo_and_path.split("/", 3).pop(3)
    grouped_urls[repo_url].append(target_dir)


def process_url(url: str, target_dirs: list[str]) -> list[Bundle]:
    """Resolve URLs, handling potential redirects and API responses."""
    response = requests.get(url, stream=True)

    if not response.ok:
        print(f"Failed to download ZIP from {url}")
        return []

    chunk_size = 1024 * 1024
    downloaded = 0

    with BytesIO() as zip_buffer:
        for chunk in tqdm(
            response.iter_content(chunk_size=chunk_size),
            unit_scale=True,
            unit="MB",
            unit_divisor=1024,
            miniters=1,
            desc="Downloading ZIP",
        ):
            zip_buffer.write(chunk)
            downloaded += len(chunk)

        zip_buffer.seek(0)
        with ZipFile(zip_buffer) as zip_file:
            root_dir = zip_file.namelist()[0].split("/")[0]
            target_dirs_set = {f"{root_dir}/{target_dir}/" for target_dir in target_dirs}

            extracted_objects = []
            files_to_process = [
                file_info
                for file_info in zip_file.infolist()
                if any(
                    file_info.filename.startswith(target_dir) and file_info.filename.endswith(".json")
                    for target_dir in target_dirs_set
                )
            ]

            with ThreadPoolExecutor() as executor:
                future_to_file = {
                    executor.submit(process_file, zip_file, file_info): file_info.filename
                    for file_info in files_to_process
                }

                for future in as_completed(future_to_file):
                    try:
                        stix_obj = future.result()
                        if stix_obj:
                            extracted_objects.append(stix_obj)
                    except Exception as e:
                        print(f"Failed to parse content from {future_to_file[future]}: {e}")

            return Bundle(objects=[obj for bundle in extracted_objects for obj in bundle.objects])


def process_json_url(url: str) -> Bundle:
    """Download a JSON file from a URL and parse it."""
    print(f"Processing {url}")
    response = requests.get(url)

    if not response.ok:
        print(f"Failed to download JSON from {url}")
        return Bundle()

    return parse(response.text, allow_custom=True)


def process_file(zip_file: ZipFile, file_info) -> Bundle:
    """Process a single file from the zip archive."""
    with zip_file.open(file_info) as file:
        content = file.read().decode("utf-8")
        try:
            return parse(content, allow_custom=True)
        except Exception as e:
            print(f"Failed to parse content from {file_info.filename}: {e}")
            return None


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
