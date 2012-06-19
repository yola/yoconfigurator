import imp
import os
import sys

from .dicts import DotDict


def config_sources(app, environment, cluster, deployconfigs_dirs, app_dir):
    '''Return a list of the configuration files used by app in the specified
    environment+cluster
    '''
    sources = [
        # Environment + Cluster
        (deployconfigs_dirs, 'common-%s' % environment),
        (deployconfigs_dirs, 'common-%s-%s' % (environment, cluster)),
        # Global
        (deployconfigs_dirs, 'common'),
        # Machine-specific overrides
        (deployconfigs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-default' % app),
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

    # Create a fake module that we can import the configuration-generating
    # modules into
    fake_mod = 'yola.configurator.configs'
    if fake_mod not in sys.modules:
        sys.modules[fake_mod] = imp.new_module(fake_mod)

    config = DotDict()
    for fn in sources:
        mod_name = fake_mod + '.' + os.path.basename(fn).rsplit('.', 1)[-1]
        description = ('.py', 'r', imp.PY_SOURCE)
        with open(fn) as f:
            m = imp.load_module(mod_name, f, fn, description)
            config = m.update(config)
    return config
