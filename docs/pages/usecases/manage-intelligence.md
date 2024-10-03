# Manage Intelligence

Import the necessary modules and get started with creating and managing STIX objects within your defined workspace.

## Start

### Initialize workspace
```python
from openstix.toolkit.workspace import Workspace

# Create a new workspace with your organization's namespace
workspace = Workspace(namespace="<your-namespace-uuid>")
```

### Load and Parse
```python
data = """
{
    "type": "bundle",
    "id": "bundle--0ef10afc-6a6b-4df7-bc4b-099977bfcba8",
    "objects": [
        {
            "type": "domain-name",
            "spec_version": "2.1",
            "id": "domain-name--9076dffc-9b97-55f6-a720-bc115b25fe31",
            "value": "openstix.dev"
        }
    ]
}
"""

# Parse STIX data and load automatically the objects in workspace
workspace.parse(data)
```

## CRUD

### Create SCO within workspace
```python
from openstix.objects import DomainName

# Add STIX observable object (SCO)
domain = self.workspace.create(Domain, value="abusetotal.com")
```

### Remove object from workspace
```python
# Remove STIX observable object (SCO)
self.workspace.remove(domain.id)
```

### Create SDO within workspace
```python
from openstix.objects import Malware

# Add STIX domain object (SDO)
self.workspace.create(Malware, name="Malicious", is_family=False)
```

## Filtering

### Filter workspace objects using presets filters
```python
from openstix.toolkit.filters.presets import MALWARE_FILTER

# Filter objects using presets
malwares = self.workspace.query(MALWARE_FILTER)
```