import os

from openstix import DEFAULT_OPENSTIX_PATH
from openstix.providers.mitre import MITRECapec
from openstix.toolkit.sources import FileSystemSource

mitre_capec = MITRECapec(
    source=FileSystemSource(
        stix_dir=os.path.join(
            DEFAULT_OPENSTIX_PATH,
            MITRECapec.config.provider,
            MITRECapec.config.name,
        ),
        allow_custom=True,
    ),
)

print("MITRE CAPEC Dataset loaded.")

technique = mitre_capec.technique(external_id="CAPEC-586")

print("Search found the MITRE CAPEC Technique ...")
input("[PRESS ENTER]")
print(technique.serialize(pretty=True))
