"""Contains methods for creating creating public configuration."""
import json
import os

from yoconfigurator.dicts import DotDict


def get_public_config(config, app_config_dir, app_name):
    """Return the subset of config that is defined as public."""
    public_config_source = os.path.join(app_config_dir, 'public-data.json')

    if not os.path.isfile(public_config_source):
        return False

    with open(public_config_source) as f:
        public_keys = json.load(f)
    config = DotDict(config)
    public_config = DotDict()
    for key in public_keys:
        public_config[key] = config[key]

    return public_config
