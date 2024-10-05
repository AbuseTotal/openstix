import uuid
from pathlib import Path
from zipfile import ZipFile

import requests
from tqdm import tqdm

from openstix.constants import DEFAULT_OPENSTIX_PATH

from .base import BaseDownloader


class ZIPDownloader(BaseDownloader):
    def __init__(self, *args, **kwargs):
        self.root = Path(DEFAULT_OPENSTIX_PATH) / "tmp" / str(uuid.uuid4())
        self.files_path = Path(self.root) / "files"

        self.root.mkdir(parents=True, exist_ok=True)
        self.files_path.mkdir(parents=True, exist_ok=True)

        self.zip_path = Path(self.root) / "original.zip"

        super().__init__(*args, **kwargs)

    def process(self):
        self._download()
        self._extract()
        self._load()

    def _download(self):
        with requests.get(self.config.url, stream=True) as r:
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

        for content_path in self.config.paths:
            content_path = self.files_path / folder / content_path

            for file in content_path.iterdir():
                if not file.is_file():
                    continue

                with file.open("r") as fp:
                    self.save(fp.read())
