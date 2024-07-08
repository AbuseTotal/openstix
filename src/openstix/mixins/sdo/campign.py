from openstix.filters.presets import (
    CAMPAIGN_FILTER,
)


class CampaignMixin:
    def campaigns(self):
        return self.query([CAMPAIGN_FILTER])

    def campaign(self, name, aliases=True):
        return self.query_name_and_alias(filters=[CAMPAIGN_FILTER], name=name, aliases=aliases)
