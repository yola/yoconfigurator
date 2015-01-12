"""A configration filter for public data."""

from yoconfigurator.dicts import filter_dict


def filter(config):
    """The subset of configuration keys to be made public."""
    keys = [
        "myapp.hello",
        "myapp.some.deeply.nested.value",
        "myapp.oz"
    ]
    return filter_dict(config, keys)
