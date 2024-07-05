from openstix.filters import Filter
from openstix.objects import Location

class LocationsMixin:
    def regions(self) -> list[Location]:
        filters = [
            Filter("type", "=", "location"),
        ]
        return [item for item in self.query(filters) if hasattr(item, "region")]

    def region(self, value: str) -> Location:
        value = value.lower().replace("_", "-").replace(" ", "-")

        filters = [
            Filter("type", "=", "location"),
            Filter("region", "=", value),
        ]
        return self.query_one(filters)

    def countries(self) -> list[Location]:
        filters = [
            Filter("type", "=", "location"),
        ]
        return [item for item in self.query(filters) if hasattr(item, "country")]

    def country(self, value: str) -> Location:
        value = value.upper()

        filters = [
            Filter("type", "=", "location"),
            Filter("country", "=", value),
        ]
        return self.query_one(filters)

    def administrative_areas(self, country: str) -> list[Location]:
        country = country.upper()

        filters = [
            Filter("type", "=", "location"),
            Filter("country", "=", country),
        ]
        return [item for item in self.query(filters) if hasattr(item, "administrative_area")]

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
        return self.query_one(filters)
