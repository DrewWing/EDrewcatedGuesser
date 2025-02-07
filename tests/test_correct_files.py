#
# -*- coding: utf-8 -*-
# Correct Files
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
Provides unit tests validating file and script locations.

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




    
if __name__ == "__main__":
    unittest.main()