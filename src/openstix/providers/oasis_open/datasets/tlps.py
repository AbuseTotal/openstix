from openstix.filters import Filter
from openstix.providers._base import Dataset

VALID_TLPs = [
    "CLEAR",
    "GREEN",
    "AMBER",
    "AMBER+STRICT",
    "RED",
]


class TLP20(Dataset):
    def get_tlp(self, color):
        color = color.upper()

        if color not in VALID_TLPs:
            raise ValueError(f"Invalid TLP color: {color}")

        return self._query_one(
            filters=[
                Filter("type", "=", "marking-definition"),
                Filter("name", "=", f"TLP:{color}"),
            ]
        )

    @property
    def red(self):
        return self.get_tlp("RED")

    @property
    def amber_strict(self):
        return self.get_tlp("AMBER+STRICT")

    @property
    def amber(self):
        return self.get_tlp("AMBER")

    @property
    def green(self):
        return self.get_tlp("GREEN")

    @property
    def clear(self):
        return self.get_tlp("CLEAR")
