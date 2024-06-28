import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open.datasets.locations import OASISOpenLocations
from openstix.toolkit.sources import FileSystemSource

oasis_locations = OASISOpenLocations(
    source=FileSystemSource(
        stix_dir=os.path.join(OPENSTIX_PATH, "oasis-open", "locations"),
        allow_custom=True,
    ),
)

print("OASIS Open Locations Dataset loaded.")

locations = oasis_locations.locations_by_country(country="PE")

print("Search found the location PE ...")
input("[PRESS ENTER]")
for location in locations:
    print(location.serialize(pretty=True))
