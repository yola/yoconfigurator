import json
import os

from .dicts import DotDict


def write_config(config, app_dir):
    path = os.path.join(app_dir, 'configuration.json')
    with open(path, 'w') as f:
        json.dump(config, f, indent=4)


def read_config(app_dir):
    path = os.path.join(app_dir, 'configuration.json')
    with open(path, 'r') as f:
        return DotDict(json.load(f))
