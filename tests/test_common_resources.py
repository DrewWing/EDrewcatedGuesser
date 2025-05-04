#
# -*- coding: utf-8 -*-
# Test Common Resources
# 
# by Drew Wingfield
#
# Copyright (C) 2024, Drew Wingfield
#
# This script is part of EDrewcated Guesser by Drew Wingfield.
# EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
# the terms of the AGNU Affero General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the AGNU Affero General Public License for more details.
#
# You should have received a copy of the AGNU Affero General Public License along with 
# EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.
#
# See the documentation in the README.md file.
#
"""
Provides unit tests validating functions and variables in common_resources.py

See the documentation in the README.md file.

Copyright (C) 2024, Drew Wingfield

This script is part of EDrewcated Guesser by Drew Wingfield.
EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
the terms of the AGNU Affero General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the AGNU Affero General Public License for more details.

You should have received a copy of the AGNU Affero General Public License along with 
EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.

"""


import unittest
import os
# Add app to the path to prevent errors when commonresources tries to import python_settings
# Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
import sys
# caution: path[0] is reserved for script path (or "" in REPL)
sys.path.insert(1, "app")

import common_resources

class CommonResourcesTest(unittest.TestCase):

    def setUp(self):
        pass

    def string_contains_both_slashes(self, st: str) -> bool:
        """ Returns boolean for if the given string contains forwardslash and backslash. """
        return ("/" in st and "\\" in st)

    def test_slashes(self):
        """ Make sure that the paths don't contain both forwardslashes and backslashes """
        self.assertFalse(self.string_contains_both_slashes(common_resources.PROJECT_PATH))
        self.assertFalse(self.string_contains_both_slashes(common_resources.PATH_TO_JOBLIB_CACHE))
    
    def test_byte_to_gb(self):
        self.assertEqual(common_resources.byte_to_gb(1000000000),1)
        self.assertEqual(common_resources.byte_to_gb(1234567890),1.2346) # rounds to 4 digits

    def test_get_json(self):
        with open("get_json_test.json","w+") as file:
            file.write(
                '{"schedule":[{"description":"Semifinal 1 Match 1","field":"1","tournamentLevel":"SEMIFINAL"}]}'
                )
        
        
        data = common_resources.get_json("get_json_test.json")
        self.assertTrue(type(data)==type({"this is":"a dictionary"}))
        self.assertEqual(data,{"schedule":[{"description":"Semifinal 1 Match 1","field":"1","tournamentLevel":"SEMIFINAL"}]})
        os.remove("get_json_test.json")

if __name__ == "__main__":
    unittest.main()