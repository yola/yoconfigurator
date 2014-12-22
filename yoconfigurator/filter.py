"""Contains methods for filtering configuration."""
import os

from yoconfigurator.base import get_config_module
from yoconfigurator.dicts import DotDict


def filter_config(config, pathname):
    """Return the config keys to be published as public."""
    print pathname
    if not os.path.isfile(pathname):
        return DotDict()
    config_module = get_config_module('public-config', pathname)
    return config_module.filter(config)
