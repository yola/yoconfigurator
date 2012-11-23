#!/usr/bin/env python

import argparse
import itertools
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from yola.configurator.smush import (config_sources, local_config_sources,
                                     smush_config)
from yola.configurator.base import write_config


def main():
    p = argparse.ArgumentParser(
            description="Build a Yola application's configuration.json file")
    p.add_argument('--configs-dir', '-d', metavar='DIRECTORY',
                   action='append',
                   help='Location of Configs. '
                        'Can be specified multiple times.'
                        '(Default: /srv/configs,/etc/yola/deployconfigs/chef)')
    p.add_argument('--app-dir', '-a', metavar='DIRECTORY',
                   default='.',
                   help='Location of the application. '
                        'The configuration.json will be written here. '
                        '(Default: .)')
    p.add_argument('--cluster', '-c', metavar='CLUSTER',
                   help='Deployment cluster (Default: None)')
    p.add_argument('--local', '-l', action='store_true',
                   help='Do a second pass, applying -local configuration')
    p.add_argument('--dry-run', '-n',
                   action='store_true',
                   help="Display the generated configuration, "
                        "but don't write it.")
    p.add_argument('--verbose', '-v',
                   action='store_true',
                   help="Display the configuration at each step of merging")
    p.add_argument('app', help='Application name')
    p.add_argument('environment', help='Deployment environment')

    options = p.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    if not options.configs_dir:
        options.configs_dir = ['/srv/configs', '/etc/yola/deployconfigs/chef']

    app_config = os.path.join(options.app_dir, 'deploy', 'configuration')
    site_config = options.configs_dir
    if options.local:
        site_config.insert(0, os.path.join(options.app_dir, 'deploy',
                                           'configuration', 'local'))

    sources = config_sources(options.app, options.environment, options.cluster,
                             site_config, app_config)
    if options.local:
        sources = itertools.chain(sources,
                local_config_sources(options.app, site_config, app_config))

    config = smush_config(sources)

    if not options.dry_run:
        write_config(config, options.app_dir)
    else:
        json.dump(config, sys.stdout, indent=4)


if __name__ == '__main__':
    main()
