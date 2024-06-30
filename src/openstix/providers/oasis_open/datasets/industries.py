from openstix.filters import Filter
from openstix.objects import Identity
from openstix.providers._base import Dataset, DatasetConfig


class Industries(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="industries",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/identity",
        ],
    )

    def search(self, query):
        return self._search(
            [
                Filter("name", "contains", query),
                Filter("description", "contains", query),
                Filter("roles", "contains", query),
                Filter("identity_class", "contains", query),
                Filter("sectors", "contains", query),
                Filter("contact_information", "contains", query),
            ],
        )

    def sectors(self) -> list[Identity]:
        filters = [
            Filter("type", "=", "identity"),
        ]
        return [item for item in self._query(filters) if hasattr(item, "sectors")]

    def sector(self, value: str) -> Identity:
        value = value.lower().replace("_", "-").replace(" ", "-")

        filters = [
            Filter("type", "=", "identity"),
            Filter("sectors", "contains", value),
        ]
        return self._query_one(filters)