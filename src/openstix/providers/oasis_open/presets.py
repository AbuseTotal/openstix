from openstix.filters import Filter

OASIS_SECTOR_FILTER = Filter("identity_class", "=", "class")

OASIS_VULNERABILITY_FILTER = Filter("type", "=", "vulnerability")

OASIS_TLP_FILTER_WHITE = Filter("definition.tlp", "=", "white")
OASIS_TLP_FILTER_GREEN = Filter("definition.tlp", "=", "green")
OASIS_TLP_FILTER_AMBER = Filter("definition.tlp", "=", "amber")
OASIS_TLP_FILTER_RED = Filter("definition.tlp", "=", "red")

OASIS_LOCATION_FILTER = Filter("type", "=", "location")
OASIS_LOCATION_REGION_FILTER = Filter("region", "exists", True)
