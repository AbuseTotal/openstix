from openstix.filters.presets import (
    COURSE_OF_ACTION_FILTER,
)


class MitigationMixin:
    def mitigations(self):
        return self.query([COURSE_OF_ACTION_FILTER])

    def mitigation(self, name, aliases=False):
        return self.query_name_and_alias(filters=[COURSE_OF_ACTION_FILTER], name=name, aliases=aliases)
