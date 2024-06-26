from openstix.filters import Filter

MITRE_TECHNIQUE_FILTER = Filter("x_mitre_is_subtechnique", "=", False)
MITRE_SUBTECHNIQUE_FILTER = Filter("x_mitre_is_subtechnique", "=", True)
MITRE_DATASOURCE_FILTER = Filter("type", "=", "x-mitre-datasource")
MITRE_DATA_COMPONENT_FILTER = Filter("type", "=", "x-mitre-data-component")
MITRE_ASSET_FILTER = Filter("type", "=", "x-mitre-asset")
MITRE_MATRIX_FILTER = Filter("type", "=", "x-mitre-matrix")
MITRE_TACTIC_FILTER = Filter("type", "=", "x-mitre-tactic")
