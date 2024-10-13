import json
from typing import Any, List

from openstix.objects import Bundle
from openstix.toolkit.sinks import load_sink
from openstix.toolkit.sources import load_source

DEFAULT_MAX_BUNDLE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes


def process(source: str, sink: str, send_bundle: bool = False) -> None:
    """
    Process STIX objects from source to sink.

    Args:
        source (str): Source of STIX objects.
        sink (str): Destination for STIX objects.
        send_bundle (bool): Whether to send objects as a bundle or individually.
    """
    source_store = load_source(source)
    sink_store = load_sink(sink)
    objects = source_store.query()

    processor = process_bundles if send_bundle else add_objects_individually
    processor(sink_store, objects)


def add_objects_individually(sink_store: Any, objects: List[Any]) -> None:
    """Add STIX objects to sink store individually."""
    for obj in objects:
        try:
            sink_store.add(obj)
        except Exception as e:
            raise Exception(f"Failed to add object {obj.id}: {str(e)}")


def process_bundles(sink_store: Any, objects: List[Any]) -> None:
    """Process STIX objects as bundles."""
    max_bundle_size = get_max_bundle_size(sink_store)
    current_bundle = []
    current_size = 0

    for obj in objects:
        obj_size = len(json.dumps(obj.serialize()).encode("utf-8"))
        if current_size + obj_size > max_bundle_size:
            send_bundle(sink_store, current_bundle)
            current_bundle = [obj]
            current_size = obj_size
        else:
            current_bundle.append(obj)
            current_size += obj_size

    if current_bundle:
        send_bundle(sink_store, current_bundle)


def send_bundle(sink_store: Any, objects: List[Any]) -> None:
    """Send a bundle of STIX objects to the sink store."""
    bundle = Bundle(objects=objects, allow_custom=True)
    try:
        sink_store.add(bundle)
    except Exception as e:
        raise Exception(f"Failed to add bundle: {str(e)}")


def get_max_bundle_size(sink_store: Any) -> int:
    """Get maximum bundle size from sink store or use default."""
    return getattr(sink_store, "max_bundle_size", DEFAULT_MAX_BUNDLE_SIZE)
