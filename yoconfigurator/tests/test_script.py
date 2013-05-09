import os
import subprocess
import sys

from . import unittest


class TestScript(unittest.TestCase):
    def test_help(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..',
                                   'bin', 'configurator.py')
        env = {
            'PATH': os.environ['PATH'],
            'PYTHONPATH': ':'.join(sys.path),
        }
        p = subprocess.Popen((script_path, '--help'),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env)
        out, err = p.communicate()
        self.assertEqual(p.wait(), 0)
        self.assertEqual(err, '')
