#
# -*- coding: utf-8 -*-
# Test Imports
# 
# by Drew Wingfield
#
# This script is part of Drew Wingfield's EDrewcated Guesser.
# It is licensed under the license found at LICENSE.txt.
# See the documentation in the README.md file.
#
"""
Provides unit tests for external and internal imports.

This script is part of Drew Wingfield's EDrewcated Guesser.
It is licensed under the license found at LICENSE.txt.
See the documentation in the README.md file.

Unit tests for external imports include builtins as well as true externals 
(pandas, googleapiclient, etc.). Unit tests for internal imports make suree
that internal scripts can be imported correctly.
"""

import unittest

class importsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_external_imports(self):
        try:
            import sys
            import os
            import json
            import joblib
            import numpy
            import pandas
            import datetime
            import pathlib
            import pickle

            # Google API stuff
            from google.oauth2 import service_account
            import google.auth.exceptions
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError

        except ImportError as e:
            raise AssertionError(e) # Error while importing builtins. Do you have the Venv setup correctly?


    def test_internal_imports(self):
        # Add app to the path to prevent errors when commonresources tries to import python_settings
        # Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
        import sys
        # Caution: path[0] is reserved for script path (or "" in REPL)
        sys.path.insert(1, "app")

        try:
            import common_resources
            import OPR
            import json_parse
            import init_settings #TODO: this uses argparse, fix this test later
            import sheets_api #TODO: fix this one too
        
        except ImportError as e:
            raise AssertionError(e)



if __name__ == "__main__":
    unittest.main()