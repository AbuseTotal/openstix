from openstix.filters import Filter
from openstix.providers._base import Dataset, DatasetConfig


class OASISOpenSectors(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="sectors",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/identity",
        ],
    )

    def search(self, query, revoked=False):
        return self._search(
            [
                Filter("name", "contains", query),
                Filter("description", "contains", query),
                Filter("roles", "contains", query),
                Filter("identity_class", "contains", query),
                Filter("sectors", "contains", query),
                Filter("contact_information", "contains", query),
            ],
            revoked,
        )

    def sectors(self, revoked=False) -> list:
        filters = [
            Filter("type", "=", "identity"),
            Filter("sectors", "exists", True),
        ]
        return self._query(filters, revoked)

    def sector(self, name, aliases=True, revoked=False):
        filters = [
            Filter("type", "=", "identity"),
            Filter("name", "=", name),
        ]
        return self._query_one(filters, revoked)
