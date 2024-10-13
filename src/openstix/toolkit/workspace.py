from collections import Counter

from stix2 import Environment, MemoryStore

from openstix import utils
from openstix.objects import Bundle
from openstix.toolkit import ObjectFactory
import copy

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

    # This is a modified version of the create method in stix2.Environment
    # As soon as stix2 is updated with our pull request, we can remove this copy.
    def create(self, cls, **kwargs):
        """Create a STIX object using object factory defaults.

        Args:
            cls: the python-stix2 class of the object to be created (eg. Indicator)
            **kwargs: The property/value pairs of the STIX object to be created
        """

        # Use self.defaults as the base, but update with any explicit args
        # provided by the user.
        properties = copy.deepcopy(self._defaults)

        # SCOs do not have these common properties provided by the factory
        if "observables" in cls.__module__:
            properties.pop("created", None)
            properties.pop("created_by_ref", None)
            properties.pop("external_references", None)

        if kwargs:
            if self._list_append:
                # Append provided items to list properties instead of replacing them
                for list_prop in set(self._list_properties).intersection(kwargs.keys(), properties.keys()):
                    kwarg_prop = kwargs.pop(list_prop)
                    if kwarg_prop is None:
                        del properties[list_prop]
                        continue
                    if not isinstance(properties[list_prop], list):
                        properties[list_prop] = [properties[list_prop]]

                    if isinstance(kwarg_prop, list):
                        properties[list_prop].extend(kwarg_prop)
                    else:
                        properties[list_prop].append(kwarg_prop)

            properties.update(**kwargs)

        return cls(**properties)

    def parse_add(self, data, allow_custom=False):
        parsed_data = utils.parse(data, allow_custom)
        if isinstance(parsed_data, Bundle):
            self.add(parsed_data.objects)
        else:
            self.add(parsed_data)

    def create_add(self, cls, **kwargs):
        obj = self.create(cls, **kwargs)
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
