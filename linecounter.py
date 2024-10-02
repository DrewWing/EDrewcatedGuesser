#
# -*- coding: utf-8 -*-

# Linecounter
# Started 2024-06-29
# by Drew Wingfield

# Description:
# Counts the lines of code in a directory

# recursively finding files with help from stackoverflow
# https://stackoverflow.com/questions/2186525/how-to-use-to-find-files-recursively

#region setup
import os
# Add app to the path to prevent errors when commonresources tries to import python_settings
# Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, 'app')


from app.commonresources import info_i, red_x, green_check


print(info_i()+" linecounter.py by Drew Wingfield")
print(info_i()+" This is intended to be a temporary script and should be deleted before release.")


def pretty_percent(lines_to_count,total_lines):
    """ Make a percentage from a division, round it to two places """
    return round((lines_to_count/total_lines)*100,2)

path_to_directory = str(os.path.dirname(os.path.realpath(__file__)))

# Get .gitignore files
print(info_i()+" Getting .gitignore files...")

with open(".gitignore","r") as ignore_file:
    ignore_list = [line for line in ignore_file]

ignore_list = [line.replace("\n","") for line in ignore_list if line!="\n"]
ignore_list = [line[:-1] if line[-1]=="/" else line for line in ignore_list]

# print("Ignore list:")
# for i in ignore_list:
#     print("  - "+str(i))

ignore_list.append(".git")

# Keeps track of statistics per language, such as file and line count.
# I made this dynamic so you can easily add more languages later. You're welcome.
language_stats = {
    "python":{
        "valid extensions":[".py"],
        "lines":0,
        "files":0
    },
    "powershell":{
        "valid extensions":[".ps1"],
        "lines":0,
        "files":0
    },
    "bash":{
        "valid extensions":[".sh"],
        "lines":0,
        "files":0
    },
}

ALL_VALID_EXTENSIONS = []
for language in language_stats.keys():
    ALL_VALID_EXTENSIONS += language_stats[language]["valid extensions"]

#endregion setup

def pretty_percent_bars(percentage:float, total_chars:int =10)->str:
    """ Note: takes in percentage as a float between 0-100 """
    assert 0<=percentage
    assert percentage<=100

    result = "▰"*round((percentage/100)*total_chars)
    result += "▱"*round(total_chars-len(result))
    return result


print(info_i()+" Filtering files and directories...")
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
        if filename.endswith(tuple(ALL_VALID_EXTENSIONS)):
            matches.append(os.path.join(root, filename))



print(green_check()+f" Found {len(matches)} valid files in {path_to_directory}.")

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
                line = line.rstrip() # Remove trailing whitespace

                # Remove indents so startswith detection works.
                if line.startswith("    "):
                    lines_with_indents += 1
                    while "    "==line[:3]:
                        line = line[4:]
                
                total_line_count += 1

                # Total line count for each language
                for language in language_stats.keys():
                    if file_path.endswith(tuple(language_stats[language]["valid extensions"])):
                        language_stats[language]["lines"] += 1
                        break
                
                
                if not(line.startswith("#")):
                    line_count_uncommented +=1

                    if "print(" in line or "Write-Output" in line or line.startswith("echo "):
                        lines_with_print_statements+=1
                    if " if " in line or line.startswith("if "):
                        lines_with_if_statements+=1
                    if " for " in line or line.startswith("for "):
                        lines_with_for_statements+=1
                    if " def " in line or line.startswith("def "):
                        functions+=1
                    if line.startswith("class "):
                        classes+=1
                    if "todo" in line.lower():
                        todos+=1
            
            except UnicodeDecodeError as e:
                print(f"\n{red_x()} UnicodeDecode Error! line: '{line}'")
                raise e


    visual_counter+=1


#region results
print()
print(green_check()+" Done!")
print(green_check()+f" Read {total_file_count} files.")
print(info_i()+f" Total lines: {total_line_count}")
print(info_i()+f"     Non-comment lines:  {line_count_uncommented:<12} {     pretty_percent_bars(100*line_count_uncommented/total_line_count, 12)} {       pretty_percent(line_count_uncommented,total_line_count)}% of all lines")
print(info_i()+f"     Lines with output:  {lines_with_print_statements:<12} {pretty_percent_bars(100*lines_with_print_statements/line_count_uncommented,12)} {pretty_percent(lines_with_print_statements,line_count_uncommented)}% of code")
print(info_i()+f"     Lines with indents: {lines_with_indents:<12} {pretty_percent_bars(100*lines_with_indents/line_count_uncommented,12)} {pretty_percent(lines_with_indents,line_count_uncommented)}% of code")
print(info_i()+f"     For loops: {lines_with_for_statements}")
print(info_i()+f"     Functions: {functions}")
print(info_i()+f"     Classes:   {classes}")
print(info_i()+f"     Todos:     {todos}")
print(info_i())
print(info_i()+" Lines by language")
print(info_i()+f"     Language     : Lines")
for language in language_stats.keys():
    perc = pretty_percent(language_stats[language]['lines'],total_line_count)
    print(info_i()+f"     {language:<13}: {language_stats[language]['lines']:<12} {pretty_percent_bars(perc, 12)} {perc}%")
     
print(green_check()+" Program complete.")
#endregion results

# -- END OF FILE --