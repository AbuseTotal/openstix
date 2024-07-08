from openstix.filters.presets import (
    TOOL_FILTER,
)


class ToolMixin:
    def tools(self):
        return self.query([TOOL_FILTER])

    def tool(self, name, aliases=True):
        return self.query_name_and_alias(filters=[TOOL_FILTER], name=name, aliases=aliases)
