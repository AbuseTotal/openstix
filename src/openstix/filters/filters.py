from stix2.datastore.filters import FilterSet, _check_filter_components, apply_common_filters, collections


class OrFilterSet(FilterSet):
    """Class to combine multiple filters using logical OR."""

    def apply(self, stix_objs):
        results = []
        for filter_ in self._filters:
            filtered_results = list(apply_common_filters(stix_objs, [filter_]))
            results.extend(filtered_results)
        return results


class Filter(collections.namedtuple("Filter", ["property", "op", "value", "case_insensitive"])):
    """STIX 2 filters that support the querying functionality of STIX 2
    DataStores and DataSources.

    Initialized like a Python tuple.

    Args:
        property (str): filter property name, corresponds to STIX 2 object property
        op (str): operator of the filter
        value (str): filter property value
        case_insensitive (bool): indicates if the filter should be case-insensitive

    Example:
        Filter("id", "=", "malware--0f862b01-99da-47cc-9bdb-db4a86a95bb1", True)

    """

    __slots__ = ()

    def __new__(cls, prop, op, value, case_insensitive=False):
        # If value is a list, convert it to a tuple so it is hashable.
        if isinstance(value, list):
            value = tuple(value)

        _check_filter_components(prop, op, value)

        self = super(Filter, cls).__new__(cls, prop, op, value, case_insensitive)
        return self

    def _check_property(self, stix_obj_property):
        """Check a property of a STIX Object against this filter.

        Args:
            stix_obj_property: value to check this filter against

        Returns:
            True if property matches the filter,
            False otherwise.
        """
        filter_value = self.value

        if self.case_insensitive:
            if isinstance(stix_obj_property, str):
                stix_obj_property = stix_obj_property.lower()
            if isinstance(filter_value, str):
                filter_value = filter_value.lower()

        if self.op == "=":
            return stix_obj_property == filter_value
        elif self.op == "!=":
            return stix_obj_property != filter_value
        elif self.op == "in":
            return stix_obj_property in filter_value
        elif self.op == "contains":
            if isinstance(filter_value, dict):
                return filter_value in stix_obj_property.values()
            else:
                return filter_value in stix_obj_property
        elif self.op == ">":
            return stix_obj_property > filter_value
        elif self.op == "<":
            return stix_obj_property < filter_value
        elif self.op == ">=":
            return stix_obj_property >= filter_value
        elif self.op == "<=":
            return stix_obj_property <= filter_value
        else:
            raise ValueError(
                "Filter operator: {0} not supported for specified property: {1}".format(self.op, self.property)
            )
