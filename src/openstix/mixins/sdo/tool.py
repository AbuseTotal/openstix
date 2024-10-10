from openstix.filters import utils
from openstix.filters.presets import (
    TOOL_FILTER,
)


class ToolMixin:
    def tools(self):
        return self.query([TOOL_FILTER])

    def tool(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(TOOL_FILTER, name)
        return self.query(filter_name) or self.query(filter_aliases)
