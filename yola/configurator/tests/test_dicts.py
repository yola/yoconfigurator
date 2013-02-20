from ..dicts import DotDict, MissingValue, merge_dicts

from . import unittest


class DotDictTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Python < 2.7 compatibility:
        if not hasattr(cls, 'assertIsInstance'):
            cls.assertIsInstance = lambda self, a, b: self.assertTrue(
                    isinstance(a, b))

    def test_create(self):
        'ensure that we support all dict creation methods'
        by_attr = DotDict(one=1, two=2)
        by_dict = DotDict({'one': 1, 'two': 2})
        by_list = DotDict([['one', 1], ['two', 2]])
        self.assertEqual(by_attr, by_dict)
        self.assertEqual(by_attr, by_list)

    def test_create_tree(self):
        'ensure that nested dicts are converted to DotDicts'
        tree = DotDict({'foo': {'bar': True}})
        self.assertIsInstance(tree['foo'], DotDict)

    def test_list_of_dicts(self):
        'ensure that nested dicts insied lists are converted to DotDicts'
        tree = DotDict({'foo': [{'bar': True}]})
        self.assertIsInstance(tree['foo'][0], DotDict)

    def test_mutablity(self):
        'ensure that the whole tree is mutable'
        tree = DotDict({'foo': {'bar': True}})
        self.assertTrue(tree.foo.bar)
        tree.foo.bar = False
        self.assertFalse(tree.foo.bar)

    def test_setdefault(self):
        'ensure that the setdefault works'
        tree = DotDict({'foo': 'bar'})
        tree.setdefault('baz', {})
        self.assertIsInstance(tree.baz, DotDict)

    def test_update(self):
        'ensure that update works'
        tree = DotDict({'foo': 'bar'})
        tree.update({'foo': {}})
        self.assertIsInstance(tree.foo, DotDict)
        tree.update(bar={})
        self.assertIsInstance(tree.bar, DotDict)
        tree.update([['baz', {}]])
        self.assertIsInstance(tree.baz, DotDict)


class TestMissingValue(unittest.TestCase):
    def test_dict_access(self):
        d = DotDict(foo=MissingValue('foo'))
        self.assertRaises(KeyError, d.foo.get, 'bar')
        self.assertRaises(KeyError, lambda x: x.foo['bar'], d)

    def test_attribute_access(self):
        d = DotDict(foo=MissingValue('foo'))
        self.assertRaises(AttributeError, lambda x: x.foo.bar, d)


class TestMergeDicts(unittest.TestCase):
    def test_merge(self):
        'ensure that the new entries in B are merged into A'
        a = DotDict(a=1, b=1)
        b = DotDict(c=1)
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 1)
        self.assertEqual(c.c, 1)

    def test_replacement(self):
        'ensure that the new entries in B replace equivalents in A'
        a = DotDict(a=1, b=1)
        b = DotDict(b=2)
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)

    def test_sub_merge(self):
        'ensure that a subtree from B is merged with the same subtree in A'
        a = DotDict(a=1, sub={'c': 1})
        b = DotDict(b=2, sub={'d': 2})
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub.c, 1)
        self.assertEqual(c.sub.d, 2)

    def test_sub_replacement(self):
        'ensure that a subtree from B is merged with the same subtree in A'
        a = DotDict(a=1, sub={'c': 1})
        b = DotDict(b=2, sub={'c': 2})
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub.c, 2)

    def test_replace_missing_with_dict(self):
        'ensure that a subtree from B replaces a MissingValue in A'
        a = DotDict(a=1, sub=MissingValue('sub'))
        b = DotDict(b=2, sub={'c': 2})
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub.c, 2)

    def test_merge_lists(self):
        'ensure that leaf lists are merged'
        a = DotDict(a=1, sub=[1, 2])
        b = DotDict(b=2, sub=[3, 4])
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub, [1, 2, 3, 4])
