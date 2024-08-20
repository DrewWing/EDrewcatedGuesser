

import unittest
import os

class correctFileTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_app_files(self):
        """
        Makes sure no data (generated) files are in the apps dir outside the generatedfiles dir
        """
        data_extensions = [".json",".csv",".config",".log",".txt",".npy"]
        list_of_app_files = os.listdir("app")

        for extension in data_extensions:
            for file in list_of_app_files:
                self.assertFalse(extension in file, msg=f"A data file of extension {extension} is in the apps folder, with path {file}. It should be in generatedfiles")
    
    def test_generatedfiles_files(self):
        """
        Makes sure no script files are in the generatedfiles dir in the apps dir
        """
        data_extensions = [".ps1",".sh",".py",".java",".cpp"]
        list_of_app_files = os.listdir("app/generatedfiles")

        for extension in data_extensions:
            for file in list_of_app_files:
                self.assertFalse(extension in file, msg=f"A data file of extension {extension} is in the generatedfiles folder, with path {file}. It is a script and should be in app.")

    
if __name__ == '__main__':
    unittest.main()