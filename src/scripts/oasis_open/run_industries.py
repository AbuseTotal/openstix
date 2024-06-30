import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open import Industries
from openstix.toolkit.sources import FileSystemSource

sectors = Industries(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            Industries.config.provider,
            Industries.config.name,
        ),
        allow_custom=True,
    ),
)

sector = sectors.sector("agriculture")
print(sector.serialize(pretty=True))
