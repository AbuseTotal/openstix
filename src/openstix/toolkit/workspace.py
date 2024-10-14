from collections import Counter

from stix2 import Environment, MemoryStore

from openstix import utils
from openstix.objects import Bundle
from openstix.toolkit import ObjectFactory


class Workspace(Environment):
    """Extends the `stix2.Environment` class to provide a customized environment for handling
    STIX objects in a workspace context. Offers functionality for creating, querying, and
    removing STIX objects, including handling multiple versions of objects.
    """

    def __init__(self, factory=None, store=None, source=None, sink=None):
        factory = factory or ObjectFactory()
        if not source and not sink:
            store = store or MemoryStore()
        super().__init__(factory=factory, store=store, source=source, sink=sink)

    def parse_add(self, data, allow_custom=False):
        parsed_data = utils.parse(data, allow_custom)
        if isinstance(parsed_data, Bundle):
            self.add(parsed_data.objects)
        else:
            self.add(parsed_data)

    def create_add(self, cls, **kwargs):
        obj = super().create(cls, **kwargs)
        self.add(obj)
        return obj

    def get_or_none(self, stix_id):
        try:
            return self.get(stix_id)
        except Exception:
            return None

    def query_one_or_none(self, filters=None):
        filters = filters if filters else []
        objects = self.query(filters)
        return objects[0] if objects else None

    def query(self, query=None, last_version_only=True):
        all_objects = super().query(query or [])
        return (
            all_objects
            if not last_version_only
            else list({obj.id: obj for obj in reversed(all_objects)}.values())
        )

    def stats(self, query=None):
        return Counter(obj.type for obj in self.query(query))
