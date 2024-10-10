from typing import Literal

from openstix.filters import Filter, utils
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
from openstix.toolkit import CommonExplorerMixin, Workspace


class MITREDatasetExplorer(CommonExplorerMixin):
    def __init__(self, source):
        self._workspace = Workspace(source=source)

    def get_techniques(self, model: Literal["attack", "capec", "atlas"] = None) -> list:
        filters = [ATTACK_PATTERN_FILTER]

        match model:
            case "attack":
                filters.append(Filter("external_references.source_name", "=", "mitre-attack"))
            case "capec":
                filters.append(Filter("external_references.source_name", "=", "capec"))
            case "atlas":
                filters.append(Filter("external_references.source_name", "=", "mitre-atlas"))

        return self._workspace.query(filters)

    def get_technique(self, external_id):
        filters = [
            ATTACK_PATTERN_FILTER,
            Filter("external_references.external_id", "=", external_id),
        ]
        return self._workspace.query_one_or_none(filters)

    def get_matrices(self):
        return self._workspace.query([MITRE_MATRIX_FILTER])

    def get_matrix(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(MITRE_MATRIX_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_tactics(self):
        return self._workspace.query([MITRE_TACTIC_FILTER])

    def get_tactic(self, name, aliases=False):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(MITRE_TACTIC_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_data_sources(self):
        return self._workspace.query([MITRE_DATASOURCE_FILTER])

    def get_data_source(self, name, aliases=False):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(MITRE_DATASOURCE_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_data_components(self):
        return self._workspace.query([MITRE_DATA_COMPONENT_FILTER])

    def get_data_component(self, name, aliases=False):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(MITRE_DATA_COMPONENT_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_assets(self):
        return self._workspace.query([MITRE_ASSET_FILTER])

    def get_asset(self, name, aliases=False):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(MITRE_ASSET_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)
