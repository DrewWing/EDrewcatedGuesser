
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
        self.assertFalse(self.string_contains_both_slashes(common_resources.PATH_TO_FTCAPI))
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