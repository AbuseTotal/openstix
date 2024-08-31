CONFIG = [
    {
        "name": "locations",
        "provider": "oasis-open",
        "sources": [
            {
                "type": "github_api",
                "url": "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/location",
            },
        ],
    },
    {
        "name": "industries",
        "provider": "oasis-open",
        "sources": [
            {
                "type": "github_api",
                "url": "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/identity",
            },
        ],
    },
    {
        "name": "vulnerabilities",
        "provider": "oasis-open",
        "sources": [
            {
                "type": "zip",
                "url": "https://github.com/oasis-open/cti-stix-common-objects/archive/refs/heads/main.zip",
                "paths": ["objects/vulnerability"],
            },
        ],
    },
    {
        "name": "tlp20",
        "provider": "oasis-open",
        "sources": [
            {
                "type": "github_api",
                "url": "https://api.github.com/repos/oasis-open/cti-stix-common-objects/contents/objects/marking-definition",
            },
        ],
    },
]
