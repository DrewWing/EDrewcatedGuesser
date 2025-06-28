#
# -*- coding: utf-8 -*-
# __init__.py
# Started 2024/08/20
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
Makes the required directories for the project.

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



import os

def make_required_directories(SEASON_YEAR=2024):
    """
    Make directories required for the program to run if they don't already exist
    """
    # Make required directories if they don't exist already
    for dir in [
        f"app/generatedfiles/{SEASON_YEAR}",
        #f"app/generatedfiles/{SEASON_YEAR}/joblibcache",
        f"app/generatedfiles/{SEASON_YEAR}/opr",
        f"app/generatedfiles/{SEASON_YEAR}/opr/all-events",
        #f"app/generatedfiles/{SEASON_YEAR}opr/all-teams",
        f"app/generatedfiles/{SEASON_YEAR}/eventdata"
    ]:
        if not os.path.exists(dir):
            os.makedirs(dir)



make_required_directories()

# -- End of file --