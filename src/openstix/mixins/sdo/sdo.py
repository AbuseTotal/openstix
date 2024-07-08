from .intrusion_set import IntrusionSetMixin
from .campign import CampaignMixin
from .malware import MalwareMixin
from .mitigation import MitigationMixin
from .software import SoftwareMixin
from .tool import ToolMixin
from .vulnerabilities import VulnerabilitiesMixin
from .locations import LocationsMixin
from .industries import IndustriesMixin

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