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
    MITRE_SUBTECHNIQUE_FILTER,
    MITRE_TACTIC_FILTER,
    MITRE_TECHNIQUE_FILTER,
)


class MITRE(Dataset):
    def techniques(self, include_subtechniques=True, revoked=False) -> list:
        filters = [ATTACK_PATTERN_FILTER]
        if include_subtechniques:
            filters += [MITRE_SUBTECHNIQUE_FILTER]
        else:
            filters += [MITRE_TECHNIQUE_FILTER]
        return self._query(filters, revoked)

    def subtechniques(self, revoked=False) -> list:
        return self._query([ATTACK_PATTERN_FILTER, MITRE_SUBTECHNIQUE_FILTER], revoked)

    def technique(self, external_id, revoked=False):
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.external_id", "=", external_id),
        ]
        return self._query_one(filters, revoked)

    def intrusion_sets(self, revoked=False):
        return self._query([INTRUSION_SET_FILTER], revoked)

    def intrusion_set(self, name, aliases=True, revoked=False):
        return self._query_name_and_alias(filters=[INTRUSION_SET_FILTER], name=name, aliases=aliases, revoked=revoked)

    def campaigns(self, revoked=False):
        return self._query([CAMPAIGN_FILTER], revoked)

    def campaign(self, name, aliases=True, revoked=False):
        return self._query_name_and_alias(filters=[CAMPAIGN_FILTER], name=name, aliases=aliases, revoked=revoked)

    def malwares(self, revoked=False):
        return self._query([MALWARE_FILTER], revoked)

    def malware(self, name, aliases=True, revoked=False):
        return self._query_name_and_alias(filters=[MALWARE_FILTER], name=name, aliases=aliases, revoked=revoked)

    def tools(self, revoked=False):
        return self._query([TOOL_FILTER], revoked)

    def tool(self, name, aliases=True, revoked=False):
        return self._query_name_and_alias(filters=[TOOL_FILTER], name=name, aliases=aliases, revoked=revoked)

    def matrices(self, revoked=False):
        return self._query([MITRE_MATRIX_FILTER], revoked)

    def matrix(self, name, aliases=True, revoked=False):
        return self._query_name_and_alias(filters=[MITRE_MATRIX_FILTER], name=name, aliases=aliases, revoked=revoked)

    def tactics(self, revoked=False):
        return self._query([MITRE_TACTIC_FILTER], revoked)

    def tactic(self, name, aliases=False, revoked=False):
        return self._query_name_and_alias(filters=[MITRE_TACTIC_FILTER], name=name, aliases=aliases, revoked=revoked)

    def mitigations(self, revoked=False):
        return self._query([COURSE_OF_ACTION_FILTER], revoked)

    def mitigation(self, name, aliases=False, revoked=False):
        return self._query_name_and_alias(
            filters=[COURSE_OF_ACTION_FILTER], name=name, aliases=aliases, revoked=revoked
        )

    def softwares(self, revoked=False):
        return self._query([SOFTWARE_FILTER], revoked)

    def software(self, name, aliases=True, revoked=False):
        return self._query_name_and_alias(filters=[SOFTWARE_FILTER], name=name, aliases=aliases, revoked=revoked)

    def data_sources(self, revoked=False):
        return self._query([MITRE_DATASOURCE_FILTER], revoked)

    def data_source(self, name, aliases=False, revoked=False):
        return self._query_name_and_alias(
            filters=[MITRE_DATASOURCE_FILTER], name=name, aliases=aliases, revoked=revoked
        )

    def data_components(self, revoked=False):
        return self._query([MITRE_DATA_COMPONENT_FILTER], revoked)

    def data_component(self, name, aliases=False, revoked=False):
        return self._query_name_and_alias(
            filters=[MITRE_DATA_COMPONENT_FILTER], name=name, aliases=aliases, revoked=revoked
        )

    def assets(self, revoked=False):
        return self._query([MITRE_ASSET_FILTER], revoked)

    def asset(self, name, aliases=False, revoked=False):
        return self._query_name_and_alias(filters=[MITRE_ASSET_FILTER], name=name, aliases=aliases, revoked=revoked)


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


class MITRECapec(MITRE):
    config = DatasetConfig(
        provider="mitre",
        name="capec",
        urls=[
            "https://raw.githubusercontent.com/mitre/cti/master/capec/2.1/stix-capec.json",
        ],
    )


class MITREAtlas(MITRE):
    config = DatasetConfig(
        provider="mitre",
        name="atlas",
        urls=[
            "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas-attack-enterprise.json",
            "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas.json",
        ],
    )
