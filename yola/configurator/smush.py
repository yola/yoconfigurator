import imp
import json
import logging
import os
import sys

from .dicts import DotDict


log = logging.getLogger('yola.configurator.smush')


def config_sources(app, environment, cluster, configs_dirs, app_dir):
    '''Return a list of the configuration files used by app in the specified
    environment+cluster
    '''
    sources = [
        # Environment + Cluster
        (configs_dirs, 'common-%s' % environment),
        (configs_dirs, 'common-%s-%s' % (environment, cluster)),
        # Global
        (configs_dirs, 'common'),
        # Machine-specific overrides
        (configs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-default' % app),
        (configs_dirs, '%s-%s' % (app, environment)),
        (configs_dirs, '%s-%s-%s' % (app, environment, cluster)),
        # Application override
        (configs_dirs, '%s-overrides' % app),
    ]
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
        log.debug('Current config:\n%s', json.dumps(config, indent=4))
    return config
