from openstix.filters import Filter

from openstix.filters.presets import (
    VULNERABILITY_FILTER,
)

class VulnerabilitiesMixin:
    def vulnerabilities(self) -> list:
        filters = [VULNERABILITY_FILTER]
        return self.query(filters)

    def vulnerability(self, value=None):
        value = value.upper()
        filters = [
            VULNERABILITY_FILTER,
            Filter("external_references.external_id", "=", value),
        ]
        return self.query_one(filters)
