#
# -*- coding: utf-8 -*-
# Test PEP
# 
# by Drew Wingfield
#
# This script is part of Drew Wingfield's EDrewcated Guesser.
# It is licensed under the license found at LICENSE.txt.
# See the documentation in the README.md file.
#
"""
Provides unit tests for PEP style guides and conventions on Python scripts.

This script is part of Drew Wingfield's EDrewcated Guesser.
It is licensed under the license found at LICENSE.txt.
See the documentation in the README.md file.

Unit tests for trailing commas, multiple imports in one line, and other PEP
nonconformities as well as conventions for every Python script.
"""


import unittest

correct_python_header = [ # Starting lines of the python header. ~ANY~ can be replaced with anything.
    "#\n",
    "# -*- coding: utf-8 -*-\n",
    "# ~ANY~\n", # Title of program
    "# ~ANY~\n", # Started (date), or nothing if date unkown
    "# by Drew Wingfield\n",
    "#\n",
    "# This script is part of Drew Wingfield's EDrewcated Guesser.\n",
    "# It is licensed under the license found at LICENSE.txt.\n",
    "# See the documentation in the README.md file.\n",
    "#\n",
    '"""\n',
    "~ANY~\n", # Brief description.
    "\n",
    "This script is part of Drew Wingfield's EDrewcated Guesser.\n",
    "It is licensed under the license found at LICENSE.txt.\n",
    "See the documentation in the README.md file.\n",
    "\n"
]

def remove_leading_indents(line):
    while "    "==line[:3]:
        line = line[4:]

    return line

class pepTest(unittest.TestCase):

    def setUp(self):
        pass

    def single_file_import_format_test(self, file_path):
        with open(file_path, "r", encoding="utf8") as current_file:
            # Iterate over every line
            current_line = 0

            for line in current_file:
                current_line += 1
                line = line.rstrip()

                # Remove the indents so startswith detection works.
                line = remove_leading_indents(line)
                
                # Remove all trailing comments
                if "#" in line:
                    line = line[:line.index("#")]
                
                # If an import is in the line and not a comment
                if (line.startswith("import ")):
                    try:
                        assert ("from" in line) or ("," not in line) # See the below error message for details.
                    
                    except AssertionError as e:
                        raise AssertionError(f"PEP 8 nonconformity (importing more than one module in one line) at line {current_line} in file {file_path} \n Line: {line}")

    def single_file_header_test(self, file_path):
        with open(file_path, "r", encoding="utf8") as current_file:
            # Iterate over every line
            current_line = 0
            file_lines = current_file.readlines()

            for correct_line in correct_python_header:
                current_line += 1
                line = file_lines[current_line-1]

                line_is_correct = bool(correct_line == line)

                if not(line_is_correct) and ("~ANY~" in correct_line):
                    line_is_correct = bool(
                            correct_line[:correct_line.index("~ANY~")]==line[:correct_line.index("~ANY~")]
                        and correct_line[correct_line.index("~ANY~")+5:]==correct_line[correct_line.index("~ANY~")+5:]
                        )
                
                # If an import is in the line and not a comment
                try:
                    assert line_is_correct # See the below error message for details.
                    
                except AssertionError as e:
                    raise AssertionError(f"Header nonconformity at line {current_line} in file {file_path} \nHeader is {line.strip()} but should be {correct_line.strip()}")
                
    def single_file_trailing_commas_test(self, file_path):
        with open(file_path, "r", encoding="utf8") as current_file:
            # Iterate over every line
            current_line = 0

            for line in current_file:
                current_line += 1
                line = line.rstrip()
                
                # Remove all trailing comments
                if "#" in line:
                    line = line[:line.index("#")]
                
                # If an import is in the line and not a comment
                try:
                    assert not(",)" in line or ",]" in line or ",}" in line) or ("test_pep" in file_path) # See the below error message for details.
                    
                except AssertionError as e:
                    raise AssertionError(f"PEP 8 nonconformity (no whitespace between traling comma and close parentheses) at line {current_line} in file {file_path} \n Line: {line}")
    
    def test_python_files(self, test_function=None):
        """ Iterates through all Python files in project and tests using a test function. """
        import os
        
        # If the test function is none, return 0.
        # Because the unittest module auto-runs functions staring with "test_"
        # and we call this function later to test all files.
        if test_function==None:
            return None

        with open(".\\.gitignore","r") as ignore_file:
            ignore_list = [line for line in ignore_file]

        ignore_list = [line.replace("\n","").replace(".\\","") for line in ignore_list if line!="\n"]
        ignore_list = [line[:-1] if line[-1]=="/" else line for line in ignore_list]
        ignore_list += [".git"]
        ignore_list = list(set(ignore_list)) # Remove duplicates
        #print(ignore_list) #DEBUG

        #all_files = [] #DEBUG

        for root, dirnames, filenames in os.walk(".", topdown=True): # Topdown=true means that changes to dirnames and filenames modify in place

            dirnames[:] = [d for d in dirnames if d not in ignore_list]
            filenames[:] = [f for f in filenames if f not in ignore_list]
            
            #all_files += dirnames #DEBUG
        
            #print("Root:",root) #DEBUG

            for file_name in filenames:
                if file_name.endswith(".py") and not(root in ignore_list):
                    file_name = os.path.join(root,file_name)
                    #print("    ",file_name) #DEBUG
                    test_function(file_name)
            
        #print("All files:") #DEBUG
        #print(all_files) #DEBUG

    def test_import_formats(self):
        self.test_python_files(test_function=self.single_file_import_format_test)

    def test_trailing_commas(self):
        self.test_python_files(test_function=self.single_file_trailing_commas_test)

    def test_headers(self):
        self.test_python_files(test_function=self.single_file_header_test)

if __name__ == '__main__':
    unittest.main()