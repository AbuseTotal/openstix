import os

from stix2.datastore import CompositeDataSource, DataSource  # noqa: F401
from stix2.datastore.filesystem import FileSystemSource  # noqa: F401
from stix2.datastore.memory import MemorySource  # noqa: F401
from stix2.datastore.taxii import TAXIICollectionSource  # noqa: F401
from taxii2client import Collection

from openstix.utils.extras import is_url

__all__ = [
    "load_source",
    "CompositeDataSource",
    "DataSource",
    "FileSystemSource",
    "MemorySource",
    "TAXIICollectionSource",
]


def load_source(source_value):
    if is_url(source_value):
        collection = Collection(source_value)
        return TAXIICollectionSource(collection=collection, allow_custom=True)
    elif os.path.isdir(source_value):
        return FileSystemSource(stix_dir=source_value, allow_custom=True)
    else:
        raise ValueError("Source must be a valid URL or directory path.")
