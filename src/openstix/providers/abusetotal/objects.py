from openstix import properties
from openstix.customize import CustomObservable


@CustomObservable(
    "x-dns-record",
    [
        ("record_class", properties.StringProperty(required=True)),
        ("record_type", properties.StringProperty(required=True)),
        ("record_ttl", properties.StringProperty(required=True)),
        ("value", properties.StringProperty(required=True)),
    ],
    [
        "record_class",
        "record_type",
        "record_ttl",
        "value",
    ],
)
class DNSRecord:
    pass
