from abc import ABC

from pydantic import BaseModel
from stix2 import MemoryStore

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
