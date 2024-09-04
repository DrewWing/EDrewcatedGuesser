

import unittest
import os

class correctFileTest(unittest.TestCase):

    def setUp(self):
        pass

    def no_extensions_in_directory(self, extensions, dirpath, msg="A file isn't where it should be."):
        list_of_files = os.listdir(dirpath)

        for extension in extensions:
            for file in list_of_files:
                self.assertFalse(extension == os.path.splitext(file)[1], msg=msg+f" - Extension  {extension} with path {file}.")


    def test_app_files(self):
        """
        Makes sure no data (generated) files are in the apps dir outside the generatedfiles dir
        """
        data_extensions = [".json",".csv",".config",".log",".txt",".npy"]
        self.no_extensions_in_directory(extensions=data_extensions, dirpath="app",msg="Data (generated) file is in the apps dir! Should be in generatedfilesdir.")
    
    def test_generatedfiles_files(self):
        """
        Makes sure no script files are in the generatedfiles dir in the apps dir
        """
        script_extensions = [".ps1",".sh",".py",".java",".cpp"]
        self.no_extensions_in_directory(script_extensions,"app/generatedfiles","A script is in the generatedfiles dir! It should be in apps!")
    
    def test_markdown_files(self):
        """
        Makes sure no markdown files are anywhere but the root directory
        """
        markdown_extensions = [".md"]
        self.no_extensions_in_directory(markdown_extensions, "app","A markdown file is in apps! It should be somewhere else!")
        self.no_extensions_in_directory(markdown_extensions, "app/generatedfiles","A markdown file is in generatedfiles! It should be somewhere else!")




    
if __name__ == '__main__':
    unittest.main()