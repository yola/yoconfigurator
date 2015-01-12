#!/usr/bin/env python

import sys

from setuptools import setup, find_packages

install_requires = []
if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(
    name='yoconfigurator',
    description='Build configuration for deployable apps',
    author='Yola',
    author_email='engineers@yola.com',
    license='MIT (Expat)',
    url='https://github.com/yola/yoconfigurator',
    version='0.4.6',
    packages=find_packages(),
    scripts=['bin/configurator.py'],
    install_requires=install_requires,
    test_suite='yoconfigurator.tests',
)
