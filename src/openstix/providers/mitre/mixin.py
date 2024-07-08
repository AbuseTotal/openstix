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


class Mixin:
    def __init__(self, workspace):
        self.workspace = workspace

    def techniques(self, model: Literal["attack", "capec", "atlas"] = None) -> list:
        filters = [ATTACK_PATTERN_FILTER]

        if model and model == "attack":
            filters.append(Filter("external_references.source_name", "=", "mitre-attack"))

        if model and model == "capec":
            filters.append(Filter("external_references.source_name", "=", "capec"))

        if model and model == "atlas":
            filters.append(Filter("external_references.source_name", "=", "mitre-atlas"))

        return self.workspace.query(filters)

    def technique(self, external_id):
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.external_id", "=", external_id),
        ]
        return self.workspace.query_one(filters)

    def matrices(self):
        return self.workspace.query([MITRE_MATRIX_FILTER])

    def matrix(self, name, aliases=True):
        return self.workspace.query_name_and_alias(filters=[MITRE_MATRIX_FILTER], name=name, aliases=aliases)

    def tactics(self):
        return self.workspace.query([MITRE_TACTIC_FILTER])

    def tactic(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_TACTIC_FILTER], name=name, aliases=aliases)

    def data_sources(self):
        return self.workspace.query([MITRE_DATASOURCE_FILTER])

    def data_source(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_DATASOURCE_FILTER], name=name, aliases=aliases)

    def data_components(self):
        return self.workspace.query([MITRE_DATA_COMPONENT_FILTER])

    def data_component(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_DATA_COMPONENT_FILTER], name=name, aliases=aliases)

    def assets(self):
        return self.workspace.query([MITRE_ASSET_FILTER])

    def asset(self, name, aliases=False):
        return self.workspace.query_name_and_alias(filters=[MITRE_ASSET_FILTER], name=name, aliases=aliases)
