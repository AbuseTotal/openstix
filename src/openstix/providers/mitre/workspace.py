from openstix.providers.mitre.mixin import Mixin
from openstix.toolkit.workspace import Workspace


class MITREWorkspace(Workspace):
    def __init__(self, store=None):
        super().__init__(store)
        self.mitre = Mixin(self)
