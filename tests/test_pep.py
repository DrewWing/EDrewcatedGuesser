

#https://peps.python.org/pep-0008/#imports

import unittest

class pepTset(unittest.TestCase):

    def setUp(self):
        pass

    def single_file_import_format_test(self, file_path):
        with open(file_path, "r", encoding="utf8") as current_file:
            # Iterate over every line
            for line in current_file:
                line = line.rstrip()

                # Remove the indents so startswith detection works.
                if line.startswith("    "):
                    while "    "==line[:3]:
                        line = line[4:]
                
                # If an import is in the line and not a comment
                if not(line.startswith("#")) and "import" in line:
                    assert ("from" in line) or ("," not in line)

    def test_import_format(self):
        import os

        with open(".\\.gitignore","r") as ignore_file:
            ignore_list = [line for line in ignore_file]

        ignore_list = [line.replace("\n","") for line in ignore_list if line!="\n"]
        ignore_list = [line[:-1] if line[-1]=="/" else line for line in ignore_list]
        ignore_list += [".git"]
        ignore_list = [".\\"+i for i in ignore_list]
        print(ignore_list)


        for root, dirnames, filenames in os.walk("."):

            dirnames[:] = [d for d in dirnames if d not in ignore_list]
            filenames[:] = [f for f in filenames if f not in ignore_list]
            
            if root in ignore_list:
                continue

            print(root)

            for file_name in filenames:
                if file_name.endswith(".py") and not(root in ignore_list):
                    file_name = os.path.join(root,file_name)
                    print("    ",file_name)
                    self.single_file_import_format_test(file_name)

if __name__ == '__main__':
    unittest.main()