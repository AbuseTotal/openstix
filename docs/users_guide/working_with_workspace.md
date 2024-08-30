## Using the Workspace for Cybersecurity Analysis
The Workspace class extends the stix2.Environment class to provide a customized environment for handling STIX objects. This guide will walk you through using the Workspace class to perform various operations, such as creating, querying, and parsing STIX objects.

**Prerequisites**

- Python 3.7 or higher
- OpenSTIX library installed (pip install openstix)

### Importing Required Modules
First, import the necessary modules:

```python
from stix2 import Environment, MemoryStore
from openstix import utils
from openstix.objects import Bundle
```

### Initializing the Workspace
Create an instance of the Workspace class. By default, it uses a MemoryStore to store STIX objects.

```python
workspace = Workspace()
```

### Creating STIX Objects
You can create and add STIX objects to the workspace using the create method. This method immediately adds the created object to the store.

**Example: Creating an Indicator**
```python
indicator = workspace.create('Indicator', name='Malicious IP', pattern="[ipv4-addr:value = '198.51.100.1']")
print(indicator.serialize(pretty=True))
```

### Querying STIX Objects
Use the `query` method to retrieve STIX objects from the store. You can filter results and choose to return only the most recent versions of objects.

**Example: Querying All Objects**
```python
all_objects = workspace.query()
for obj in all_objects:
    print(obj.serialize(pretty=True))
```

**Example: Querying with Filters**
```python
from openstix.toolkit.filters.presets import INDICATOR_FILTER

indicators = workspace.query(INDICATOR_FILTER)
for indicator in indicators:
    print(indicator.serialize(pretty=True))
```


### Parsing STIX Data
The `parse` method allows you to convert a string, dictionary, or file-like object containing STIX data into STIX objects and add them to the workspace.

**Example: Parsing a JSON Bundle**

Assume you have a STIX bundle in a JSON file named `bundle.json`.
```python
with open('bundle.json', 'r') as f:
    data = f.read()
workspace.parse(data)
```

### Generating Statistics
The `stats` method generates statistics on the STIX objects within the store, counting the occurrences of each type of STIX object.


**Example: Generating Statistics**

```python
stats = workspace.stats()
print(stats)
```


### Generating Statistics
You can remove a STIX object and all its versions from the store using the `remove` method.


**Example: Removing an Object**

```python
object_id = 'indicator--12345678-1234-1234-1234-123456789012'
workspace.remove(object_id)
```

### Complete Example: Cybersecurity Analysis
Here is a complete example that demonstrates creating, querying, parsing, and analyzing network traffic data using the `Workspace` class.


```python
from stix2 import Environment, MemoryStore
from openstix import utils
from openstix.objects import Bundle

# Initialize the workspace
workspace = Workspace()

# Create an IP address observable
src_ip = workspace.create('IPv4Address', value='192.168.1.1')
dst_ip = workspace.create('IPv4Address', value='10.0.0.1')

# Create a Network Traffic object
network_traffic = workspace.create(
    'NetworkTraffic',
    start="2024-06-01T12:00:00Z",
    end="2024-06-01T12:05:00Z",
    src_ref=src_ip.id,
    dst_ref=dst_ip.id,
    protocols=["tcp"],
    src_port=443,
    dst_port=8080
)

# Bundle the objects and serialize to JSON
bundle = Bundle(objects=[src_ip, dst_ip, network_traffic])
print(bundle.serialize(pretty=True))

# Query the workspace for all objects
all_objects = workspace.query()
for obj in all_objects:
    print(obj.serialize(pretty=True))

# Parse a STIX bundle from a JSON file
with open('bundle.json', 'r') as f:
    data = f.read()
workspace.parse(data)

# Generate statistics
stats = workspace.stats()
print(stats)

# Remove an object by ID
object_id = 'network-traffic--12345678-1234-1234-1234-123456789012'
workspace.remove(object_id)
```