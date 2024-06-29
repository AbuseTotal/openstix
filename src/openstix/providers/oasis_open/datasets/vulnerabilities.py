from openstix.filters import Filter
from openstix.providers._base import Dataset, DatasetConfig


class OASISOpenVulnerabilities(Dataset):
    config = DatasetConfig(
        provider="oasis-open",
        name="vulnerabilities",
        urls=[
            "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/vulnerability",
        ],
    )

    def search(self, query, revoked=False):
        return self._search(
            [
                Filter("name", "contains", query, case_insensitive=True),
                Filter("description", "contains", query, case_insensitive=True),
                Filter("external_references", "contains", query, case_insensitive=True),
            ],
            revoked,
        )

    def vulnerabilities(self, revoked=False) -> list:
        filters = [Filter("type", "=", "vulnerability")]
        return self._query(filters, revoked)

    def vulnerability(self, name, revoked=False):
        filters = [
            Filter("type", "=", "vulnerability"),
            Filter("name", "=", name, case_insensitive=True),
        ]
        return self._query_one(filters, revoked)

    def vulnerabilities_by_description(self, description, revoked=False) -> list:
        filters = [
            Filter("type", "=", "vulnerability"),
            Filter("description", "contains", description, case_insensitive=True),
        ]
        return self._query(filters, revoked)

    def vulnerabilities_by_external_reference(self, external_id, revoked=False) -> list:
        filters = [
            Filter("type", "=", "vulnerability"),
            Filter("external_references.external_id", "=", external_id, case_insensitive=True),
        ]
        return self._query(filters, revoked)

    def vulnerabilities_by_created_by(self, created_by_ref, revoked=False) -> list:
        filters = [
            Filter("type", "=", "vulnerability"),
            Filter("created_by_ref", "=", created_by_ref, case_insensitive=True),
        ]
        return self._query(filters, revoked)
