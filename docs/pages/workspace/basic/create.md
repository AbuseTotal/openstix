# Create Objects in the Workspace

Creating objects in the OpenSTIX workspace is essential for adding new STIX objects to your environment. This guide will walk you through the steps to efficiently create various types of STIX objects using the Workspace class, leveraging the powerful capabilities of the STIX 2.1 specification. By using the create method of the Workspace class, you can easily add, customize with additional properties, and manage various types of STIX objects.

For more detailed information on the different types of STIX objects you can create, refer to the [STIX 2.1 documentation](https://docs.oasis-open.org/cti/stix/v2.1/csprd01/stix-v2.1-csprd01.html).

## Prerequisites

Before creating objects, ensure that you have the OpenSTIX library installed and properly configured in your environment.

## Importing Necessary Modules

First, import the necessary modules and classes:

```python
from openstix.objects import Indicator, Malware
from openstix import Workspace
```

## Initializing the Workspace

Create an instance of the Workspace class

```python
workspace = Workspace()
```

## Creating STIX Objects

### Example 1: Creating an Indicator
Indicators are used to describe specific and observable patterns of malicious activities. Here’s how to create an Indicator:

```python
indicator = workspace.create(
    Indicator, 
    name="Malicious IP", 
    pattern="[ipv4-addr:value = '203.0.113.1']", 
    pattern_type="stix"
)
print(indicator.serialize(pretty=True))
```


### Example 2: Creating Malware
Malware objects are used to describe malicious software, such as viruses, worms, or Trojans:


```python
malware = workspace.create(
    Malware, 
    name="Example Malware", 
    malware_types=["ransomware"]
)
print(malware.serialize(pretty=True))
```

### Adding Custom Properties
You can add custom properties to your STIX objects by including them as keyword arguments:


```python
custom_indicator = workspace.create(
    Indicator, 
    name="Custom Indicator", 
    pattern="[ipv4-addr:value = '198.51.100.1']", 
    pattern_type="stix", 
    confidence=75
)
print(custom_indicator.serialize(pretty=True))
```
