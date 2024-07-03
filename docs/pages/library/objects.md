# Objects

## Standard Objects

Objects from STIX2 library can be accessed under `openstix.objects`:
```python
from opencti.objects import (
    Artifact
    AttackPattern
    AutonomousSystem
    Bundle
    Campaign
    CourseOfAction
    Directory
    DomainName
    EmailAddress
    EmailMessage
    File
    GranularMarking
    Grouping
    IPv4Address
    IPv6Address
    Identity
    Incident
    Indicator
    Infrastructure
    IntrusionSet
    LanguageContent
    Location
    MACAddress
    Malware
    MalwareAnalysis
    Mutex
    NetworkTraffic
    Note
    ObservedData
    Opinion
    Process
    Relationship
    Report
    Sighting
    Software
    StatementMarking
    TLPMarking
    ThreatActor
    Tool
    URL
    UserAccount
    Vulnerability
    WindowsRegistryKey
    X509Certificate
    Bundle
)   
```

**Reference:** https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html

## Custom Objects

### DNSRecord

```python
from openstix.objects.custom import DNSRecord

dns_record = DNSRecord(
    record_class="IN",
    record_type="A",
    record_ttl="60",
    value="8.8.8.8"
)
```