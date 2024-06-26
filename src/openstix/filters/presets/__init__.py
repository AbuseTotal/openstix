from stix2.datastore.filters import Filter

from openstix.mappings import SCOS_MAPPING, SDOS_MAPPING, SROS_MAPPING


def __generate_preset_filters():
    object_types = [key for mapping in [SROS_MAPPING, SDOS_MAPPING, SCOS_MAPPING] for key in mapping]

    data = {}

    for object_type in object_types:
        constant = object_type.replace("-", "_").upper() + "_FILTER"
        data[constant] = Filter("type", "=", object_type)

    return data


globals().update(__generate_preset_filters())
