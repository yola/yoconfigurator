import json
import os

from .dicts import DotDict, MissingValue


class DetectMissingEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MissingValue):
            raise ValueError("Missing Value found in config: %s" % obj.name)
        return super(DetectMissingEncoder, self).default(obj)


def write_config(config, app_dir):
    path = os.path.join(app_dir, 'configuration.json')
    with open(path, 'w') as f:
        json.dump(config, f, indent=4, cls=DetectMissingEncoder)


def read_config(app_dir):
    path = os.path.join(app_dir, 'configuration.json')
    with open(path, 'r') as f:
        return DotDict(json.load(f))
