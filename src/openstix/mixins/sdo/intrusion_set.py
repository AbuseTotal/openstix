from openstix.filters.presets import (
    INTRUSION_SET_FILTER,
)


class IntrusionSetMixin:
    def intrusion_sets(self):
        return self.query([INTRUSION_SET_FILTER])

    def intrusion_set(self, name, aliases=True):
        return self.query_name_and_alias(filters=[INTRUSION_SET_FILTER], name=name, aliases=aliases)
