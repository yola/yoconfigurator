"""A configration filter for public data."""

from yoconfigurator.dicts import DotDict


def filter(config):
    """The subset of configuration keys to be made public."""
    keys = [
        "myapp.hello",
        "myapp.some.deeply.nested.value",
        "myapp.oz"
    ]
    public_config = DotDict()
    for key in keys:
        public_config[key] = config[key]
    return public_config
