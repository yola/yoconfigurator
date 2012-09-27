import imp
import json
import logging
import os
import sys

from .dicts import DotDict, MissingValue


log = logging.getLogger('yola.configurator.smush')


class LenientJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MissingValue):
            return '### MISSING VALUE ###'
        return super(LenientJSONEncoder, self).default(obj)


def config_sources(app, environment, cluster, configs_dirs, app_dir):
    '''Return a list of the configuration files used by app in the specified
    environment+cluster
    '''
    sources = [
        # Machine-specific
        (configs_dirs, 'hostname'),
        # Global
        (configs_dirs, 'common'),
        # Environment + Cluster
        (configs_dirs, 'common-%s' % environment),
        (configs_dirs, 'common-%s-%s' % (environment, cluster)),
        # Machine-specific overrides
        (configs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-default' % app),
        ([app_dir], '%s-%s' % (app, environment)),
        ([app_dir], '%s-%s-%s' % (app, environment, cluster)),
        (configs_dirs, app),
        (configs_dirs, '%s-%s' % (app, environment)),
        (configs_dirs, '%s-%s-%s' % (app, environment, cluster)),
        # Machine-specific application override
        (configs_dirs, '%s-overrides' % app),
    ]
    return available_sources(sources)


def local_config_sources(app, configs_dirs, app_dir):
    '''Return an extra list of configuration files that should be applied
    after config_sources, when worknig locally
    '''
    environment = 'local'
    sources = [
        # Environment
        (configs_dirs, 'common-%s' % environment),
        # Machine-specific overrides
        (configs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-%s' % (app, environment)),
        (configs_dirs, '%s-%s' % (app, environment)),
        # Machine-specific application override
        (configs_dirs, '%s-overrides' % app),
    ]
    return available_sources(sources)


def available_sources(sources):
    '''Yield the sources that are present'''
    for dirs, name in sources:
        for directory in dirs:
            fn = os.path.join(directory, name) + '.py'
            if os.path.isfile(fn):
                yield fn
                break


def smush_config(sources):
    '''Merge the configuration files specified, and return the resulting
    DotDict
    '''

    # Create a fake module that we can import the configuration-generating
    # modules into
    fake_mod = 'yola.configurator.configs'
    if fake_mod not in sys.modules:
        sys.modules[fake_mod] = imp.new_module(fake_mod)

    config = DotDict()
    for fn in sources:
        log.debug('Merging %s', fn)
        mod_name = fake_mod + '.' + os.path.basename(fn).rsplit('.', 1)[-1]
        description = ('.py', 'r', imp.PY_SOURCE)
        with open(fn) as f:
            m = imp.load_module(mod_name, f, fn, description)
            config = m.update(config)
        log.debug('Current config:\n%s', json.dumps(config, indent=4,
                                                    cls=LenientJSONEncoder))
    return config
