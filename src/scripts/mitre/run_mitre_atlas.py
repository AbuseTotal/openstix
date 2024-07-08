import os

from stix2 import Environment

from openstix import OPENSTIX_PATH
from openstix.providers.mitre.workspace import MITREWorkspace
from openstix.toolkit.sinks import FileSystemSink
from openstix.toolkit.sources import FileSystemSource
from openstix.toolkit.stores import MemoryStore

enviroment = Environment(
    source=FileSystemSource(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            "mitre",
            "atlas",
        ),
        allow_custom=True,
    ),
    sink=FileSystemSink(
        stix_dir=os.path.join(
            OPENSTIX_PATH,
            "mitre",
            "atlas",
        ),
        allow_custom=True,
    ),
)

store = MemoryStore(
    stix_data=enviroment.source.query(),
)

workspace = MITREWorkspace(store=store)

items = workspace.mitre.tactics()

print(items[0])
