#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

install_requires = []
if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(
    name='yoconfigurator',
    description='Configuration Mangling Module for Configs',
    author='Stefano Rivera',
    author_email='stefano.rivera@yola.com',
    url='https://github.com/yola/yoconfigurator',
    version='0.4.1',
    packages=find_packages(),
    scripts=['bin/configurator.py'],
    install_requires=install_requires,
    test_suite='yoconfigurator.tests',
)
