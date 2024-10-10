from openstix.filters import utils
from openstix.filters.presets import (
    INTRUSION_SET_FILTER,
)


class IntrusionSetMixin:
    def intrusion_sets(self):
        return self.query([INTRUSION_SET_FILTER])

    def intrusion_set(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(INTRUSION_SET_FILTER, name)
        return self.query(filter_name) or self.query(filter_aliases)
