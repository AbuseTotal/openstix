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
    def get_threat_actors(self):
        return self._workspace.query([THREAT_ACTOR_FILTER])

    def get_threat_actor(self, name, aliases=True):
        return self._workspace.query_name_and_alias(filters=[THREAT_ACTOR_FILTER], name=name, aliases=aliases)

    def get_intrusion_sets(self):
        return self._workspace.query([INTRUSION_SET_FILTER])

    def get_intrusion_set(self, name, aliases=True):
        return self._workspace.query_name_and_alias(filters=[INTRUSION_SET_FILTER], name=name, aliases=aliases)

    def get_campaigns(self):
        return self._workspace.query([CAMPAIGN_FILTER])

    def get_campaign(self, name, aliases=True):
        return self._workspace.query_name_and_alias(filters=[CAMPAIGN_FILTER], name=name, aliases=aliases)

    def get_malwares(self):
        return self._workspace.query([MALWARE_FILTER])

    def get_malware(self, name, aliases=True):
        return self._workspace.query_name_and_alias(filters=[MALWARE_FILTER], name=name, aliases=aliases)

    def get_tools(self):
        return self._workspace.query([TOOL_FILTER])

    def get_tool(self, name, aliases=True):
        return self._workspace.query_name_and_alias(filters=[TOOL_FILTER], name=name, aliases=aliases)

    def get_couses_of_action(self):
        return self._workspace.query([COURSE_OF_ACTION_FILTER])

    def get_couse_of_action(self, name, aliases=False):
        return self._workspace.query_name_and_alias(filters=[COURSE_OF_ACTION_FILTER], name=name, aliases=aliases)

    def get_softwares(self):
        return self._workspace.query([SOFTWARE_FILTER])

    def get_software(self, name, aliases=True):
        return self._workspace.query_name_and_alias(filters=[SOFTWARE_FILTER], name=name, aliases=aliases)
