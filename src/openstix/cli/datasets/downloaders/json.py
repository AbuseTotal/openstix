import os
import tempfile

import requests
from tqdm import tqdm

from .base import BaseDownloader


class JSONDownloader(BaseDownloader):
    def process(self):
        response = requests.get(self.config.url, stream=True)

        if not response.ok:
            print(f"Failed to download JSON from {self.config.url}")
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

            self.save(content)
        finally:
            os.remove(temp_file_path)
