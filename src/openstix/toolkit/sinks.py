import os

from stix2.datastore import DataSink  # noqa: F401
from stix2.datastore.filesystem import FileSystemSink  # noqa: F401
from stix2.datastore.memory import MemorySink  # noqa: F401
from stix2.datastore.taxii import TAXIICollectionSink  # noqa: F401
from taxii2client import Collection

from openstix.utils.extras import is_url

__all__ = [
    "load_sink",
    "DataSink",
    "FileSystemSink",
    "MemorySink",
    "TAXIICollectionSink",
]


def load_sink(sink_value):
    if is_url(sink_value):
        collection = Collection(sink_value)
        return TAXIICollectionSink(collection=collection, allow_custom=True)
    elif os.path.isdir(sink_value):
        return FileSystemSink(stix_dir=sink_value, allow_custom=True)
    else:
        raise ValueError("Sink must be a valid URL or directory path.")
