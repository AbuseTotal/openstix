from openstix.utils import is_marking, is_sco, is_sdo, is_sro, is_stix_type

__all__ = [
    "class_for_type",
    "get_object_type",
]


def class_for_type(stix_type):
    """Returns the class for a given STIX type.

    Args:
    ----
        stix_type (str): The STIX type to get the class for.

    Returns:
    -------
        class: The class for the given STIX type.

    """
    from openstix.mappings import STIX_OBJECTS_MAPPING

    if is_stix_type(stix_type):
        return STIX_OBJECTS_MAPPING[stix_type]

    raise ValueError("Invalid STIX type: %s" % stix_type)


def get_object_type(stix_object):
    if is_sco(stix_object):
        return "sco"

    if is_sdo(stix_object):
        return "sdo"

    if is_sro(stix_object):
        return "sro"

    if is_marking(stix_object):
        return "smo"

    if hasattr(stix_object, "_type") and stix_object._type.endswith("-ext"):
        return "extension"

    raise ValueError("Invalid STIX object: %s" % stix_object)


def diff(object1, object2):
    dict1 = object1._inner
    dict2 = object2._inner
    return {k: (dict1.get(k), dict2.get(k)) for k in set(dict1) | set(dict2) if dict1.get(k) != dict2.get(k)}
