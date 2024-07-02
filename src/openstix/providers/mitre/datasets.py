from typing import Literal

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
from openstix.providers._base import Dataset
from openstix.providers.mitre.presets import (
    MITRE_ASSET_FILTER,
    MITRE_DATA_COMPONENT_FILTER,
    MITRE_DATASOURCE_FILTER,
    MITRE_MATRIX_FILTER,
    MITRE_TACTIC_FILTER,
)


class MITRE(Dataset):
    def techniques(self, model: Literal["attack", "capec", "atlas"] = None) -> list:
        filters = [ATTACK_PATTERN_FILTER]

        if model and model == "attack":
            filters += Filter("external_references.source_name", "=", "mitre-attack")

        if model and model == "capec":
            filters += Filter("external_references.source_name", "=", "capec")

        if model and model == "atlas":
            filters += Filter("external_references.source_name", "=", "mitre-atlas")

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
