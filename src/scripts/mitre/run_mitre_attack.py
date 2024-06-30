import os

from openstix import OPENSTIX_PATH
from openstix.providers.mitre import MITREAttack
from openstix.toolkit.sources import FileSystemSource

mitre_attack = MITREAttack(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            MITREAttack.config.provider,
            MITREAttack.config.name,
        ),
        allow_custom=True,
    ),
)
mitre_attack.intrusion_set("red delta")
mitre_attack.intrusion_set("Ke3Chang")
mitre_attack.intrusion_set("metushy")

print("MITRE ATT&CK Dataset loaded.")

technique = mitre_attack.technique(external_id="T1132.001")

print("Search found the MITRE ATT&CK Technique ...")
input("[PRESS ENTER]")
print(technique.serialize(pretty=True))
