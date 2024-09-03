
import unittest

class importsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_external_imports(self):
        try:
            import pandas
            import joblib
            import numpy
            from google.oauth2 import service_account
            import google.auth.exceptions
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError

        except ImportError as e:
            raise AssertionError(e)


    def test_internal_imports(self):
        # Add app to the path to prevent errors when commonresources tries to import python_settings
        # Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
        import sys
        # caution: path[0] is reserved for script path (or '' in REPL)
        sys.path.insert(1, 'app')

        try:
            import commonresources
            import OPR
            import jsonparse
            #import init_settings #TODO: this uses argparse, fix this test later
            #import sheetsapi #TODO: fix this one too
        
        except ImportError as e:
            raise AssertionError(e)



if __name__ == '__main__':
    unittest.main()