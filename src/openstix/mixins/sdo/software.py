from openstix.filters import utils
from openstix.filters.presets import (
    SOFTWARE_FILTER,
)


class SoftwareMixin:
    def softwares(self):
        return self.query([SOFTWARE_FILTER])

    def software(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(SOFTWARE_FILTER, name)
        return self.query(filter_name) or self.query(filter_aliases)
