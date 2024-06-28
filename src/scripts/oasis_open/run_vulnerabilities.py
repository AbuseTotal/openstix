import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open.datasets.vulnerabilities import OASISOpenVulnerabilities
from openstix.toolkit.sources import FileSystemSource

oasis_vulnerabilities = OASISOpenVulnerabilities(
    source=FileSystemSource(
        stix_dir=os.path.join(OPENSTIX_PATH, "oasis-open", "vulnerabilities"),
        allow_custom=True,
    ),
)

print("OASIS Open Vulnerability Dataset loaded.")

vulnerability_name = "CVE-2009-3343"
vulnerability = oasis_vulnerabilities.vulnerability(name=vulnerability_name)

print(f"Search found the vulnerability '{vulnerability_name}' ...")
input("[PRESS ENTER]")
print(vulnerability.serialize(pretty=True))
