#
# -*- coding: utf-8 -*-
# init_settings.py
# Started 2024/06/16
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
A program that writes certain variables to a machine-readable file for other scripts in Drew Wingfield's FTCAPI program.

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

Argument parsing with help from Michael Dorner on StackOverflow:
https://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments
and the docs:
https://docs.python.org/3/library/argparse.html
"""


import argparse
import os

desc = "A program that writes certain variables to a machine-readable file for other scripts in Drew Wingfield's FTCAPI program."

parser = argparse.ArgumentParser("init_settings.py", description=desc)
parser.add_argument("-EventCode", help="An alphanumeric event code for the current event.", type=str, required=True)
parser.add_argument("-DebugLevel", help="The debug level used for all python scripts. Determines debug info printed to terminal. Default 0", type=int, required=False, default=0)
parser.add_argument("-showsettings", help="Displays the settings for this script.", type=bool, required=False)
parser.add_argument("-FieldMode", help="During an event, set to true (default True). Prevents global calculations from being performed (LOTS of CPU time).", type=str, required=False, default=True)


args = parser.parse_args()

# ftcapiv4.ps1 hands init_settings boolean values that may be wrongly capitalized.
# Fix that here

if args.FieldMode.lower() == "true":
    args.FieldMode = True

else:
    args.FieldMode = False


path_to_ftcapi = str(os.path.dirname(os.path.realpath(__file__)))

if args.showsettings or args.DebugLevel > 0:
    print("init_settings.py")
    print("    Settings:")
    print(f"      - EventCode={args.EventCode}")
    print(f"      - path_to_ftcapi={path_to_ftcapi}")
    print(f"      - showsettings={args.showsettings}")
    print(f"      - DebugLevel={args.DebugLevel}")
    print(f"      - FieldMode={args.FieldMode}")



lines = [
    "# THIS FILE IS OVERWRITTEN EACH TIME THE SCRIPT RUNS!",
    "# DO NOT EDIT THIS, IT WILL NOT MATTER!",
    "# To edit settings, call the ftcapiv4.sh or ftcapiv4.ps1 with different arguments,",
    "# or edit those respective files.",
    f"# This file is written by {os.path.join(path_to_ftcapi,'init_settings.py')}",
    f"event_code={args.EventCode}",
    f"path_to_ftcapi={path_to_ftcapi}",
    f"debug_level={args.DebugLevel}",
    f"field_mode={args.FieldMode}"
    ""
]

settings_path = os.path.join(path_to_ftcapi,"generatedfiles","settings.config")

with open(settings_path, "w+") as settings_file:
    settings_file.truncate()
    for line in lines:
        settings_file.write(line)
        settings_file.write("\n")



