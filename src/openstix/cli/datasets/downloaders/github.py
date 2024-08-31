import requests

from .base import BaseDownloader


class GitHubFolderDownloader(BaseDownloader):
    def process(self):
        print("Downloading files from GitHub folder")
        response = requests.get(self.config.url)

        if not response.ok:
            print(f"Failed to fetch data from {self.config.url}")
            return

        data = response.json()

        if not isinstance(data, list):
            print(f"Unexpected data format from {self.config.url}")
            return

        download_urls = [item["download_url"] for item in data if "download_url" in item]

        for url in download_urls:
            self.download_file(url)

    def download_file(self, url):
        response = requests.get(url, stream=True)

        if not response.ok:
            print(f"Failed to download file from {url}")
            return

        self.save(response.text)
