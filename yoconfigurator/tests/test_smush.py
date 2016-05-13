import json
import os
import shutil
import unittest
from tempfile import mkdtemp

from ..dicts import MissingValue
from ..smush import (config_sources, available_sources, smush_config,
                     LenientJSONEncoder)


class TestLenientJSONEncoder(unittest.TestCase):

    """Tests for LenientJSONEncoder.

    Not a part of the public API, only used in debugging, but worth testing
    the behavior
    """

    def test_encode(self):
        self.assertEqual('{}', json.dumps({}, cls=LenientJSONEncoder))

    def test_missing(self):
        expected = '"### MISSING VALUE ###"'
        obj = MissingValue('test')
        self.assertEqual(expected, json.dumps(obj, cls=LenientJSONEncoder))

    def test_unencodable(self):
        obj = object()
        self.assertRaises(TypeError, json.dumps, obj, cls=LenientJSONEncoder)


class TestConfigSources(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp(prefix='yoconfigurator-test')
        self.appdir = os.path.join(self.tmpdir, 'app')
        self.dc1dir = os.path.join(self.tmpdir, 'dc1')
        self.dc2dir = os.path.join(self.tmpdir, 'dc2')
        os.mkdir(self.appdir)
        os.mkdir(self.dc1dir)
        os.mkdir(self.dc2dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def touch(self, name):
        f = open(os.path.join(self.tmpdir, name), 'w')
        f.close()

    def create_sources(self, sources):
        for source in sources:
            self.touch(os.path.join(source[0], source[1] + '.py'))

    def clean_sources(self, sources):
        """Convert a config_sources result into a create_sources list.

        i.e. the last two path components, minus a file extension
        """
        return [tuple(path.rsplit('.', 1)[0].rsplit('/', 2)[1:])
                for path in sources]

    def test_available_sources(self):
        sources = [
            ('dc1', 'common-foo'),
        ]
        self.create_sources(sources)
        # An extra source that won't be present
        all_sources = [
            ([self.dc1dir], 'common-foo'),
            ([self.dc1dir], 'common-foo-bar'),
        ]

        r = available_sources(all_sources)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_source_order(self):
        sources = [
            ('dc1', 'common'),
            ('dc1', 'common-foo'),
            ('dc1', 'common-foo-bar'),
            ('dc1', 'common-overrides'),
            ('app', 'baz-default'),
            ('app', 'baz-foo'),
            ('app', 'baz-foo-bar'),
            ('dc1', 'baz'),
            ('dc1', 'baz-foo'),
            ('dc1', 'baz-foo-bar'),
            ('dc1', 'baz-overrides'),
        ]
        self.create_sources(sources)
        r = config_sources('baz', 'foo', 'bar', [self.dc1dir], self.appdir)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_local_source_order(self):
        sources = [
            ('dc1', 'common'),
            ('dc1', 'common-foo'),
            ('dc1', 'common-foo-bar'),
            ('dc1', 'common-local'),
            ('dc1', 'common-overrides'),
            ('app', 'baz-default'),
            ('app', 'baz-foo'),
            ('app', 'baz-foo-bar'),
            ('dc1', 'baz'),
            ('dc1', 'baz-foo'),
            ('dc1', 'baz-foo-bar'),
            ('app', 'baz-local'),
            ('dc1', 'baz-local'),
            ('dc1', 'baz-overrides'),
        ]
        self.create_sources(sources)
        r = config_sources('baz', 'foo', 'bar', [self.dc1dir], self.appdir,
                           local=True)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_build_source_order(self):
        sources = [
            ('dc1', 'common'),
            ('dc1', 'common-foo'),
            ('dc1', 'common-foo-bar'),
            ('dc1', 'common-local'),
            ('dc1', 'common-build'),
            ('dc1', 'common-overrides'),
            ('app', 'baz-default'),
            ('app', 'baz-foo'),
            ('app', 'baz-foo-bar'),
            ('dc1', 'baz'),
            ('dc1', 'baz-foo'),
            ('dc1', 'baz-foo-bar'),
            ('app', 'baz-local'),
            ('dc1', 'baz-local'),
            ('dc1', 'baz-build'),
            ('dc1', 'baz-overrides'),
        ]
        self.create_sources(sources)
        r = config_sources('baz', 'foo', 'bar', [self.dc1dir], self.appdir,
                           local=True, build=True)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_build_implies_local(self):
        sources = [
            ('dc1', 'common'),
            ('dc1', 'common-foo'),
            ('dc1', 'common-foo-bar'),
            ('dc1', 'common-local'),
            ('dc1', 'common-build'),
            ('dc1', 'common-overrides'),
            ('app', 'baz-default'),
            ('app', 'baz-foo'),
            ('app', 'baz-foo-bar'),
            ('dc1', 'baz'),
            ('dc1', 'baz-foo'),
            ('dc1', 'baz-foo-bar'),
            ('app', 'baz-local'),
            ('dc1', 'baz-local'),
            ('dc1', 'baz-build'),
            ('dc1', 'baz-overrides'),
        ]
        self.create_sources(sources)
        r = config_sources('baz', 'foo', 'bar', [self.dc1dir], self.appdir,
                           local=False, build=True)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_multiple_config_dirs(self):
        sources = [
            ('dc1', 'common-foo'),
            ('dc2', 'common-foo'),
            ('dc2', 'common-overrides')
        ]
        self.create_sources(sources)

        r = config_sources('baz', 'foo', 'bar', [self.dc1dir, self.dc2dir],
                           self.appdir)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_override_config_dirs(self):
        sources = [
            ('dc1', 'common-foo'),
            ('dc2', 'common-foo'),
        ]
        self.create_sources(sources)

        r = config_sources('baz', 'foo', 'bar', [self.dc1dir, self.dc2dir],
                           self.appdir)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)


class TestSmush(unittest.TestCase):

    def setUp(self):
        self.tmpdir = mkdtemp(prefix='yoconfigurator-test')

    def tearDown(self):
        # coverage gets confused if we delete files we've imported into our
        # namespace https://github.com/nose-devs/nose/issues/111
        if 'NO_CLEAN_TESTS' not in os.environ:
            shutil.rmtree(self.tmpdir)

    def test_nop(self):
        c = smush_config([])
        self.assertEqual(c, {})

    def write(self, name, contents):
        """Write contents to tmpdir/name. Return full filename."""
        fn = os.path.join(self.tmpdir, name)
        with open(fn, 'w') as f:
            f.write(contents)
        return fn

    def test_single(self):
        fn = self.write('test.py', """
from yoconfigurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'a': 1})
""")
        c = smush_config([fn])
        self.assertEqual(c, {'a': 1})

    def test_initial(self):
        fn = self.write('test.py', """
from yoconfigurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'a': 2})
""")
        c = smush_config([fn], initial={'a': 1})
        self.assertEqual(c, {'a': 2})

    def test_multiple(self):
        a = self.write('a.py', """
from yoconfigurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'a': 1})
""")
        b = self.write('b.py', """
from yoconfigurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'b': 2})
""")
        c = smush_config([a, b])
        self.assertEqual(c, {'a': 1, 'b': 2})

    def test_missing_value(self):
        a = self.write('a.py', """
from yoconfigurator.dicts import MissingValue, merge_dicts

def update(config):
    return merge_dicts(config, {'a': MissingValue('a')})
""")
        b = self.write('b.py', """
from yoconfigurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'a': 1})
""")
        c = smush_config([a, b])
        self.assertEqual(c, {'a': 1})
