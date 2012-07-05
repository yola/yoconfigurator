import json
import os
import shutil
from tempfile import mkdtemp

from ..base import read_config, write_config
from ..dicts import merge_dicts, MissingValue

from . import unittest


class TestReadWriteConfig(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp(prefix='yola-configurator-test')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_read_config(self):
        config = {'a': 1, 'b': {'c': 2}}
        with open(os.path.join(self.tmpdir, 'configuration.json'), 'w') as f:
            json.dump(config, f)
        parsed = read_config(self.tmpdir)
        self.assertEqual(config, parsed)

    def test_write_config(self):
        config = {'a': 1, 'b': {'c': 2}}
        write_config(config, self.tmpdir)
        with open(os.path.join(self.tmpdir, 'configuration.json'), 'r') as f:
            parsed = json.load(f)
        self.assertEqual(config, parsed)

    def test_missing_value(self):
        config = {'a': 1, 'b': MissingValue('b')}
        self.assertRaises(ValueError, write_config, config, self.tmpdir)

    def test_substituted_missing_value(self):
        config = {'a': 1, 'b': MissingValue('b')}
        config = merge_dicts(config, {'b': 2})
        write_config(config, self.tmpdir)
