import imp
import json
import os
import sys

from yoconfigurator.dicts import DotDict, MissingValue


class DetectMissingEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MissingValue):
            raise ValueError("Missing Value found in config: %s" % obj.name)
        return super(DetectMissingEncoder, self).default(obj)


def write_config(config, app_dir, filename='configuration.json'):
    """Write configuration to the applicaiton directory."""
    path = os.path.join(app_dir, filename)
    with open(path, 'w') as f:
        json.dump(
            config, f, indent=4, cls=DetectMissingEncoder,
            separators=(',', ': '))


def read_config(app_dir):
    path = os.path.join(app_dir, 'configuration.json')
    with open(path, 'r') as f:
        return DotDict(json.load(f))


def get_config_module(config_pathname):
    """Imports the config file to yoconfigurator.configs.<config_basename>."""
    configs_mod = 'yoconfigurator.configs'
    if configs_mod not in sys.modules:
        sys.modules[configs_mod] = imp.new_module(configs_mod)
    module_name = os.path.basename(config_pathname).rsplit('.', 1)[-1]
    module_name = configs_mod + '.' + module_name
    return imp.load_source(module_name, config_pathname)
