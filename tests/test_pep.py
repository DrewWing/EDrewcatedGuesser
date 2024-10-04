

#https://peps.python.org/pep-0008/#imports

import unittest

class pepTset(unittest.TestCase):

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
                if line.startswith("    "):
                    while "    "==line[:3]:
                        line = line[4:]
                
                # Remove all trailing comments
                if "#" in line:
                    line = line[:line.index("#")]
                
                # If an import is in the line and not a comment
                if (line.startswith("import ")):
                    try:
                        assert ("from" in line) or ("," not in line) # See the below error message for details.
                    
                    except AssertionError as e:
                        raise AssertionError(f"PEP 8 nonconformity (importing more than one module in one line) at line {current_line} in file {file_path} \n Line: {line}")

    def test_import_format(self):
        import os

        with open(".\\.gitignore","r") as ignore_file:
            ignore_list = [line for line in ignore_file]

        ignore_list = [line.replace("\n","").replace(".\\","") for line in ignore_list if line!="\n"]
        ignore_list = [line[:-1] if line[-1]=="/" else line for line in ignore_list]
        ignore_list += [".git"]
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
                    self.single_file_import_format_test(file_name)
            
        #print("All files:") #DEBUG
        #rint(all_files) #DEBUG

if __name__ == '__main__':
    unittest.main()