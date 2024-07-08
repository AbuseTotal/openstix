from openstix.providers._base import DatasetConfig, ProviderConfig, SourceConfig

CONFIG = ProviderConfig(
    name="mitre",
    datasets=[
        DatasetConfig(
            name="attack",
            sources=[
                SourceConfig(
                    type="json",
                    url="https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
                ),
                SourceConfig(
                    type="json",
                    url="https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json",
                ),
                SourceConfig(
                    type="json",
                    url="https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json",
                ),
            ],
        ),
        DatasetConfig(
            name="capec",
            sources=[
                SourceConfig(
                    type="json", url="https://raw.githubusercontent.com/mitre/cti/master/capec/2.1/stix-capec.json"
                ),
            ],
        ),
        DatasetConfig(
            name="attack",
            sources=[
                SourceConfig(
                    type="json",
                    url="https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas-attack-enterprise.json",
                ),
                SourceConfig(
                    type="json",
                    url="https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas.json",
                ),
            ],
        ),
    ],
)
