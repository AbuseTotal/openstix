import os
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal, Union
from zipfile import ZipFile

from pydantic import BaseModel
from stix2 import MemoryStore
import requests
from pydantic import BaseModel, ConfigDict
from stix2 import Bundle

from openstix.constants import OPENSTIX_PATH
from openstix.filters import Filter
from openstix.toolkit import Environment
from openstix.toolkit.sources import DataSource
from openstix.utils import parse


class JSONSourceConfig(BaseModel):
    type: Literal["json"]
    url: str


class ZIPSourceConfig(BaseModel):
    type: Literal["zip"]
    url: str


class GitHubAPISourceConfig(BaseModel):
    type: Literal["github_api"]
    url: str
    paths: list[str]


class DatasetConfig(BaseModel):
    name: str
    sources: list[Union[JSONSourceConfig, ZIPSourceConfig, GitHubAPISourceConfig]]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ProviderConfig(BaseModel):
    name: str
    datasets: list[DatasetConfig]


class Downloader(ABC):
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def process(self):
        pass

    # def save_bundle(self, bundle: Bundle, dataset: Dataset) -> None:
    #     """Save the STIX objects to the local repository."""
    #     path = Path(OPENSTIX_PATH) / dataset.config.provider / dataset.config.name
    #     path.mkdir(parents=True, exist_ok=True)

    #     repository = FileSystemSink(
    #         stix_dir=path,
    #         allow_custom=True,
    #     )

    #     for stix_object in bundle.objects:
    #         if isinstance(stix_object, dict):
    #             continue

    #         try:
    #             repository.add(stix_object)
    #         except DataSourceError as e:
    #             print(f"{e}. Skipping ...")


class JSONDownloader(Downloader):
    def process(self) -> Bundle:
        response = requests.get(self.url)

        if not response.ok:
            print(f"Failed to download JSON from {self.url}")
            return Bundle()

        return parse(response.text, allow_custom=True)


class GitHubFolderDownloader(Downloader):
    def __init__(self, config: GitHubAPISourceConfig):
        super().__init__()

    def process(self):
        pass


class ZIPDownloader(Downloader):
    def __init__(self, config: JSONSourceConfig):
        self.root = os.path.join(OPENSTIX_PATH, "tmp", str(uuid.uuid4()))

        self.zip_path = os.path.join(self.root, "original.zip")
        self.files_path = os.path.join(self.root, "files")

        self.paths = []
        for content_path in config.paths:
            path = os.path.join(self.files_path, content_path)
            self.paths.append(path)

        Path(self.root).mkdir(parents=True, exist_ok=True)
        Path(self.files_path).mkdir(parents=True, exist_ok=True)

        super().__init__(config.url)

    def process(self):
        self._download()
        self._extract()
        self._load()

    def _download(self):
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            with open(self.zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def _extract(self):
        with ZipFile(self.zip_path, "r") as zip_ref:
            zip_ref.extractall(self.files_path)

    def _load(self):
        for content_path in self.paths:
            _, _, files = next(os.walk(content_path))

            for file in files:
                file_path = os.path.join(content_path, file)

                with open(file_path, "r") as f:
                    print(f"Processing file: {file_path}")
                    print(f.read())  # Replace this with actual processing logic


class Dataset(ABC):
    config: DatasetConfig

    def __init__(self, source: DataSource):
        self.environment = Environment(source=source)
        self.cache = MemoryStore()

    def _query(self, filters=None):
        filters = filters if filters else []
        return self.environment.query(filters)

    def _query_one(self, filters=None):
        filters: list[Filter] = filters if filters else []

        cached_objects = self.cache.query(filters)
        if cached_objects:
            return cached_objects[0]

        objects = self._query(filters)
        if objects:
            obj = objects[0]
            self.cache.add([obj])
            return obj

        return None

    def _query_name_and_alias(self, filters, name, aliases=True):
        filters += [Filter("name", "=", name)]

        if aliases:
            filters += [Filter("aliases", "contains", name)]

        return self._query_one(filters)
