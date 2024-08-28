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

# Add app to the path to prevent errors when commonresources tries to import python_settings
# Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'app')


from app.commonresources import info_i, red_x, green_check


print(info_i()+" linecounter.py by Drew Wingfield")
print(info_i()+" This is intended to be a temporary thing and should be deleted before release.")



def pretty_percent(lines_to_count,total_lines):
    """ Make a percentage from a division, round it to two places """
    return round((lines_to_count/total_lines)*100,2)

path_to_directory = str(os.path.dirname(os.path.realpath(__file__)))

# Get .gitignore files
with open(".gitignore","r") as ignore_file:
    ignore_list = [line for line in ignore_file]

ignore_list = [line.replace("\n","") for line in ignore_list if line!="\n"]
ignore_list = [line[:-1] if line[-1]=="/" else line for line in ignore_list]

# print("Ignore list:")
# for i in ignore_list:
#     print("  - "+str(i))

ignore_list.append(".git")

matches = []
for root, dirnames, filenames in os.walk(path_to_directory):
    # Excluding directories/files from os.walk with help from unutbu on StackOverflow:
    # https://stackoverflow.com/a/19859907/25598210
    # print("BEFORE")
    # print(f"root: {root}")
    # print(f"dirnames: {dirnames}")
    # print(f"filenames: {filenames}")
    
    dirnames[:] = [d for d in dirnames if d not in ignore_list]
    filenames[:] = [f for f in filenames if f not in ignore_list]
    # print("AFTER")
    # print(f"root: {root}")
    # print(f"dirnames: {dirnames}")
    # print(f"filenames: {filenames}")

    for filename in filenames:
        if filename.endswith((".sh",".ps1",".py")):
            matches.append(os.path.join(root, filename))



print(info_i()+f" Found {len(matches)} files in {path_to_directory}.")

visual_counter = 1
total_file_count = len(matches)

total_line_count = 0
line_count_uncommented = 0

lines_with_print_statements = 0
lines_with_if_statements  = 0
lines_with_for_statements = 0
lines_with_indents = 0
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

                if line.startswith("    "):
                    lines_with_indents += 1
                    # Remove the indents so startswith detection works.
                    while "    "==line[:3]:
                        line = line[4:]
                
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
                print(f"\n{red_x()} UnicodeDecode Error! line: '{line}'")
                raise e


    visual_counter+=1



print()
print(green_check()+" Done!")
print(green_check()+f" Read {total_file_count} files.")
print(info_i()+f" Total lines: {total_line_count}")
print(info_i()+f" Non-comment lines: {line_count_uncommented} - {pretty_percent(line_count_uncommented,total_line_count)}% of all lines")
print(info_i()+f" lines with print: {lines_with_print_statements} - {pretty_percent(lines_with_print_statements,line_count_uncommented)}% of code")
print(info_i()+f" lines with 1 or more indents: {lines_with_indents} - {pretty_percent(lines_with_indents,line_count_uncommented)}% of code")
print(info_i()+f" for loops: {lines_with_for_statements}")
print(info_i()+f" functions: {functions}")
print(info_i()+f" classes: {classes}")
print(info_i()+f" todos: {todos}")
print(green_check()+" Program complete.")

# -- END OF FILE --