import json
import os
import shutil
from tempfile import mkdtemp

from ..base import DetectMissingEncoder, read_config, write_configs
from ..dicts import merge_dicts, MissingValue

from . import unittest


class TestDetectMissingEncoder(unittest.TestCase):
    """Not part of the public API"""
    def test_encode(self):
        self.assertEqual('{}', json.dumps({}, cls=DetectMissingEncoder))

    def test_missing(self):
        o = MissingValue('test')
        self.assertRaises(ValueError, json.dumps, o, cls=DetectMissingEncoder)

    def test_other(self):
        o = object()
        self.assertRaises(TypeError, json.dumps, o, cls=DetectMissingEncoder)


class TestReadWriteConfig(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp(prefix='yoconfigurator-test')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_read_config(self):
        config = {'a': 1, 'b': {'c': 2}}
        with open(os.path.join(self.tmpdir, 'configuration.json'), 'w') as f:
            json.dump(config, f)
        parsed = read_config(self.tmpdir)
        self.assertEqual(config, parsed)

    def test_write_single_config(self):
        config = {'a': 1, 'b': {'c': 2}}
        configs = [(config, 'configuration.json')]
        write_configs(self.tmpdir, configs)
        with open(os.path.join(self.tmpdir, 'configuration.json'), 'r') as f:
            parsed = json.load(f)
        self.assertEqual(config, parsed)

    def test_write_multiple_configs(self):
        config_a = {'a': 1, 'b': {'c': 2}}
        config_b = {'x': -1, 'y': {'z': -2}}
        configs = [
            (config_a, 'config-a.json'),
            (config_b, 'config-b.json')]
        write_configs(self.tmpdir, configs)
        second_conf_fn = os.path.join(self.tmpdir, 'config-b.json')
        with open(second_conf_fn) as f:
            parsed = json.load(f)
        self.assertEqual(config_b, parsed)

    def test_missing_value(self):
        config = {'a': 1, 'b': MissingValue('b')}
        configs = [(config, 'config.json')]
        self.assertRaises(ValueError, write_configs, self.tmpdir, configs)

    def test_substituted_missing_value(self):
        config = {'a': 1, 'b': MissingValue('b')}
        config = merge_dicts(config, {'b': 2})
        configs = [(config, 'config.json')]
        write_configs(self.tmpdir, configs)
