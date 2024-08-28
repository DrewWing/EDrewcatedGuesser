
import unittest
import os
# Add app to the path to prevent errors when commonresources tries to import python_settings
# Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'app')

import commonresources

class CommonResourcesTest(unittest.TestCase):

    def setUp(self):
        pass

    def string_contains_both_slashes(self,st):
        return ("/" in st and "\\" in st)

    def test_slashes(self):
        self.assertFalse(self.string_contains_both_slashes(commonresources.PATH_TO_FTCAPI))
        self.assertFalse(self.string_contains_both_slashes(commonresources.PATH_TO_JOBLIB_CACHE))

if __name__ == '__main__':
    unittest.main()