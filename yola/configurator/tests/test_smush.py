import os
import shutil
from tempfile import mkdtemp

from ..smush import config_sources, smush_config

from . import unittest


class TestConfigSources(unittest.TestCase):
    def setUp(self):
        self.tmpdir = mkdtemp(prefix='yola-configurator-test')
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
        '''Convert a config_sources result into a create_sources list
        i.e. the last two path components, minus a file extension
        '''
        return [tuple(path.rsplit('.', 1)[0].rsplit('/', 2)[1:])
                for path in sources]

    def test_source_order(self):
        sources = [
            ('dc1', 'common-foo'),
            ('dc1', 'common-foo-bar'),
            ('dc1', 'common'),
            ('dc1', 'common-overrides'),
            ('app', 'baz-default'),
            ('app', 'baz-foo'),
            ('app', 'baz-foo-bar'),
            ('dc1', 'baz-foo'),
            ('dc1', 'baz-foo-bar'),
            ('dc1', 'baz-overrides'),
        ]
        self.create_sources(sources)
        r = config_sources('baz', 'foo', 'bar', [self.dc1dir], self.appdir)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_multiple_config_dirs(self):
        sources = [
            ('dc1', 'common-foo'),
            ('dc2', 'common-overrides')
        ]
        self.create_sources(sources)
        # An extra source that'll be overridden by dc1:
        self.create_sources([('dc2', 'common-foo')])

        r = config_sources('baz', 'foo', 'bar', [self.dc1dir, self.dc2dir],
                           self.appdir)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)

    def test_override_config_dirs(self):
        sources = [
            ('dc1', 'common-foo'),
        ]
        self.create_sources(sources)
        self.create_sources([('dc2', 'common-foo')])

        r = config_sources('baz', 'foo', 'bar', [self.dc1dir, self.dc2dir],
                           self.appdir)
        r = self.clean_sources(r)
        self.assertEqual(r, sources)


class TestSmush(unittest.TestCase):

    def setUp(self):
        self.tmpdir = mkdtemp(prefix='yola-configurator-test')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_nop(self):
        c = smush_config([])
        self.assertEqual(c, {})

    def write(self, name, contents):
        '''Write contents to tmpdir/name. Return full filename'''
        fn = os.path.join(self.tmpdir, name)
        with open(fn, 'w') as f:
            f.write(contents)
        return fn

    def test_single(self):
        fn = self.write('test.py', """
from yola.configurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'a': 1})
""")
        c = smush_config([fn])
        self.assertEqual(c, {'a': 1})

    def test_multiple(self):
        a = self.write('a.py', """
from yola.configurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'a': 1})
""")
        b = self.write('b.py', """
from yola.configurator.dicts import merge_dicts

def update(config):
    return merge_dicts(config, {'b': 2})
""")
        c = smush_config([a, b])
        self.assertEqual(c, {'a': 1, 'b': 2})
