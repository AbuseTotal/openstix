import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open.datasets.sectors import OASISOpenSectors
from openstix.toolkit.sources import FileSystemSource

oasis_sectors = OASISOpenSectors(
    source=FileSystemSource(
        stix_dir=os.path.join(OPENSTIX_PATH, "oasis-open", "sectors"),
        allow_custom=True,
    ),
)

print("OASIS Open Sectors Dataset loaded.")

sector_name = "Agriculture sector as a target"
sector = oasis_sectors.sector(name=sector_name)

print(f"Search found the sector '{sector_name}' ...")
input("[PRESS ENTER]")
print(sector.serialize(pretty=True))
