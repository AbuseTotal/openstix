import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open.datasets.tlps import OASISOpenTLPs
from openstix.toolkit.sources import FileSystemSource

oasis_tlps = OASISOpenTLPs(
    source=FileSystemSource(
        stix_dir=os.path.join(OPENSTIX_PATH, "oasis-open", "tlps"),
        allow_custom=True,
    ),
)

print("OASIS Open TLPs Dataset loaded.")

tlp_color = "amber"
tlps = oasis_tlps.tlp_by_color(color=tlp_color)

print(f"Search found the TLP '{tlp_color}' ...")
input("[PRESS ENTER]")
for tlp in tlps:
    print(tlp.serialize(pretty=True))
