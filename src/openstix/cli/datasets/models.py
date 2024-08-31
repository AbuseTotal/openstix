from enum import Enum

from pydantic import BaseModel


class DataSourceType(str, Enum):
    GITHUB_API = "github_api"
    JSON = "json"
    ZIP = "zip"

    @property
    def downloader(self):
        # Import here to avoid circular import
        from .downloaders import (
            GitHubFolderDownloader,
            JSONDownloader,
            ZIPDownloader,
        )

        mapping = {
            DataSourceType.GITHUB_API.value: GitHubFolderDownloader,
            DataSourceType.JSON.value: JSONDownloader,
            DataSourceType.ZIP.value: ZIPDownloader,
        }

        return mapping.get(self.value, None)


class DataSourceConfig(BaseModel):
    type: DataSourceType
    url: str
    paths: list[str] = None
    ignore_object_types: list[str] = []


class DatasetConfig(BaseModel):
    name: str
    provider: str
    sources: list[DataSourceConfig]
