import os

from openstix import OPENSTIX_PATH
from openstix.providers.oasis_open import Vulnerabilities
from openstix.toolkit.sources import FileSystemSource

vulnerabilities = Vulnerabilities(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            Vulnerabilities.config.provider,
            Vulnerabilities.config.name,
        ),
        allow_custom=True,
    ),
)

print("OASIS Open Vulnerability Dataset loaded.")

vulnerability = vulnerabilities.vulnerability("CVE-2009-3343")
print(vulnerability.serialize(pretty=True))
