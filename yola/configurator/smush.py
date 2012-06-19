import imp
import os
import sys

from .dicts import DotDict


def config_sources(app, environment, cluster, deployconfigs_dirs, app_dir):
    '''Return a list of the configuration files used by app in the specified
    environment+cluster
    '''
    sources = [
        # Global
        (deployconfigs_dirs, 'common'),
        # Environment + Cluster
        (deployconfigs_dirs, 'common-%s' % environment),
        (deployconfigs_dirs, 'common-%s-%s' % (environment, cluster)),
        # Machine-specific overrides
        (deployconfigs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-default' % app),
        (deployconfigs_dirs, app),
        (deployconfigs_dirs, '%s-%s' % (app, environment)),
        (deployconfigs_dirs, '%s-%s-%s' % (app, environment, cluster)),
        # Application override
        (deployconfigs_dirs, '%s-overrides' % app),
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
    if 'yola.config' not in sys.modules:
        sys.modules['yola.config'] = imp.new_module('yola.config')
    config = DotDict()
    for fn in sources:
        mod_name = 'yola.config.' + os.path.basename(fn).rsplit('.', 1)[-1]
        description = ('.py', 'r', imp.PY_SOURCE)
        with open(fn) as f:
            m = imp.load_module(mod_name, f, fn, description)
            config = m.update(config)
    return config
