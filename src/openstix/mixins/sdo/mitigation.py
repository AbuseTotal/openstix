from openstix.filters import utils
from openstix.filters.presets import (
    COURSE_OF_ACTION_FILTER,
)


class MitigationMixin:
    def mitigations(self):
        return self.query([COURSE_OF_ACTION_FILTER])

    def mitigation(self, name, aliases=False):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(COURSE_OF_ACTION_FILTER, name)
        return self.query(filter_name) or self.query(filter_aliases)
