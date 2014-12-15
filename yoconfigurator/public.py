"""Contains methods for creating creating public configuration."""
import imp
import os

from yoconfigurator.dicts import DotDict


def read_public_data_config(fn):
    """Return the config keys to be published as public."""
    if not os.path.isfile(fn):
        return []
    m = imp.load_source('public-config', fn)
    return m.public_data


def get_public_config(config, app_config_dir, app_name):
    """Return the subset of config that is defined as public."""
    public_config_fn = os.path.join(app_config_dir, 'public-data.py')
    public_data_keys = read_public_data_config(public_config_fn)
    public_config = DotDict()

    for key in public_data_keys:
        public_config[key] = config[key]

    return public_config
