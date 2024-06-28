from stix2.v21.common import TLP_AMBER as _AMBER
from stix2.v21.common import TLP_GREEN as _GREEN
from stix2.v21.common import TLP_RED as _RED
from stix2.v21.common import TLP_WHITE as _WHITE

from openstix.filters import Filter
from openstix.providers._base import Dataset, DatasetConfig


class OASISOpenTLPs(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="tlps",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/marking-definition",
        ],
    )

    def get_tlp(self, name):
        if name == "white":
            return _WHITE
        elif name == "green":
            return _GREEN
        elif name == "amber":
            return _AMBER
        elif name == "red":
            return _RED
        else:
            raise ValueError(f"Invalid TLP name: {name}")

    @property
    def red(self):
        return _RED

    @property
    def amber(self):
        return _AMBER

    @property
    def green(self):
        return _GREEN

    @property
    def white(self):
        return _WHITE

    def search(self, query, revoked=False):
        return self._search(
            [
                Filter("definition_type", "contains", query),
                Filter("definition.tlp", "contains", query),
            ],
            revoked,
        )

    def tlps(self, revoked=False) -> list:
        filters = [Filter("type", "=", "marking-definition")]
        return self._query(filters, revoked)

    def tlp_by_color(self, color, revoked=False):
        if color not in ["white", "green", "amber", "red"]:
            raise ValueError(f"Invalid TLP color: {color}")

        filters = [
            Filter("type", "=", "marking-definition"),
            Filter("definition_type", "=", "tlp"),
            Filter("definition.tlp", "=", color),
        ]
        return self._query(filters, revoked)
