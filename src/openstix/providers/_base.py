from abc import ABC

from pydantic import BaseModel

from openstix.filters import Filter
from openstix.toolkit import Environment
from openstix.toolkit.sources import DataSource


class DatasetConfig(BaseModel):
    name: str
    provider: str
    urls: list[str]


class Dataset(ABC):
    config: DatasetConfig

    def __init__(self, source: DataSource):
        self.environment = Environment(source=source)

    def _query(self, filters=None):
        filters = filters if filters else []
        return self.environment.query(filters)

    def _query_one(self, filters=None):
        filters = filters if filters else []

        objects = self._query(filters)

        if objects:
            return objects[0]

        return None

    def _query_name_and_alias(self, filters, name, aliases=True):
        filters += [Filter("name", "=", name)]

        if aliases:
            filters += [Filter("aliases", "contains", name)]

        return self._query_one(filters)
