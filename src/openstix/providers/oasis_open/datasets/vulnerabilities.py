from openstix.filters import Filter
from openstix.providers._base import Dataset


class Vulnerabilities(Dataset):
    def vulnerabilities(self) -> list:
        filters = [Filter("type", "=", "vulnerability")]
        return self._query(filters)

    def vulnerability(self, value=None):
        value = value.upper()
        filters = [
            Filter("type", "=", "vulnerability"),
            Filter("external_references.external_id", "=", value),
        ]
        return self._query_one(filters)
