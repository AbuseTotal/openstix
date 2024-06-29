from openstix.filters import Filter
from openstix.providers._base import Dataset, DatasetConfig


class OASISOpenLocations(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="locations",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/location",
        ],
    )

    def search(self, query, revoked=False):
        return self._search(
            [
                Filter("name", "contains", query, case_insensitive=True),
                Filter("description", "contains", query, case_insensitive=True),
                Filter("latitude", "contains", query),
                Filter("longitude", "contains", query),
                Filter("precision", "contains", query),
                Filter("region", "contains", query, case_insensitive=True),
                Filter("country", "contains", query, case_insensitive=True),
                Filter("administrative_area", "contains", query, case_insensitive=True),
                Filter("city", "contains", query, case_insensitive=True),
                Filter("street_address", "contains", query, case_insensitive=True),
                Filter("postal_code", "contains", query),
            ],
            revoked,
        )

    def locations(self, revoked=False) -> list:
        filters = [Filter("type", "=", "location")]
        return self._query(filters, revoked)

    def location(self, name, revoked=False):
        filters = [
            Filter("type", "=", "location"),
            Filter("name", "=", name, case_insensitive=True),
        ]
        return self._query_one(filters, revoked)

    def regions(self, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("region", "exists", True),
        ]
        return self._query(filters, revoked)

    def region(self, name, revoked=False):
        filters = [
            Filter("type", "=", "location"),
            Filter("region", "=", name, case_insensitive=True),
        ]
        return self._query_one(filters, revoked)

    def locations_by_latitude(self, latitude, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("latitude", "=", latitude),
        ]
        return self._query(filters, revoked)

    def locations_by_longitude(self, longitude, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("longitude", "=", longitude),
        ]
        return self._query(filters, revoked)

    def locations_by_coordinates(self, latitude, longitude, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("latitude", "=", latitude),
            Filter("longitude", "=", longitude),
        ]
        return self._query(filters, revoked)

    def locations_by_precision(self, precision, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("precision", "=", precision),
        ]
        return self._query(filters, revoked)

    def locations_by_country(self, country, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("country", "=", country, case_insensitive=True),
        ]
        return self._query(filters, revoked)

    def locations_by_administrative_area(self, administrative_area, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("administrative_area", "=", administrative_area, case_insensitive=True),
        ]
        return self._query(filters, revoked)

    def locations_by_city(self, city, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("city", "=", city, case_insensitive=True),
        ]
        return self._query(filters, revoked)

    def locations_by_street_address(self, street_address, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("street_address", "=", street_address, case_insensitive=True),
        ]
        return self._query(filters, revoked)

    def locations_by_postal_code(self, postal_code, revoked=False) -> list:
        filters = [
            Filter("type", "=", "location"),
            Filter("postal_code", "=", postal_code),
        ]
        return self._query(filters, revoked)
