import json
import os
import types
import sys

from yoconfigurator.dicts import DotDict, MissingValue

try:
    # SourceFileLoader added in Python 3.3
    from importlib.machinery import SourceFileLoader
except ImportError:
    # imp.load_source deprecated in Python 3.3
    from imp import load_source
    _load_module = load_source
else:
    def _load_module(module_name, file_name):
         return SourceFileLoader(module_name, file_name).load_module()


class DetectMissingEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MissingValue):
            raise ValueError('Missing Value found in config: %s' % obj.name)
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
        sys.modules[configs_mod] = types.ModuleType(configs_mod)
    module_name = os.path.basename(config_pathname).rsplit('.', 1)[0]
    module_name = configs_mod + '.' + module_name
    return _load_module(module_name, config_pathname)
