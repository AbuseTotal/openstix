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

    # def _parse(self, data):
    #     bundle = parse(data, allow_custom=True)
    #     self.environment.add(bundle.objects)
    #     self._check_not_supported_objects()

    # def _check_not_supported_objects(self):
    #     for obj in self.environment.query():
    #         if isinstance(obj, dict):
    #             print(f"Unsupported object type: {obj.type}")

    def _query(self, filters=None, revoked=False):
        filters = filters if filters else []

        if not revoked:
            not_revoked_filter = Filter("revoked", "=", False)
            filters.append(not_revoked_filter)

        return self.environment.query(filters)

    def _query_one(self, filters=None, revoked=False):
        filters = filters if filters else []

        objects = self._query(filters, revoked=revoked)

        if objects:
            return objects[0]

        return None

    def _query_name_and_alias(self, filters, name, aliases=True, revoked=False):
        filters += [Filter("name", "=", name)]

        if aliases:
            filters += [Filter("aliases", "contains", name)]

        return self._query_one(filters, revoked=False)
