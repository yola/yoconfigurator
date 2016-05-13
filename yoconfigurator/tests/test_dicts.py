import copy
import unittest

from yoconfigurator.dicts import (DeletedValue, DotDict, MissingValue,
                                  filter_dict, merge_dicts)


class DotDictTestCase(unittest.TestCase):

    def test_create(self):
        """Ensure that we support all dict creation methods"""
        by_attr = DotDict(one=1, two=2)
        by_dict = DotDict({'one': 1, 'two': 2})
        by_list = DotDict([['one', 1], ['two', 2]])
        self.assertEqual(by_attr, by_dict)
        self.assertEqual(by_attr, by_list)

    def test_create_tree(self):
        """Ensure that nested dicts are converted to DotDicts"""
        tree = DotDict({'foo': {'bar': True}})
        self.assertIsInstance(tree['foo'], DotDict)

    def test_list_of_dicts(self):
        """Ensure that nested dicts insied lists are converted to DotDicts"""
        tree = DotDict({'foo': [{'bar': True}]})
        self.assertIsInstance(tree['foo'][0], DotDict)

    def test_mutablity(self):
        """Ensure that the whole tree is mutable"""
        tree = DotDict({'foo': {'bar': True}})
        self.assertTrue(tree.foo.bar)
        tree.foo.bar = False
        self.assertFalse(tree.foo.bar)

    def test_setdefault(self):
        """Ensure that the setdefault works"""
        tree = DotDict({'foo': 'bar'})
        tree.setdefault('baz', {})
        self.assertIsInstance(tree.baz, DotDict)

    def test_update(self):
        """Ensure that update works"""
        tree = DotDict({'foo': 'bar'})
        tree.update({'foo': {}})
        self.assertIsInstance(tree.foo, DotDict)
        tree.update(bar={})
        self.assertIsInstance(tree.bar, DotDict)
        tree.update([['baz', {}]])
        self.assertIsInstance(tree.baz, DotDict)

    def test_deepcopy(self):
        """Ensure that DotDict can be deepcopied"""
        tree = DotDict({'foo': 'bar'})
        self.assertEqual(tree, copy.deepcopy(tree))

    def test_get_dotted(self):
        """Ensure that DotDict can get values using a dotted key"""
        tree = DotDict({'foo': {'bar': {'baz': 'huzzah'}}})
        self.assertEqual(tree['foo.bar.baz'], 'huzzah')

    def test_set_dotted(self):
        """Ensure that DotDict can set values using a dotted key"""
        tree = DotDict()
        tree['foo.bar.baz'] = 'huzzah'
        self.assertEqual(tree['foo.bar.baz'], 'huzzah')


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
        """Ensure that the new entries in B are merged into A"""
        a = DotDict(a=1, b=1)
        b = DotDict(c=1)
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 1)
        self.assertEqual(c.c, 1)

    def test_filter(self):
        """Ensure that the subset of A is filtered out using keys"""
        a = DotDict(a=1, b=1)
        keys = ['a']
        b = filter_dict(a, keys)
        self.assertEqual(b, {'a': 1})

    def test_replacement(self):
        """Ensure that the new entries in B replace equivalents in A"""
        a = DotDict(a=1, b=1)
        b = DotDict(b=2)
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)

    def test_sub_merge(self):
        """Ensure that a subtree from B is merged with the same subtree in A"""
        a = DotDict(a=1, sub={'c': 1})
        b = DotDict(b=2, sub={'d': 2})
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub.c, 1)
        self.assertEqual(c.sub.d, 2)

    def test_sub_replacement(self):
        """Ensure that a subtree from B is merged with the same subtree in A"""
        a = DotDict(a=1, sub={'c': 1})
        b = DotDict(b=2, sub={'c': 2})
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub.c, 2)

    def test_replace_missing_with_dict(self):
        """Ensure that a subtree from B replaces a MissingValue in A"""
        a = DotDict(a=1, sub=MissingValue('sub'))
        b = DotDict(b=2, sub={'c': 2})
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub.c, 2)

    def test_unnamed_missing_value(self):
        """Ensure that missing values get a name assigned"""
        a = DotDict()
        b = DotDict(foo=MissingValue())
        c = merge_dicts(a, b)
        self.assertEqual(c.foo.name, 'foo')

    def test_unnamed_missing_value_in_new_tree(self):
        """Ensure that missing values in new sub-trees get a name assigned"""
        a = DotDict()
        b = DotDict(foo={'bar': MissingValue()})
        c = merge_dicts(a, b)
        self.assertEqual(c.foo.bar.name, 'foo.bar')

    def test_merge_lists(self):
        """Ensure that leaf lists are merged"""
        a = DotDict(a=1, sub=[1, 2])
        b = DotDict(b=2, sub=[3, 4])
        c = merge_dicts(a, b)
        self.assertEqual(c.a, 1)
        self.assertEqual(c.b, 2)
        self.assertEqual(c.sub, [1, 2, 3, 4])

    def test_merge_incompatible(self):
        """Ensure that the merged items are of the same types"""
        a = DotDict(foo=42)
        b = DotDict(foo='42')
        self.assertRaises(TypeError, merge_dicts, a, b)
        b = DotDict(foo={})
        self.assertRaises(TypeError, merge_dicts, a, b)

    def test_replace_none(self):
        """Ensure that None can be replaced with another type"""
        a = DotDict(foo=None)
        b = DotDict(foo='foo')
        c = merge_dicts(a, b)
        self.assertEqual(c, {'foo': 'foo'})

    def test_deltedvalue(self):
        """Ensure that deletedvalue deletes values"""
        a = DotDict(foo=42)
        b = DotDict(foo=DeletedValue())
        c = merge_dicts(a, b)
        self.assertEqual(c, {})
