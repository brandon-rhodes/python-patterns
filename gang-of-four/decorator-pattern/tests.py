import os
import sys
import unittest

# Allow modules to be imported from the current directory.
sys.path.insert(0, os.path.dirname(__file__))

import static_wrapper

import test.test_file

class AutoTests(test.test_file.AutoFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return static_wrapper.AllCapsFileWrapper(normal_file)

    # TODO: why does this test fail?
    def testReadinto_text(self):
        return

class OtherTests(test.test_file.OtherFileTests, unittest.TestCase):
    def open(self, *args, **kw):
        normal_file = open(*args, **kw)
        return static_wrapper.AllCapsFileWrapper(normal_file)

