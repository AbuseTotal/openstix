from openstix.filters import utils
from openstix.filters.presets import (
    CAMPAIGN_FILTER,
)


class CampaignMixin:
    def campaigns(self):
        return self.query([CAMPAIGN_FILTER])

    def campaign(self, name, aliases=True):
        filter_name, filter_aliases = utils.generate_filters_with_name_and_alias(CAMPAIGN_FILTER, name)
        return self.query(filter_name) or self.query(filter_aliases)
