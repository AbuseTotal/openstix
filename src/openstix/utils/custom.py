from openstix.toolkit.utils import object_equivalence as object_equivalence_datastores
from openstix.toolkit.utils import object_similarity as object_similarity_datastores
from openstix.utils import is_marking, is_sco, is_sdo, is_sro, is_stix_type


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


def object_equivalence(
    obj1,
    obj2,
    prop_scores={},
    threshold=70,
    ignore_spec_version=False,
    versioning_checks=False,
    max_depth=1,
    **weight_dict,
):
    return object_equivalence_datastores(
        obj1,
        obj2,
        prop_scores,
        threshold,
        ignore_spec_version,
        versioning_checks,
        max_depth,
        **weight_dict,
    )


def object_similarity(
    obj1,
    obj2,
    prop_scores={},
    ignore_spec_version=False,
    versioning_checks=False,
    max_depth=1,
    **weight_dict,
):
    return object_similarity_datastores(
        obj1,
        obj2,
        prop_scores,
        ignore_spec_version,
        versioning_checks,
        max_depth,
        **weight_dict,
    )
