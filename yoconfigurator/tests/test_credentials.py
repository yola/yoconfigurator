import unittest

from ..credentials import seeded_auth_token


class TestSeededAuthToken(unittest.TestCase):
    def test_seeded_auth(self):
        self.assertEqual(seeded_auth_token(b'foo', b'bar', b'baz'),
                         '5a9350198f854de4b2ab56f187f87707')
