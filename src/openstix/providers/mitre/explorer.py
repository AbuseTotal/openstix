from typing import Literal

from openstix.filters import Filter
from openstix.filters.presets import (
    ATTACK_PATTERN_FILTER,
)
from openstix.providers.mitre.presets import (
    MITRE_ASSET_FILTER,
    MITRE_DATA_COMPONENT_FILTER,
    MITRE_DATASOURCE_FILTER,
    MITRE_MATRIX_FILTER,
    MITRE_TACTIC_FILTER,
)
from openstix.toolkit import Workspace


class MITREDatasetExplorer:
    def __init__(self, source):
        self.workspace = Workspace(source=source)

    def get_techniques(self, model: Literal["attack", "capec", "atlas"] = None) -> list:
        filters = [ATTACK_PATTERN_FILTER]

        match model:
            case "attack":
                filters.append(Filter("external_references.source_name", "=", "mitre-attack"))
            case "capec":
                filters.append(Filter("external_references.source_name", "=", "capec"))
            case "atlas":
                filters.append(Filter("external_references.source_name", "=", "mitre-atlas"))

        return self.workspace.query(filters)

    def get_technique(self, external_id):
        filters = [ATTACK_PATTERN_FILTER, Filter("external_references.external_id", "=", external_id)]
        return self.workspace.get(filters)

    def get_matrices(self):
        return self.workspace.query([MITRE_MATRIX_FILTER])

    def get_matrix(self, name, aliases=True):
        return self.workspace.query_name_and_alias(filters=[MITRE_MATRIX_FILTER], name=name, aliases=aliases)

    def get_tactics(self):
        return self.workspace.query([MITRE_TACTIC_FILTER])

    def get_tactic(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_TACTIC_FILTER], name=name, aliases=aliases)

    def get_data_sources(self):
        return self.workspace.query([MITRE_DATASOURCE_FILTER])

    def get_data_source(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_DATASOURCE_FILTER], name=name, aliases=aliases)

    def get_data_components(self):
        return self.workspace.query([MITRE_DATA_COMPONENT_FILTER])

    def get_data_component(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_DATA_COMPONENT_FILTER], name=name, aliases=aliases)

    def get_assets(self):
        return self.workspace.query([MITRE_ASSET_FILTER])

    def get_asset(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_ASSET_FILTER], name=name, aliases=aliases)
