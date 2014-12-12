import json
import os
import subprocess
import sys

from yoconfigurator.tests import unittest


class TestPublicConfiguration(unittest.TestCase):

    def setUp(self):
        """Call configurator in the public config sample app."""
        tests_dir = os.path.dirname(__file__)
        bin_dir = script_path = os.path.join(tests_dir, '..', '..', 'bin')
        script_path = os.path.join(bin_dir, 'configurator.py')

        self.app_dir = os.path.join(tests_dir, 'samples', 'public-config')
        self.pub_conf = os.path.join(self.app_dir, 'configuration_public.json')

        env = {
            'PATH': os.environ['PATH'],
            'PYTHONPATH': ':'.join(sys.path),
        }
        p = subprocess.Popen(
            (script_path, '--app-dir', self.app_dir, 'myapp', 'myenv'),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=env)
        out, err = p.communicate()
        self.assertEqual(p.wait(), 0)
        self.assertEqual(err, '')

    def tearDown(self):
        os.remove(self.pub_conf)
        os.remove(os.path.join(self.app_dir, 'configuration.json'))

    def test_is_created(self):
        self.assertTrue(os.path.isfile(self.pub_conf))

    def test_looks_as_expected(self):
        expected = {
            'myapp': {
                'some': {
                    'deeply': {
                        'nested': {
                            'value': 'Stefano likes beer'
                        }
                    }
                },
                'hello': 'world',
                'oz': {
                    'bears': True,
                    'tigers': True,
                    'lions': True,
                    'zebras': False,
                }
            }
        }
        with open(self.pub_conf) as f:
            written = json.load(f)
        self.assertEqual(expected, written)

    def test_does_not_contain_a_secret(self):
        with open(self.pub_conf) as f:
            written = json.load(f)
        self.assertNotIn('secret', written)
