CONFIG = [
    {
        "name": "attack",
        "provider": "mitre",
        "sources": [
            {
                "type": "json",
                "url": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
                "ignore_object_types": ["x-mitre-collection"],
            },
            {
                "type": "json",
                "url": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/mobile-attack/mobile-attack.json",
                "ignore_object_types": ["x-mitre-collection"],
            },
            {
                "type": "json",
                "url": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json",
                "ignore_object_types": ["x-mitre-collection"],
            },
        ],
    },
    {
        "name": "capec",
        "provider": "mitre",
        "sources": [
            {
                "type": "json",
                "url": "https://raw.githubusercontent.com/mitre/cti/master/capec/2.1/stix-capec.json",
                "ignore_object_types": ["x-mitre-collection"],
            },
        ],
    },
    {
        "name": "atlas",
        "provider": "mitre",
        "sources": [
            {
                "type": "json",
                "url": "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas-attack-enterprise.json",
                "ignore_object_types": ["x-mitre-collection"],
            },
            {
                "type": "json",
                "url": "https://raw.githubusercontent.com/mitre-atlas/atlas-navigator-data/main/dist/stix-atlas.json",
                "ignore_object_types": ["x-mitre-collection"],
            },
        ],
    },
]
