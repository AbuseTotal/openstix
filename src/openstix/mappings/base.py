from openstix import extensions, objects
from openstix.utils import get_object_type

STIX_OBJECTS_MAPPING = {}
STIX_OBJECTS_EXTENSIONS_MAPPING = {}
SCOS_MAPPING = {}
SDOS_MAPPING = {}
SROS_MAPPING = {}
SMOS_MAPPING = {}


def load_objects_mappings(module):
    for object_class_name in dir(module):
        if object_class_name.startswith("__") or object_class_name == "Bundle" or object_class_name.islower():
            continue

        object_class = getattr(module, object_class_name)

        if object_class_name in ["MarkingDefinition", "LanguageContent", "StatementMarking", "TLPMarking"]:
            SMOS_MAPPING[object_class._type] = object_class
            continue

        if object_class_name in ["GranularMarking"]:
            continue

        mapping_type = get_object_type(object_class._type)

        if mapping_type == "sco":
            SCOS_MAPPING[object_class._type] = object_class
            continue

        if mapping_type == "sdo":
            SDOS_MAPPING[object_class._type] = object_class
            continue

        if mapping_type == "sro":
            SROS_MAPPING[object_class._type] = object_class
            continue

        SMOS_MAPPING[object_class._type] = object_class


def load_extensions_mappings(module):
    for extension_class_name in dir(module):
        if extension_class_name.startswith("__") or extension_class_name in ["custom"]:
            continue

        extension_class = getattr(extensions, extension_class_name)

        STIX_OBJECTS_EXTENSIONS_MAPPING[extension_class._type] = extension_class


load_objects_mappings(objects)
load_objects_mappings(objects.custom)
load_extensions_mappings(extensions)

STIX_OBJECTS_MAPPING = SCOS_MAPPING | SDOS_MAPPING | SROS_MAPPING | SMOS_MAPPING
