from openstix.filters import Filter
from openstix.filters.presets import (
    IDENTITY_FILTER,
    LOCATION_FILTER,
    VULNERABILITY_FILTER,
)
from openstix.objects import Identity, Location, Vulnerability
from openstix.toolkit import Workspace


class Vulnerabilities:
    def __init__(self, workspace):
        self._workspace = workspace

    def get_vulnerabilities(self) -> list[Vulnerability]:
        filters = [VULNERABILITY_FILTER]
        return self._workspace.query(filters)

    def get_vulnerability(self, value=None) -> Vulnerability:
        value = value.upper()
        filters = [
            VULNERABILITY_FILTER,
            Filter("external_references.external_id", "=", value),
        ]
        return self._workspace.query_one_or_none(filters)


class Sectors:
    def __init__(self, workspace):
        self._workspace = workspace

    def get_sectors(self) -> list[Identity]:
        filters = [IDENTITY_FILTER]
        return [item for item in self._workspace.query(filters) if hasattr(item, "sectors")]

    def get_sector(self, value: str) -> Identity:
        value = value.lower().replace("_", "-").replace(" ", "-")
        filters = [
            IDENTITY_FILTER,
            Filter("sectors", "contains", value),
        ]
        return self._workspace.query_one_or_none(filters)


class Locations:
    def __init__(self, workspace):
        self._workspace = workspace

    def get_regions(self) -> list[Location]:
        filters = [LOCATION_FILTER]
        return [item for item in self._workspace.query(filters) if hasattr(item, "region")]

    def get_region(self, value: str) -> Location:
        value = value.lower().replace("_", "-").replace(" ", "-")
        filters = [
            LOCATION_FILTER,
            Filter("region", "=", value),
        ]
        return self._workspace.query_one_or_none(filters)

    def get_countries(self) -> list[Location]:
        filters = [LOCATION_FILTER]
        return [item for item in self._workspace.query(filters) if hasattr(item, "country")]

    def get_country(self, value: str) -> Location:
        value = value.upper()
        filters = [
            LOCATION_FILTER,
            Filter("country", "=", value),
        ]
        return self._workspace.query_one_or_none(filters)

    def get_administrative_areas(self, country: str) -> list[Location]:
        country = country.upper()
        filters = [
            LOCATION_FILTER,
            Filter("country", "=", country),
        ]
        return [item for item in self._workspace.query(filters) if hasattr(item, "administrative_area")]

    def get_administrative_area(self, country: str, area: str) -> list[Location]:
        country = country.upper()
        area = area.upper()
        if country == "US":
            area = f"{country}-{area}"
        filters = [
            LOCATION_FILTER,
            Filter("country", "=", country),
            Filter("administrative_area", "=", area),
        ]
        return self._workspace.query_one_or_none(filters)


class TLP20:
    def __init__(self, workspace):
        self._workspace = workspace

    VALID_TLPs = [
        "CLEAR",
        "GREEN",
        "AMBER",
        "AMBER+STRICT",
        "RED",
    ]

    def get_tlp(self, color):
        color = color.upper()
        if color not in TLP20.VALID_TLPs:
            raise ValueError(f"Invalid TLP color: {color}")
        return self._workspace.query_one_or_none(
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


class OASISOpenDatasetExplorer:
    def __init__(self, source):
        self._workspace = Workspace(source=source)

        self._vulnerabilities = Vulnerabilities(self._workspace)
        self._sectors = Sectors(self._workspace)
        self._locations = Locations(self._workspace)
        self._tlps = TLP20(self._workspace)

    @property
    def vulnerabilities(self):
        return self._vulnerabilities

    @property
    def sectors(self):
        return self._sectors

    @property
    def locations(self):
        return self._locations

    @property
    def tlps(self):
        return self._tlps
