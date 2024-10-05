from openstix import DEFAULT_OPENSTIX_PATH
from openstix.providers.mitre import MITREDatasetExplorer
from openstix.toolkit.sources import FileSystemSource

dataset = MITREDatasetExplorer(
    source=FileSystemSource(
        stix_dir=DEFAULT_OPENSTIX_PATH / "mitre",
        allow_custom=True,
    )
)

print("Searching for the MITRE ATT&CK T1132.001 technique ...")
attack_technique = dataset.get_technique(external_id="T1132.001")
print(attack_technique.serialize(pretty=True))

print("\n")
input("[PRESS ENTER]")
print("\n\n")

print("Searching for the MITRE CAPEC CAPEC-586 technique ...")
capec_technique = dataset.get_technique(external_id="CAPEC-586")
print(capec_technique.serialize(pretty=True))
