import io
import os

from stix2 import v20, v21
from stix2.datastore import DataSink  # noqa: F401
from stix2.datastore.filesystem import (
    FileSystemSink,  # noqa: F401
    _timestamp2filename,
)
from stix2.datastore.memory import MemorySink  # noqa: F401
from stix2.datastore.taxii import TAXIICollectionSink  # noqa: F401
from stix2.serialization import fp_serialize
from taxii2client import Collection

from openstix.exceptions import DataSourceError
from openstix.utils.extras import is_url

__all__ = [
    "load_sink",
    "DataSink",
    "FileSystemSink",
    "FileSystemSinkEnhanced",
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

# This is a modified version of FileSystemSink that uses pretty=False in fp_serialize
# As soon as stix2 is updated with our pull request, we can remove this copy.
class FileSystemSinkEnhanced(FileSystemSink):
    def _check_path_and_write(self, stix_obj, encoding="utf-8"):
        """Write the given STIX object to a file in the STIX file directory."""
        type_dir = os.path.join(self._stix_dir, stix_obj["type"])

        # All versioned objects should have a "modified" property.
        if "modified" in stix_obj:
            filename = _timestamp2filename(stix_obj["modified"])
            obj_dir = os.path.join(type_dir, stix_obj["id"])
        else:
            filename = stix_obj["id"]
            obj_dir = type_dir

        file_path = os.path.join(obj_dir, filename + ".json")

        if not os.path.exists(obj_dir):
            os.makedirs(obj_dir)

        if self.bundlify:
            if "spec_version" in stix_obj:
                # Assuming future specs will allow multiple SDO/SROs
                # versions in a single bundle we won't need to check this
                # and just use the latest supported Bundle version.
                stix_obj = v21.Bundle(stix_obj, allow_custom=self.allow_custom)
            else:
                stix_obj = v20.Bundle(stix_obj, allow_custom=self.allow_custom)

        if os.path.isfile(file_path):
            raise DataSourceError("Attempted to overwrite file (!) at: {}".format(file_path))

        with io.open(file_path, mode="w", encoding=encoding) as f:
            fp_serialize(stix_obj, f, pretty=False, encoding=encoding, ensure_ascii=False)
