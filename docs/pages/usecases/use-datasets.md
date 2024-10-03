# Use Datasets

In order to avoid having to create, for example, attack pattern objects for MITRE ATT&CK and have duplicated objects all over the place, with openstix you can download STIX datasets from external providers and use them in a seemsly way.

## Get MITRE TTP using MITRE Datasets

**Note:** make sure you have downloaded the dataset using openstix cli

```python
from openstix.datasets import MITREDataset

dataset = MITREDataset()
dataset.load()

# Use Attack Pattern objects from MITRE Dataset
attack_pattern = dataset.attack_pattern("T1090")
```

## Get country and regions objects using GeoLocation Datasets

**Note:** make sure you have downloaded the dataset using openstix cli

```python
from openstix.datasets import GeoLocationsDataset

dataset = GeoLocationsDataset()
dataset.load()

# Use Location objects from GeoLocation Dataset
country = dataset.country("PT")
region = dataset.region("Europe")
```