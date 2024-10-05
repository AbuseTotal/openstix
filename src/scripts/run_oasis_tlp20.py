import os

from openstix import DEFAULT_OPENSTIX_PATH
from openstix.providers.oasis_open import TLP20
from openstix.toolkit.sources import FileSystemSource

tlp20 = TLP20(
    source=FileSystemSource(
        stix_dir=os.path.join(
            DEFAULT_OPENSTIX_PATH,
            TLP20.config.provider,
            TLP20.config.name,
        ),
        allow_custom=True,
    ),
)

print("OASIS Open TLP 2.0 Dataset loaded.")

tlp_green = tlp20.get_tlp(color="green")
tlp_red = tlp20.red

print(tlp_green.serialize(pretty=True))

print(tlp_red.serialize(pretty=True))
