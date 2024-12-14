#
# -*- coding: utf-8 -*-
# __init__.py
# Started 2024/08/20
# by Drew Wingfield
#
# This script is part of Drew Wingfield's EDrewcated Guesser.
# It is licensed under the license found at LICENSE.txt.
# See the documentation in the README.md file.
#
"""
Makes the required directories for the project.

This script is part of Drew Wingfield's EDrewcated Guesser.
It is licensed under the license found at LICENSE.txt.
See the documentation in the README.md file.

"""



import os

def make_required_directories():
    """
    Make directories required for the program to run if they don't already exist
    """
    # Make required directories if they don't exist already
    for dir in [
        "app/generatedfiles",
        #"app/generatedfiles/joblibcache",
        "app/generatedfiles/opr",
        "app/generatedfiles/opr/all-events",
        #"app/generatedfiles/opr/all-teams",
        "app/generatedfiles/eventdata"
    ]:
        if not os.path.exists(dir):
            os.makedirs(dir)



make_required_directories()

# -- End of file --