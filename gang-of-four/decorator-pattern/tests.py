import logging
import tempfile
import unittest

#from . import copy_powered_wrapper
from . import getattr_powered_wrapper
from . import verbose_static_wrapper

def wrap(cls, normal_file):
    logger = logging.getLogger('testlog')
    return verbose_static_wrapper.WriteLoggingFile(normal_file, logger)

class BaseCase(unittest.TestCase):
    class_under_test = None

    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        logger = logging.getLogger('testlog')
        return self.class_under_test(normal_file, logger)

class MyTests(BaseCase):
    def test_some_attribute_behaviors(self):
        for cls in (
                verbose_static_wrapper.WriteLoggingFile1,
                getattr_powered_wrapper.WriteLoggingFile3,
        ):
            with tempfile.TemporaryFile('w+') as f:
                logger = logging.getLogger('testlog')
                w = cls(f, logger)
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
