from stix2.equivalence.graph import graph_equivalence, graph_similarity  # noqa: F401
from stix2.equivalence.object import object_equivalence, object_similarity  # noqa: F401


def generate_possibilities(name):
    chars = [" ", "-", "_"]

    def _generate(value):
        for x in chars:
            for y in chars + [""]:
                item = value.replace(x, y)
                yield item
                yield item.upper()
                yield item.lower()
                yield item.title()

    possibilities = set()

    for a in _generate(name):
        for b in _generate(a):
            possibilities.add(b)

    return list(possibilities)
