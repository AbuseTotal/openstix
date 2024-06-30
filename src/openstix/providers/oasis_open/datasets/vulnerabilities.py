from openstix.filters import Filter
from openstix.providers._base import Dataset, DatasetConfig


class Vulnerabilities(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="vulnerabilities",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/vulnerability",
        ],
    )

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
