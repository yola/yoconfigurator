"""Contains methods for filtering configuration."""
import os

from yoconfigurator.base import get_config_module
from yoconfigurator.dicts import DotDict


def filter_config(config, deploy_config):
    """Return a config subset using the filter defined in the deploy config."""
    if not os.path.isfile(deploy_config):
        return DotDict()
    config_module = get_config_module(deploy_config)
    return config_module.filter(config)
