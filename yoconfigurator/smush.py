import imp
import json
import logging
import os
import sys

from .dicts import DotDict, MissingValue


log = logging.getLogger(__name__)


class LenientJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MissingValue):
            return '### MISSING VALUE ###'
        return super(LenientJSONEncoder, self).default(obj)


def config_sources(app, environment, cluster, configs_dirs, app_dir,
                   local=False):
    '''Return a list of the configuration files used by app in the specified
    environment+cluster
    '''

    sources = [
        # Machine-specific
        (configs_dirs, 'hostname'),
        (configs_dirs, 'hostname-local'),
        # Global
        (configs_dirs, 'common'),
        # Environment + Cluster
        (configs_dirs, 'common-%s' % environment),
        (configs_dirs, 'common-%s-%s' % (environment, cluster)),
        (configs_dirs, 'common-local'),
        # Machine-specific overrides
        (configs_dirs, 'common-overrides'),
        # Application-specific
        ([app_dir], '%s-default' % app),
        ([app_dir], '%s-%s' % (app, environment)),
        ([app_dir], '%s-%s-%s' % (app, environment, cluster)),
        (configs_dirs, app),
        (configs_dirs, '%s-%s' % (app, environment)),
        (configs_dirs, '%s-%s-%s' % (app, environment, cluster)),
        ([app_dir], '%s-local' % app),
        (configs_dirs, '%s-local' % app),
        # Machine-specific application override
        (configs_dirs, '%s-overrides' % app),
    ]

    # Filter out local sources
    if not local:
        sources = [source for source in sources
                   if not source[1].endswith('-local')]

    return available_sources(sources)


def available_sources(sources):
    '''Yield the sources that are present'''
    for dirs, name in sources:
        for directory in dirs:
            fn = os.path.join(directory, name) + '.py'
            if os.path.isfile(fn):
                yield fn


def smush_config(sources, initial=None):
    '''Merge the configuration files specified, and return the resulting
    DotDict
    '''

    # Create a fake module that we can import the configuration-generating
    # modules into
    fake_mod = '%s.configs' % __name__
    if fake_mod not in sys.modules:
        sys.modules[fake_mod] = imp.new_module(fake_mod)

    if initial is None:
        initial = {}
    config = DotDict(initial)

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
