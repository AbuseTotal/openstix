from openstix.filters.presets import (
    SOFTWARE_FILTER,
)


class SoftwareMixin:
    def softwares(self):
        return self.query([SOFTWARE_FILTER])

    def software(self, name, aliases=True):
        return self.query_name_and_alias(filters=[SOFTWARE_FILTER], name=name, aliases=aliases)
