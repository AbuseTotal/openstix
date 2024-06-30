from openstix.filters import Filter
from openstix.objects import Location
from openstix.providers._base import Dataset, DatasetConfig


class Locations(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="locations",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/location",
        ],
    )

    def search(self, query):
        return self._search(
            [
                Filter("name", "contains", query),
                Filter("description", "contains", query),
                Filter("latitude", "contains", query),
                Filter("longitude", "contains", query),
                Filter("precision", "contains", query),
                Filter("region", "contains", query),
                Filter("country", "contains", query),
                Filter("administrative_area", "contains", query),
                Filter("city", "contains", query),
                Filter("street_address", "contains", query),
                Filter("postal_code", "contains", query),
            ]
        )

    def regions(self) -> list[Location]:
        filters = [
            Filter("type", "=", "location"),
        ]
        return [item for item in self._query(filters) if hasattr(item, "region")]

    def region(self, value: str) -> Location:
        value = value.lower().replace("_", "-").replace(" ", "-")

        filters = [
            Filter("type", "=", "location"),
            Filter("region", "=", value),
        ]
        return self._query_one(filters)

    def countries(self) -> list[Location]:
        filters = [
            Filter("type", "=", "location"),
        ]
        return [item for item in self._query(filters) if hasattr(item, "country")]

    def country(self, value: str) -> Location:
        value = value.upper()

        filters = [
            Filter("type", "=", "location"),
            Filter("country", "=", value),
        ]
        return self._query_one(filters)

    def administrative_areas(self, country: str) -> list[Location]:
        country = country.upper()

        filters = [
            Filter("type", "=", "location"),
            Filter("country", "=", country),
        ]
        return [item for item in self._query(filters) if hasattr(item, "administrative_area")]

    def administrative_area(self, country: str, area: str) -> list[Location]:
        country = country.upper()
        area = area.upper()

        if country == "US":
            area = f"{country}-{area}"

        filters = [
            Filter("type", "=", "location"),
            Filter("country", "=", country),
            Filter("administrative_area", "=", area),
        ]
        return self._query_one(filters)
