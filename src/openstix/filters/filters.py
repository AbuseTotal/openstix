from stix2.datastore.filters import FilterSet, apply_common_filters


class OrFilterSet(FilterSet):
    """Class to combine multiple filters using logical OR."""

    def apply(self, stix_objs):
        results = []
        for filter_ in self._filters:
            filtered_results = list(apply_common_filters(stix_objs, [filter_]))
            results.extend(filtered_results)
        return results
