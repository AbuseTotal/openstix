import json
from abc import ABC, abstractmethod
from pathlib import Path

from openstix.constants import OPENSTIX_PATH
from openstix.exceptions import DataSourceError
from openstix.toolkit.sinks import FileSystemSink

from ..models import DataSourceConfig


class BaseDownloader(ABC):
    def __init__(self, provider: str, config: DataSourceConfig):
        self.config = config

        self.url = config.url

        provider_path = Path(OPENSTIX_PATH) / provider
        provider_path.mkdir(parents=True, exist_ok=True)

        self.sink = FileSystemSink(
            stix_dir=provider_path,
            allow_custom=True,
        )

        self.counter = 0

    def run(self):
        self.process()
        print(f"Processed and saved {self.counter} STIX objects")

    @abstractmethod
    def process(self):
        pass

    def save(self, bundle: str) -> None:
        bundle = json.loads(bundle)

        for obj in bundle["objects"]:
            if obj["type"] in self.config.ignore_object_types:
                continue

            try:
                self.sink.add(obj)
            except DataSourceError:
                pass

            self.counter += 1

            if self.counter % 1000 == 0:
                print(f"Processed and saved {self.counter} STIX objects")
