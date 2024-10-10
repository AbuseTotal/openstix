from .campaign import CampaignMixin
from .industries import IndustriesMixin
from .intrusion_set import IntrusionSetMixin
from .locations import LocationsMixin
from .malware import MalwareMixin
from .mitigation import MitigationMixin
from .software import SoftwareMixin
from .tool import ToolMixin
from .vulnerabilities import VulnerabilitiesMixin


class SDOMixin(
    IntrusionSetMixin,
    CampaignMixin,
    MalwareMixin,
    MitigationMixin,
    SoftwareMixin,
    ToolMixin,
    VulnerabilitiesMixin,
    LocationsMixin,
    IndustriesMixin,
):
    pass
