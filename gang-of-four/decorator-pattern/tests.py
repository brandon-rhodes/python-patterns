import os
import sys
import tempfile
import unittest

# Allow modules to be imported from the current directory.
sys.path.insert(0, os.path.dirname(__file__))

import copy_powered_wrapper
import getattr_powered_wrapper
import verbose_static_wrapper

import test.test_file

class AutoTests1(test.test_file.AutoFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return verbose_static_wrapper.AllCapsFileWrapper(normal_file)

    @unittest.skip('TODO: why does this fail?')
    def testReadinto_text(self):
        raise unittest.Skip()

class OtherTests1(test.test_file.OtherFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return verbose_static_wrapper.AllCapsFileWrapper(normal_file)

    @unittest.skip('TODO: make this insensitive to case')
    def testIteration(self):
        raise unittest.Skip()

class AutoTests2(test.test_file.AutoFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return getattr_powered_wrapper.AllCapsFileWrapper(normal_file)

    @unittest.skip('TODO: why does this fail?')
    def testReadinto_text(self):
        raise unittest.Skip()

class OtherTests2(test.test_file.OtherFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return getattr_powered_wrapper.AllCapsFileWrapper(normal_file)

    @unittest.skip('TODO: make this insensitive to case')
    def testIteration(self):
        raise unittest.Skip()

class AutoTests3(test.test_file.AutoFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return copy_powered_wrapper.AllCapsFileWrapper(normal_file)

    @unittest.skip('TODO: why does this fail?')
    def testReadinto_text(self):
        raise unittest.Skip()

class OtherTests3(test.test_file.OtherFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return copy_powered_wrapper.AllCapsFileWrapper(normal_file)

    @unittest.skip('TODO: make this insensitive to case')
    def testIteration(self):
        raise unittest.Skip()

class MyTests(unittest.TestCase):
    def test_thing(self):
        for module in (
                verbose_static_wrapper,
                getattr_powered_wrapper,
        ):
            with tempfile.TemporaryFile('w+') as f:
                w = module.AllCapsFileWrapper(f)
                self.assertEqual(f.newlines, w.newlines)
                with self.assertRaises(AttributeError):
                    w.name = '\n'
                with self.assertRaisesRegex(AttributeError, '.*TextIO.*'):
                    del w.name

                for name in dir(w):
                    if not name.startswith('_') and name not in (
                            'file', 'readinto'):  # TODO: why readinto?
                        getattr(f, name)
