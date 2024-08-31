import json

from openstix.toolkit.sinks import load_sink
from openstix.toolkit.sources import load_source


def get_size(obj):
    return len(json.dumps(obj))


def split_objects(objects, max_size):
    bundles = []
    current_bundle = []
    current_size = 0

    for obj in objects:
        obj_size = get_size(obj)
        if current_size + obj_size > max_size:
            bundles.append(current_bundle)
            current_bundle = [obj]
            current_size = obj_size
        else:
            current_bundle.append(obj)
            current_size += obj_size

    if current_bundle:
        bundles.append(current_bundle)

    return bundles


def process(source, sink, send_bundle=False):
    from openstix.objects import Bundle

    source_store = load_source(source)
    sink_store = load_sink(sink)
    objects = source_store.query()

    if send_bundle:
        bundle = Bundle(objects=objects)
        bundle_size = get_size(bundle)

        if bundle_size > 100 * 1024 * 1024:  # 100MB
            bundles = split_objects(objects, 100 * 1024 * 1024)
            for bundle_objects in bundles:
                small_bundle = Bundle(objects=bundle_objects)
                sink_store.add(small_bundle)
        else:
            sink_store.add(bundle)

    else:
        for obj in objects:
            sink_store.add(obj)
