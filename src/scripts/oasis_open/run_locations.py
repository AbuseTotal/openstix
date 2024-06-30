import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open import Locations
from openstix.toolkit.sources import FileSystemSource

locations = Locations(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            Locations.config.provider,
            Locations.config.name,
        ),
        allow_custom=True,
    ),
)

print("OASIS Open Locations Dataset loaded.")

location = locations.country("PT")
print(location.serialize(pretty=True))

location = locations.region("western-europe")
print(location.serialize(pretty=True))

location = locations.administrative_area("US", "DC")
print(location.serialize(pretty=True))
