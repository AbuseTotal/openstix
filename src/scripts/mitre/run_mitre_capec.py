import os

from openstix import OPENSTIX_PATH
from openstix.providers.mitre import MITRECapec
from openstix.toolkit.sources import FileSystemSource

mitre_atlas = MITRECapec(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            MITRECapec.config.provider,
            MITRECapec.config.name,
        ),
        allow_custom=True,
    ),
)

print("MITRE CAPEC Dataset loaded.")

technique = mitre_atlas.technique(external_id="AML.T0003")

print("Search found the MITRE CAPEC Technique ...")
input("[PRESS ENTER]")
print(technique.serialize(pretty=True))
