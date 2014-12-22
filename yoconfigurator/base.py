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


def _write(content, path):
    with open(path, 'w') as f:
        json.dump(
            content, f, indent=2, cls=DetectMissingEncoder,
            separators=(',', ': '))


def write_config(app_dir, config, pub_config=None):
    """Write configuration to the applicaiton directory."""
    _write(config, os.path.join(app_dir, 'configuration.json'))
    if pub_config:
        _write(pub_config, os.path.join(app_dir, 'configuration_public.json'))


def read_config(app_dir):
    path = os.path.join(app_dir, 'configuration.json')
    with open(path, 'r') as f:
        return DotDict(json.load(f))


def get_config_module(module_name, config_pathname):
    """Imports the config file to yoconfigurator.configs.<module_name>."""
    configs_mod = 'yoconfigurator.configs'
    if configs_mod not in sys.modules:
        sys.modules[configs_mod] = imp.new_module(configs_mod)
    module_name = configs_mod + '.' + module_name
    return imp.load_source(module_name, config_pathname)
