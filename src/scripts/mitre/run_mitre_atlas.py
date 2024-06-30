import os

from openstix import OPENSTIX_PATH
from openstix.providers.mitre import MITREAtlas
from openstix.toolkit.sources import FileSystemSource

mitre_atlas = MITREAtlas(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            MITREAtlas.config.provider,
            MITREAtlas.config.name,
        ),
        allow_custom=True,
    ),
)

print("MITRE Atlas Dataset loaded.")

technique = mitre_atlas.technique(external_id="AML.T0003")

print("Search found the MITRE Atlas Technique ...")
input("[PRESS ENTER]")
print(technique.serialize(pretty=True))
