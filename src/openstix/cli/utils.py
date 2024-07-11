import inspect
import os
from urllib.parse import urlparse

from taxii2client import Collection

from openstix import providers
from openstix.objects import Bundle
from openstix.toolkit.sinks import FileSystemSink, TAXIICollectionSink
from openstix.toolkit.sources import FileSystemSource, TAXIICollectionSource


def get_configs():
    configs = []

    for _, provider in inspect.getmembers(providers, inspect.ismodule):
        if not hasattr(provider, "config"):
            continue

        configs.append(provider.config.CONFIG)

    return configs


def process(provider=None, dataset=None):
    for config in get_configs():
        if provider and provider != config.name:
            continue

        for dataset_config in config.datasets:
            if dataset and dataset != dataset_config.name:
                continue

            for source in dataset_config.sources:
                downloader = providers.SOURCE_CONFIGS_MAPPING.get(source.type)
                downloader(config.name, source).process()


def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_source(source):
    if is_url(source):
        collection = Collection(source)
        return TAXIICollectionSource(collection=collection, allow_custom=True)
    elif os.path.isdir(source):
        return FileSystemSource(stix_dir=source, allow_custom=True)
    else:
        raise ValueError("Source must be a valid URL or directory path.")


def get_sink(sink):
    if is_url(sink):
        collection = Collection(sink)
        return TAXIICollectionSink(collection=collection, allow_custom=True)
    elif os.path.isdir(sink):
        return FileSystemSink(stix_dir=sink, allow_custom=True)
    else:
        raise ValueError("Sink must be a valid URL or directory path.")


def sync(source, sink, send_bundle=False):
    source_store = get_source(source)
    sink_store = get_sink(sink)
    objects = source_store.query()

    if send_bundle:
        bundle = Bundle(objects=objects)
        sink_store.add(bundle)

    else:
        for obj in objects:
            sink_store.add(obj)
