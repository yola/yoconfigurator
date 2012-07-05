import os
import subprocess

from . import unittest


class TestScript(unittest.TestCase):
    def test_help(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                                   'bin', 'configurator.py')
        p = subprocess.Popen((script_path, '--help'),
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.assertEqual(p.wait(), 0)
        self.assertEqual(err, '')
