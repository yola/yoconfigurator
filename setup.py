#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "yola.configurator",
    description = "Configuration Mangling Module for DeployConfigs",
    author = 'Stefano Rivera',
    author_email = 'stefanor@yola.com',
    version = "0.1",
    packages = find_packages(),
    scripts = ['bin/configurator.py'],
)
