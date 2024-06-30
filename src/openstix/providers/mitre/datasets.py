from openstix.filters import Filter
from openstix.filters.presets import (
    ATTACK_PATTERN_FILTER,
    CAMPAIGN_FILTER,
    COURSE_OF_ACTION_FILTER,
    INTRUSION_SET_FILTER,
    MALWARE_FILTER,
    SOFTWARE_FILTER,
    TOOL_FILTER,
)
from openstix.providers._base import Dataset, DatasetConfig
from openstix.providers.mitre.presets import (
    MITRE_ASSET_FILTER,
    MITRE_DATA_COMPONENT_FILTER,
    MITRE_DATASOURCE_FILTER,
    MITRE_MATRIX_FILTER,
    MITRE_TACTIC_FILTER,
)


class MITRE(Dataset):
    def techniques(self) -> list:
        filters = [ATTACK_PATTERN_FILTER]
        return self._query(filters)

    def technique(self, external_id):
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.external_id", "=", external_id),
        ]
        return self._query_one(filters)

    def intrusion_sets(self):
        return self._query([INTRUSION_SET_FILTER])

    def intrusion_set(self, name, aliases=True):
        return self._query_name_and_alias(filters=[INTRUSION_SET_FILTER], name=name, aliases=aliases)

    def campaigns(self):
        return self._query([CAMPAIGN_FILTER])

    def campaign(self, name, aliases=True):
        return self._query_name_and_alias(filters=[CAMPAIGN_FILTER], name=name, aliases=aliases)

    def malwares(self):
        return self._query([MALWARE_FILTER])

    def malware(self, name, aliases=True):
        return self._query_name_and_alias(filters=[MALWARE_FILTER], name=name, aliases=aliases)

    def tools(self):
        return self._query([TOOL_FILTER])

    def tool(self, name, aliases=True):
        return self._query_name_and_alias(filters=[TOOL_FILTER], name=name, aliases=aliases)

    def matrices(self):
        return self._query([MITRE_MATRIX_FILTER])

    def matrix(self, name, aliases=True):
        return self._query_name_and_alias(filters=[MITRE_MATRIX_FILTER], name=name, aliases=aliases)

    def tactics(self):
        return self._query([MITRE_TACTIC_FILTER])

    def tactic(self, name, aliases=False):
        return self._query_name_and_alias(filters=[MITRE_TACTIC_FILTER], name=name, aliases=aliases)

    def mitigations(self):
        return self._query([COURSE_OF_ACTION_FILTER])

    def mitigation(self, name, aliases=False):
        return self._query_name_and_alias(filters=[COURSE_OF_ACTION_FILTER], name=name, aliases=aliases)

    def softwares(self):
        return self._query([SOFTWARE_FILTER])

    def software(self, name, aliases=True):
        return self._query_name_and_alias(filters=[SOFTWARE_FILTER], name=name, aliases=aliases)

    def data_sources(self):
        return self._query([MITRE_DATASOURCE_FILTER])

    def data_source(self, name, aliases=False):
        return self._query_name_and_alias(filters=[MITRE_DATASOURCE_FILTER], name=name, aliases=aliases)

    def data_components(self):
        return self._query([MITRE_DATA_COMPONENT_FILTER])

    def data_component(self, name, aliases=False):
        return self._query_name_and_alias(filters=[MITRE_DATA_COMPONENT_FILTER], name=name, aliases=aliases)

    def assets(self):
        return self._query([MITRE_ASSET_FILTER])

    def asset(self, name, aliases=False):
        return self._query_name_and_alias(filters=[MITRE_ASSET_FILTER], name=name, aliases=aliases)


def common_filters(query: str) -> list[Filter]:
    return [
        Filter("name", "contains", query),
        Filter("description", "contains", query),
        Filter("labels", "contains", query),
        Filter("aliases", "contains", query),
    ]


class MITREAttack(MITRE):
    config = DatasetConfig(
        provider="mitre",
        name="attack",
        urls=[
            "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
            "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json",
            "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json",
        ],
    )

    def search(self, query):
        filters = common_filters(query) + [
            Filter("x_mitre_aliases", "contains", query),
            Filter("x_mitre_domains", "contains", query),
            Filter("x_mitre_platforms", "contains", query),
        ]

        return self.search(filters)

    def techniques(self) -> list:
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.source_name", "=", "mitre-attack"),
        ]
        return self._query(filters)


class MITRECapec(MITRE):
    config = DatasetConfig(
        provider="mitre",
        name="capec",
        urls=[
            "https://raw.githubusercontent.com/mitre/cti/master/capec/2.1/stix-capec.json",
        ],
    )

    def search(self, query):
        filters = common_filters(query) + [
            Filter("x_capec_status", "contains", query),
            Filter("x_capec_domains", "contains", query),
            Filter("x_capec_abstraction", "contains", query),
            Filter("x_capec_consequences", "contains", query),
            Filter("x_capec_prerequisites", "contains", query),
            Filter("x_capec_resources_required", "contains", query),
        ]

        return self.search(filters)

    def techniques(self) -> list:
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.source_name", "=", "capec"),
        ]
        return self._query(filters)


class MITREAtlas(MITRE):
    config = DatasetConfig(
        provider="mitre",
        name="atlas",
        urls=[
            "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas-attack-enterprise.json",
            "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas.json",
        ],
    )

    def search(self, query):
        filters = common_filters(query) + [
            Filter("x_mitre_shortname", "contains", query),
        ]

        return self.search(filters)

    def techniques(self) -> list:
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.source_name", "=", "mitre-atlas"),
        ]
        return self._query(filters)
