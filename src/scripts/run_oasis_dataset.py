from openstix import DEFAULT_OPENSTIX_PATH
from openstix.providers.oasis_open import OASISOpenDatasetExplorer
from openstix.toolkit.sources import FileSystemSource

dataset = OASISOpenDatasetExplorer(
    source=FileSystemSource(
        stix_dir=DEFAULT_OPENSTIX_PATH / "oasis-open",
        allow_custom=True,
    )
)

print("Searching for the country 'Portugal' ...\n")
country = dataset.locations.get_country("PT")
print(country.serialize(pretty=True))

print("\n")
input("[PRESS ENTER]")
print("\n\n")

print("Searching for the region 'Western Europe' ...\n")
region = dataset.locations.get_region("western-europe")
print(region.serialize(pretty=True))

print("\n")
input("[PRESS ENTER]")
print("\n\n")

print("Searching for the administrative area 'DC' in 'USA' ...\n")
location = dataset.locations.get_administrative_area("US", "DC")
print(region.serialize(pretty=True))

print("\n")
input("[PRESS ENTER]")
print("\n\n")

print("Searching for the sector 'agriculture' ...\n")
sector = dataset.sectors.get_sector("agriculture")
print(sector.serialize(pretty=True))

print("\n")
input("[PRESS ENTER]")
print("\n\n")

print("Searching for the TLP 'amber+strict' ...\n")
tlp = dataset.tlps.get_tlp("amber+strict")
print(tlp.serialize(pretty=True))

print("\n")
input("[PRESS ENTER]")
print("\n\n")

print("Searching for the vulnerability 'CVE-2009-3343' ...\n")
vulnerability = dataset.vulnerabilities.get_vulnerability("CVE-2009-3343")
print(vulnerability.serialize(pretty=True))
