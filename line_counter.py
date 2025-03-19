#
# -*- coding: utf-8 -*-
# Line Counter
# Started 2024-06-29
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
Counts the lines of code in a directory

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


Recursively finding files with help from stackoverflow: 
https://stackoverflow.com/questions/2186525/how-to-use-to-find-files-recursively
"""

#region setup
import os

# Add app to the path to prevent errors when commonresources tries to import python_settings
# Taken from Cameron on StackOverflow: https://stackoverflow.com/a/4383597/25598210
import sys
# caution: path[0] is reserved for script path (or "" in REPL)
sys.path.insert(1, "app")


from common_resources import info_i, red_x, green_check

DO_GRAPH = True # Whether to use matplotlib to create a nested pie chart and save it to languages.png

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
# Add duplicates of all items with backslashes for Windows support
ignore_list += [line.replace("/","\\") for line in ignore_list] 

# print("Ignore list:")
# for i in ignore_list:
#     print("  - "+str(i))

ignore_list.append(".git") # Ignore all git files

# Keeps track of statistics per language, such as file and line count.
# I made this dynamic so you can easily add more languages later. You're welcome.
class Language():
    def __init__(self, name:str, extensions: list, 
                 displayname:str=None, category:str="Code",
                 comment_start:str="#", comment_multi_line_start:str="", comment_multi_line_end:str="",
                 indent="    "):
        
        # Identifier variables
        self.name = name
        self.displayname = str(displayname if displayname!=None else name)
        self.extensions = extensions
        self.category = category
        
        # Counter variables
        self.files = 0 # Total number of files of this language
        self.lines = 0 # Total number of lines of this language
        self.lines_uncommented = 0
        self.lines_output = 0
        self.lines_if  = 0 # If statements
        self.lines_for = 0 # For statements
        self.lines_indented = 0 # Lines with one or more indentation
        self.functions = 0
        self.classes   = 0
        self.todos     = 0

        # Analyze variables
        self.comment_start = comment_start
        self.comment_multi_line_start = comment_multi_line_start
        self.comment_multi_line_end   = comment_multi_line_end
        self.indent = indent # The sequence of spaces/tabs for indentation, default four spaces

    
    def analyze_file(self, file_path) -> None:
        is_block_comment = False
        with open(file_path, "r", encoding="utf8") as current_file:
            # Iterate over every line
            for line in current_file:
                try:
                    line = line.rstrip() # Remove trailing whitespace

                    # Remove indents so startswith detection works.
                    if line.startswith(self.indent):
                        self.lines_indented += 1
                        while line.startswith(self.indent):
                            line = line[4:]
                    
                    self.lines += 1

                    if self.comment_multi_line_start!="" and self.comment_multi_line_end!="":
                        if line.startswith(self.comment_multi_line_start):
                            is_block_comment = True
                        
                        elif line.startswith(self.comment_multi_line_end):
                            is_block_comment = False
                    
                    if not(line.startswith(self.comment_start) and self.comment_start!="") and not(is_block_comment):
                        self.lines_uncommented +=1

                        if (   "print(" in line 
                            or "Write-Output" in line 
                            or line.strip().startswith("echo ") 
                            or line.strip().startswith("logging.debug")
                            or line.strip().startswith("logging.info")
                            or line.strip().startswith("logging.warn")
                            or line.strip().startswith("logging.error")
                            or line.strip().startswith("logging.critical")
                            or line.strip().startswith("logging.exception")
                            ):
                            self.lines_output+=1
                        
                        if " if " in line or line.startswith("if "):
                            self.lines_if+=1
                        if " for " in line or line.startswith("for "):
                            self.lines_for+=1
                        if " def " in line or line.startswith("def "):
                            self.functions+=1
                        if line.startswith("class "):
                            self.classes+=1
                        if "todo" in line.lower():
                            self.todos+=1
                
                except UnicodeDecodeError as e:
                    print(f"\n{red_x()} UnicodeDecode Error! line: '{line}'")
                    raise e
        
        assert is_block_comment==False


def detect_language(file_path: str, languages:list):
    # Iterate through all languages
    for language in languages:
        # Go through all extensions in each language
        for extension in language.extensions:
            # If the path ends in the proper extension
            if file_path.endswith(extension):
                return language # Return the correct language class
    
    raise RuntimeError(f"Found no language (out of {languages}) for a file path {file_path}")


all_languages = [
    Language("python",      [".py"],  displayname="Python"),
    Language("powershell",  [".ps1"], displayname="PowerShell", comment_multi_line_start="<#",comment_multi_line_end="#>"),
    Language("bash",        [".sh"],  displayname="BASH"),
    Language("markdown",    [".md"],  displayname="Markdown", category="Other", comment_start=""),
    Language("c",    [".c"],  displayname="C", comment_start="//", comment_multi_line_start="/*", comment_multi_line_end="*/"),
    Language("java",         [".java"], displayname="Java",        comment_start="//", comment_multi_line_start="/*", comment_multi_line_end="*/"),
    Language("cplusplus",    [".cpp"],  displayname="C++",         comment_start="//", comment_multi_line_start="/*", comment_multi_line_end="*/"),
    Language("csharp",       [".cs"],   displayname="C#",          comment_start="//", comment_multi_line_start="/*", comment_multi_line_end="*/"),
    Language("javascript",   [".js"],   displayname="JavaScript",  comment_start="//", comment_multi_line_start="/*", comment_multi_line_end="*/"),
    Language("yaml",         [".yaml"], displayname="YAML", category="Config", comment_start="#"),
    Language("txt",         [".txt"], displayname="Plain Text", category="Other", comment_start=""),
    Language("config",      [".config"],  displayname="Configuration", category="Config", comment_start=""),
]

all_extensions = []
for language in all_languages:
    all_extensions += language.extensions

#endregion setup

def pretty_percent_bars(percentage:float, total_chars:int =10)->str:
    """ Note: takes in percentage as a float between 0-100 """
    assert 0<=percentage
    assert percentage<=100

    result = "▰"*round((percentage/100)*total_chars)
    result += "▱"*round(total_chars-len(result))
    return result

def is_ignored(root:str, ignore_list:list)->bool:
    for ignore_path in ignore_list:
        if ignore_path in root:
            return True
        
    return False


print(info_i()+" Filtering files and directories...")
matches = []
for root, dirnames, filenames in os.walk(path_to_directory):
    # Excluding directories/files from os.walk with help from unutbu on StackOverflow:
    # https://stackoverflow.com/a/19859907/25598210
    if not (is_ignored(root, ignore_list)):
        # print(info_i()+" BEFORE") #DEBUG
        # print(info_i()+f"    root: {root}")
        # print(info_i()+f"    dirnames: {dirnames}")
        # print(info_i()+f"    filenames: {filenames}")
        dirnames[: ] = [d for d in dirnames if not is_ignored(d, ignore_list)]
        filenames[:] = [f for f in filenames if not is_ignored(f, ignore_list)]
        # print(info_i()+" AFTER") #DEBUG
        # print(info_i()+f"    root: {root}")
        # print(info_i()+f"    dirnames: {dirnames}")
        # print(info_i()+f"    filenames: {filenames}")

        for filename in filenames:
            if filename.endswith(tuple(all_extensions)):
                matches.append(os.path.join(root, filename))
    
    #else: #DEBUG
    #    print(info_i()+f"Ignored root {root}")



print(green_check()+f" Found {len(matches)} valid files in {path_to_directory}.")

visual_counter = 1
total_file_count = len(matches)

# Iterate over every file
for file_path in matches:
    # display output
    print(info_i()+f" {visual_counter}/{total_file_count} - {file_path}        ",end='\r')

    language = detect_language(file_path, all_languages)

    language.analyze_file(file_path)

    visual_counter+=1



#region results
total_line_count = 0
line_count_uncommented = 0

lines_with_print_statements = 0
lines_with_indents = 0
todos     = 0

used_languages = [] # Languages with one or more lines.

for language in all_languages:
    if language.lines > 0:
        used_languages.append(language)
    
    total_line_count += language.lines
    line_count_uncommented += language.lines_uncommented
    lines_with_print_statements += language.lines_output
    lines_with_indents += language.lines_indented
    todos += language.todos

print()
print(green_check()+" Done!")
print(green_check()+f" Read {total_file_count} files.")
print(info_i()+f" Total lines: {total_line_count}")
print(info_i()+f"     Non-comment lines:  {line_count_uncommented:<12} {     pretty_percent_bars(100*line_count_uncommented/total_line_count, 12)} {       pretty_percent(line_count_uncommented,total_line_count)}% of all lines")
print(info_i()+f"     Lines with output:  {lines_with_print_statements:<12} {pretty_percent_bars(100*lines_with_print_statements/line_count_uncommented,12)} {pretty_percent(lines_with_print_statements,line_count_uncommented)}% of code")
print(info_i()+f"     Lines with indents: {lines_with_indents:<12} {pretty_percent_bars(100*lines_with_indents/line_count_uncommented,12)} {pretty_percent(lines_with_indents,line_count_uncommented)}% of code")
#print(info_i()+f"     For loops: {lines_with_for_statements}")
#print(info_i()+f"     Functions: {functions}")
#print(info_i()+f"     Classes:   {classes}")
print(info_i()+f"     Todos:     {todos}")
print(info_i())
print(info_i()+" Lines by language")
print(info_i()+f"     Language     : Lines")
for language in used_languages:
    perc = pretty_percent(language.lines,total_line_count)
    print(info_i()+f"     {language.displayname:<13}: {language.lines:<12} {pretty_percent_bars(perc, 12)} {perc}%")
     

#region graph
if DO_GRAPH:
    print(info_i()+" Generating graph for README.md")

    # Do fancy stuff to generate graph
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    df = []
    for lang in used_languages:
        df.append([lang.displayname, lang.category, int(lang.lines)])

    df = pd.DataFrame(df)
    df.columns = ["Name", "Category", "Lines"]
    outer = df.groupby("Category").sum()
    outer.drop('Name', axis=1, inplace=True)

    inner = df.groupby(["Category", "Name"]).sum()
    inner_labels = inner.index.get_level_values(1)

    # The below code was modified from an example found at https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html
    fig, ax = plt.subplots(figsize=(8, 8))
    size_outer = 1.2
    size_inner = 1

    # Outer pie
    ax.pie(outer.values.flatten(), radius=size_outer,
        labels=outer.index, labeldistance=1.1,
        wedgeprops=dict(width=size_outer, edgecolor="w"),
        textprops=dict(size=16))

    # Inner pie
    ax.pie(inner.values.flatten(), radius=size_inner, 
        labels = inner_labels, labeldistance=0.6,
        wedgeprops=dict(width=size_inner, edgecolor="w"),
        textprops=dict(size=12))
    
    print(info_i()+" Graph created. Saving...")

    ax.set(aspect="equal", title="Languages by lines")
    #plt.show()

    # Save the graph
    fig.savefig('languages.png')

    print(green_check()+" Graph saved as languages.png")

#endregion graph

print(green_check()+" Program complete.")
#endregion results

# -- END OF FILE --