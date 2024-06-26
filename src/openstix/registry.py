from stix2.registry import STIX2_OBJ_MAPS


def register_objects(sdos=None, scos=None, markings=None, extensions=None):
    data = {
        "observables": scos if scos else [],
        "objects": sdos if sdos else [],
        "markings": markings if markings else [],
        "extensions": extensions if extensions else [],
    }

    for key, objects in data.items():
        for stix_object in objects:
            STIX2_OBJ_MAPS["2.1"][key].update({stix_object._type: stix_object})
