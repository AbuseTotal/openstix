# OpenSTIX

OpenSTIX is an **unofficial STIX 2.1 library and toolkit** built upon the foundations of the [STIX2 library](https://github.com/oasis-open/cti-python-stix2/), aimed at enhancing the efficiency and productivity of cybersecurity professionals. It's developed and maintained by AbuseTotal, a startup committed to delivering high-quality software solutions in the cybersecurity domain.

[![PyPI version](https://badge.fury.io/py/openstix.svg)](https://badge.fury.io/py/openstix)

## Features

- **Modular Design**: Organizes the functionalities provided by STIX2 library into modules for easy consumption and extension.
- **Workspace Class**: Extends the `Environment` class into a `Workspace` class to facilitate seamless creation, removal, and management of STIX SDOs (Structured Data Objects) based on contributing properties.
- **Built-in Datasets**: Provides ready-to-use datasets including MITRE frameworks, geolocations, custom TLP markings, and industries to expedite the analytical process.
- **Custom Objects and Extensions**: Offers custom objects and extensions to assist analysts with additional informational resources such as Whois and DNS-Records.

## Installation

```bash
pip install openstix
```

## Documentation

Documentation is available [here](https://abusetotal.github.io/openstix-python/)

## Contributing

We welcome contributions to OpenSTIX! Whether you're reporting bugs, proposing new features, or contributing code, we appreciate your help. Please make sure to read our Contributing Guidelines before making a contribution.

## License

OpenSTIX is licensed under the Apache 2.0.

## Contact

For any inquiries, issues, or support related to OpenSTIX, feel free to create an issue.

## Acknowledgements

OpenSTIX is an initiative by AbuseTotal to foster the development of cybersecurity tools and libraries. We thank the OASIS Cyber Threat Intelligence Technical Committee and all STIX community for laying down the robust foundation upon which OpenSTIX is built.