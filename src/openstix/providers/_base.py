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
from openstix.toolkit.exceptions import DataSourceError
from openstix.toolkit.sinks import FileSystemSink


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
        response = requests.get(self.url)

        if not response.ok:
            print(f"Failed to fetch data from {self.url}")
            return

        data = response.json()

        if not isinstance(data, list):
            print(f"Unexpected data format from {self.url}")
            return

        download_urls = [item["download_url"] for item in data if "download_url" in item]

        for url in download_urls:
            self.download_file(url)

    def download_file(self, url):
        response = requests.get(url, stream=True)

        if not response.ok:
            print(f"Failed to download file from {url}")
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
                desc=f"Downloading {os.path.basename(url)}",
            ):
                temp_file.write(chunk)

            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.save(content)
        finally:
            os.remove(temp_file_path)


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
            total_size = int(r.headers.get("content-length", 0))
            chunk_size = 8192

            with open(self.zip_path, "wb") as f:
                for chunk in tqdm(
                    r.iter_content(chunk_size=chunk_size),
                    total=total_size // chunk_size,
                    unit="kB",
                    unit_divisor=1024,
                    miniters=1,
                    desc="Downloading ZIP",
                ):
                    f.write(chunk)

    def _extract(self):
        with ZipFile(self.zip_path, "r") as zip_ref:
            total_files = len(zip_ref.namelist())
            with tqdm(total=total_files, unit="files", desc="Extracting ZIP") as pbar:
                for file in zip_ref.namelist():
                    zip_ref.extract(file, path=self.files_path)
                    pbar.update(1)

    def _load(self):
        folder = [f for f in self.files_path.iterdir() if f.is_dir()][0]
        total_files = sum(
            1
            for content_path in self.content_paths
            for file in (self.files_path / folder / content_path).iterdir()
            if file.is_file()
        )
        saved_files = 0

        for content_path in self.content_paths:
            content_path = self.files_path / folder / content_path

            for file in content_path.iterdir():
                if not file.is_file():
                    continue

                with file.open("r") as fp:
                    self.save(fp.read())
                    saved_files += 1
                    print(f"Saved {saved_files}/{total_files} files")


SOURCE_CONFIGS_MAPPING = {
    "json": JSONDownloader,
    "github_api": GitHubFolderDownloader,
    "zip": ZIPDownloader,
}
