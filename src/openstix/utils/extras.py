from urllib.parse import urlparse


def is_url(path):
    try:
        result = urlparse(path)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


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
