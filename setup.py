#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

install_requires = []
if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(
    name='yola.configurator',
    description='Configuration Mangling Module for Configs',
    author='Stefano Rivera',
    author_email='stefanor@yola.com',
    url='https://github.com/yola/yola.configurator',
    version="0.2.0dev",
    namespace_packages=['yola'],
    packages=find_packages(),
    scripts=['bin/configurator.py'],
    install_requires=install_requires,
)
