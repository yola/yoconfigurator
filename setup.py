#!/usr/bin/env python

from setuptools import setup, find_packages


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
    test_suite='yoconfigurator.tests',
)
