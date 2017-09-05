import logging
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

def wrap(cls, normal_file):
    logger = logging.getLogger('testlog')
    return verbose_static_wrapper.WriteLoggingFile(normal_file, logger)

class BaseCase(unittest.TestCase):
    class_under_test = None

    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        logger = logging.getLogger('testlog')
        return self.class_under_test(normal_file, logger)

class AutoTests1(test.test_file.AutoFileTests, BaseCase):
    class_under_test = verbose_static_wrapper.WriteLoggingFile

    @unittest.skip('TODO: why does this fail?')
    def testReadinto_text(self):
        raise unittest.Skip()

class OtherTests1(test.test_file.OtherFileTests, BaseCase):
    class_under_test = verbose_static_wrapper.WriteLoggingFile

class AutoTests2(test.test_file.AutoFileTests, BaseCase):
    class_under_test = getattr_powered_wrapper.WriteLoggingFile

    @unittest.skip('TODO: why does this fail?')
    def testReadinto_text(self):
        raise unittest.Skip()

class OtherTests2(test.test_file.OtherFileTests, BaseCase):
    class_under_test = getattr_powered_wrapper.WriteLoggingFile

# class AutoTests3(test.test_file.AutoFileTests, BaseCase):
#     def open(self, *args, **kw):
#         normal_file = open(*args, **kw)
#         return copy_powered_wrapper.WriteLoggingFile(normal_file)


#     @unittest.skip('TODO: why does this fail?')
#     def testReadinto_text(self):
#         raise unittest.Skip()

# class OtherTests3(test.test_file.OtherFileTests, BaseCase):

#     # @unittest.skip('TODO: make this insensitive to case')
#     # def testIteration(self):
#     #     raise unittest.Skip()

class MyTests(BaseCase):
    def test_some_attribute_behaviors(self):
        for module in (
                verbose_static_wrapper,
                getattr_powered_wrapper,
        ):
            with tempfile.TemporaryFile('w+') as f:
                logger = logging.getLogger('testlog')
                w = module.WriteLoggingFile(f, logger)
                self.assertEqual(f.newlines, w.newlines)
                with self.assertRaisesRegex(AttributeError, '.*TextIO.*'):
                    # Make sure at least one access is really going back
                    # to the file class (the 'closed' attr in particular
                    # has a delete error that mentions the class name)
                    del w.closed
                for attr in ('closed', 'encoding', 'errors',
                             'name', 'newlines'):  # 'mode' is writable
                    with self.assertRaises(AttributeError):
                        setattr(w, attr, '\n')
                    with self.assertRaises(AttributeError):
                        delattr(w, attr)

                for name in dir(w):
                    if not name.startswith('_') and name not in (
                            # TODO: why readinto?
                            'file', 'logger', 'readinto'):
                        getattr(f, name)
