from openstix.filters import Filter
from openstix.objects import Identity
from openstix.providers._base import Dataset


class Industries(Dataset):
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
