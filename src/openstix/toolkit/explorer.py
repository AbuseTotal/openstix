from openstix.filters import Filter, utils
from openstix.filters.presets import (
    CAMPAIGN_FILTER,
    COURSE_OF_ACTION_FILTER,
    INTRUSION_SET_FILTER,
    MALWARE_FILTER,
    SOFTWARE_FILTER,
    THREAT_ACTOR_FILTER,
    TOOL_FILTER,
)


class CommonExplorerMixin:
    def get(self, id):
        return self._workspace.query_one_or_none(Filter("id", "=", id))

    def get_threat_actors(self):
        return self._workspace.query([THREAT_ACTOR_FILTER])

    def get_threat_actor(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(THREAT_ACTOR_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_intrusion_sets(self):
        return self._workspace.query([INTRUSION_SET_FILTER])

    def get_intrusion_set(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(INTRUSION_SET_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_campaigns(self):
        return self._workspace.query([CAMPAIGN_FILTER])

    def get_campaign(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(CAMPAIGN_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_malwares(self):
        return self._workspace.query([MALWARE_FILTER])

    def get_malware(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(MALWARE_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_tools(self):
        return self._workspace.query([TOOL_FILTER])

    def get_tool(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(TOOL_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_couses_of_action(self):
        return self._workspace.query([COURSE_OF_ACTION_FILTER])

    def get_couse_of_action(self, name, aliases=False):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(COURSE_OF_ACTION_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)

    def get_softwares(self):
        return self._workspace.query([SOFTWARE_FILTER])

    def get_software(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(SOFTWARE_FILTER, name)
        return self._workspace.query_one_or_none(filter_name) or self._workspace.query_one_or_none(filter_aliases)
