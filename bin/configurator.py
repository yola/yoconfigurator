#!/usr/bin/env python

import argparse
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from yoconfigurator.filter import filter_config
from yoconfigurator.smush import config_sources, smush_config
from yoconfigurator.base import write_config


def main():
    p = argparse.ArgumentParser(
        description="Build a Yola application's configuration.json file")
    p.add_argument('--configs-dir', '-d', metavar='DIRECTORY',
                   action='append',
                   help='Location of Configs. '
                        'Can be specified multiple times. '
                        '(Default: /srv/configs/configs, '
                        '/etc/yola/deployconfigs/chef)')
    p.add_argument('--app-dir', '-a', metavar='DIRECTORY',
                   default='.',
                   help='Location of the application. '
                        'The configuration.json will be written here. '
                        '(Default: .)')
    p.add_argument('--cluster', '-c', metavar='CLUSTER',
                   help='Deployment cluster (Default: None)')
    p.add_argument('--local', '-l', action='store_true',
                   help='Do a second pass, applying -local configuration')
    p.add_argument('--build', '-b', action='store_true',
                   help='Do a third pass, applying -build configuration '
                        '(implies --local)')
    p.add_argument('--dry-run', '-n',
                   action='store_true',
                   help="Display the generated configuration, "
                        "but don't write it.")
    p.add_argument('--verbose', '-v',
                   action='store_true',
                   help="Display the configuration at each step of merging")
    p.add_argument('--hostname', '-H',
                   help='Specify a hostname to refer to (only with --local). '
                        'This gets stuffed into an attribute in the configs '
                        'for the benefit of hostname-local.')
    p.add_argument('app', help='Application name')
    p.add_argument('environment', help='Deployment environment')

    options = p.parse_args()

    if options.build:
        options.local = True

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    if not options.configs_dir:
        options.configs_dir = [
            '/srv/configs/configs',
            '/etc/yola/deployconfigs/chef'
        ]

    app_config = os.path.join(options.app_dir, 'deploy', 'configuration')
    site_config = options.configs_dir
    initial = {
        'yoconfigurator': {
            'app': options.app,
        },
    }
    if options.local:
        site_config.insert(0, os.path.join(options.app_dir, 'deploy',
                                           'configuration', 'local'))
        initial['yoconfigurator']['environment'] = options.environment
        if options.hostname:
            initial['yoconfigurator']['local_hostname'] = options.hostname

    sources = config_sources(options.app, options.environment, options.cluster,
                             site_config, app_config, local=options.local,
                             build=options.build)

    config = smush_config(sources, initial=initial)
    public_filter_pathname = os.path.join(app_config, 'public-data.py')
    pub_config = filter_config(config, public_filter_pathname)

    if options.dry_run:
        json.dump(config, sys.stdout, indent=4, separators=(',', ': '))
        return

    write_config(config, options.app_dir)
    if pub_config:
        write_config(pub_config, options.app_dir, 'configuration_public.json')

if __name__ == '__main__':
    main()
