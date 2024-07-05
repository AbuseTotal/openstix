import os
import tempfile
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal
from zipfile import ZipFile

from pydantic import BaseModel
from stix2 import MemoryStore
import requests
from pydantic import BaseModel
from stix2 import Bundle
from tqdm import tqdm

from openstix.constants import OPENSTIX_PATH
from openstix.filters import Filter
from openstix.toolkit import Environment
from openstix.toolkit.exceptions import DataSourceError
from openstix.toolkit.sinks import FileSystemSink
from openstix.toolkit.sources import DataSource


class SourceConfig(BaseModel):
    type: Literal["github_api", "json", "zip"]
    url: str
    paths: list[str] = None


class DatasetConfig(BaseModel):
    name: str
    sources: list[SourceConfig]


class ProviderConfig(BaseModel):
    name: str
    datasets: list[DatasetConfig]


class Downloader(ABC):
    def __init__(self, provider: str, config: SourceConfig):
        self.url = config.url

        provider_path = Path(OPENSTIX_PATH) / provider
        provider_path.mkdir(parents=True, exist_ok=True)

        self.sink = FileSystemSink(
            stix_dir=provider_path,
            allow_custom=True,
        )

    @abstractmethod
    def process(self):
        pass

    def save(self, bundle: Bundle) -> None:
        try:
            self.sink.add(bundle)
        except DataSourceError as e:
            print(f"{e}. Skipping ...")


class JSONDownloader(Downloader):
    def process(self) -> Bundle:
        response = requests.get(self.url, stream=True)

        if not response.ok:
            print(f"Failed to download JSON from {self.url}")
            return

        total_size = int(response.headers.get("content-length", 0))
        chunk_size = 1024

        with tempfile.NamedTemporaryFile(delete=False, mode="w+b") as temp_file:
            for chunk in tqdm(
                response.iter_content(chunk_size=chunk_size),
                total=total_size // chunk_size,
                unit="kB",
                unit_divisor=1024,
                miniters=1,
                desc="Downloading JSON",
            ):
                temp_file.write(chunk)

            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            bundle = self.save(content)
            return bundle
        finally:
            os.remove(temp_file_path)


class GitHubFolderDownloader(Downloader):
    def process(self):
        pass


class ZIPDownloader(Downloader):
    def __init__(self, provider: str, config: SourceConfig):
        self.root = Path(OPENSTIX_PATH) / "tmp" / str(uuid.uuid4())
        self.files_path = Path(self.root) / "files"

        self.root.mkdir(parents=True, exist_ok=True)
        self.files_path.mkdir(parents=True, exist_ok=True)

        self.zip_path = Path(self.root) / "original.zip"
        self.content_paths = config.paths

        super().__init__(provider, config)

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
            zip_ref.extractall(path=self.files_path)

    def _load(self):
        folder = [f for f in self.files_path.iterdir() if f.is_dir()][0]

        for content_path in self.content_paths:
            content_path = self.files_path / folder / content_path

            for file in content_path.iterdir():
                if not file.is_file():
                    continue

                with file.open("r") as fp:
                    self.save(fp.read())


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


SOURCE_CONFIGS_MAPPING = {
    "json": JSONDownloader,
    "github_api": GitHubFolderDownloader,
    "zip": ZIPDownloader,
}
