#
# -*- coding: utf-8 -*-

# Linecounter
# Started 2024-06-29
# by Drew Wingfield

# Description:
# Counts the lines of code in a directory

# recursively finding files with help from stackoverflow
# https://stackoverflow.com/questions/2186525/how-to-use-to-find-files-recursively

import os
import fnmatch

# Add app to the path to prevent errors when commonresources tries to import python_settings
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'app')


from app.commonresources import info_i, red_x, green_check


print(info_i()+" linecounter.py by Drew Wingfield")
print(info_i()+" This is intended to be a temporary thing and should be deleted before release.")

path_to_directory = str(os.path.dirname(os.path.realpath(__file__)))

matches = []
for root, dirnames, filenames in os.walk(path_to_directory):
    for filename in filenames:
        if filename.endswith((".sh",".ps1",".py")):
            matches.append(os.path.join(root, filename))



print(info_i()+f" Found {len(matches)} files in {path_to_directory}.")

visual_counter = 1
total_file_count = len(matches)

total_line_count = 0
line_count_uncommented = 0

lines_with_print_statements = 0
lines_with_if_statements = 0
lines_with_for_statements = 0
functions = 0
classes   = 0
todos     = 0

# Iterate over every file
for file_path in matches:
    # display output
    print(info_i()+f" {visual_counter}/{total_file_count} - {file_path}        ",end='\r')
    with open(file_path, "r", encoding="utf8") as current_file:
        # Iterate over every line
        for line in current_file:
            try:
                line = line.rstrip()
                if line.startswith("#"):
                    total_line_count +=1
                
                else:
                    total_line_count +=1
                    line_count_uncommented +=1

                    if "print(" in line:
                        lines_with_print_statements+=1
                    if "if " in line:
                        lines_with_if_statements+=1
                    if "for " in line:
                        lines_with_for_statements+=1
                    if "def " in line:
                        functions+=1
                    if line.startswith("class "):
                        classes+=1
                    if "todo" in line.lower():
                        todos+=1
            
            except UnicodeDecodeError as e:
                print(line)
                raise e


    visual_counter+=1



print()
print(green_check()+" Done!")
print(info_i()+f" Read {total_file_count} files.")
print(info_i()+f" Total lines: {total_line_count}")
print(info_i()+f" Non-comment lines: {line_count_uncommented} - {round(line_count_uncommented/total_line_count,4)*100}% of all lines")
print(info_i()+f" lines with print: {lines_with_print_statements} - {round((lines_with_print_statements/line_count_uncommented)*100,2)}% of code")
print(info_i()+f" for loops: {lines_with_for_statements}")
print(info_i()+f" functions: {functions}")
print(info_i()+f" classes: {classes}")
print(info_i()+f" todos: {todos}")

# -- END OF FILE --