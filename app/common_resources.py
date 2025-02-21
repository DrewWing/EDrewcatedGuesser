#
# -*- coding: utf-8 -*-
# Common Resources
# Started 02-18-2024
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
A set of common constants and functions for Drew Wingfield's EDrewcated Guesser program.

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


__all__ = [
    "get_json", "log_error", "byte_to_gb", "seconds_to_time", 
    "NUMBER_OF_DAYS_FOR_RECENT_OPR", "DO_JOBLIB_MEMORY", 
    "PATH_TO_FTCAPI", "PATH_TO_JOBLIB_MEMORY", "SERVICE_ACCOUNT_FILE", 
    "SPREADSHEET_ID"
]
__version__ = "49.0 Beta"
__author__ = "Drew Wingfield"

import sys
import json
import datetime
import os
import pathlib

import logging

from dotenv import load_dotenv
load_dotenv() # Load the environment variables


# Environment Variables
PATH_TO_FTCAPI = os.getenv("PROJECT_PATH", None) # The absolute path to the "app" directory within this project.
DEBUG_LEVEL = int(os.getenv("DEBUG_LEVEL", 0))
EVENT_CODE = os.getenv("EVENT_CODE", "FTCCMP1FRAN")
FIELD_MODE = os.getenv("FIELD_MODE", None) #TODO: Determine if this is necessary
SEASON_YEAR = int(os.getenv("SEASON_YEAR",2023))
DO_COLOR    = os.getenv("DO_COLOR","true").lower() == "true"

# Google Sheets stuff
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_KEY_PATH", PATH_TO_FTCAPI[:-4] + "ServiceAccountKey.json") # Used in sheetsapi (the -4 removes the "/app" from the path to ftcapi)
SPREADSHEET_ID = os.getenv("GOOGLE_SPREADSHEET_ID", "<placeholder Google Sheets Spreadsheet ID>") # https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit


#region Joblib
DO_JOBLIB_MEMORY = os.getenv("DO_JOBLIB_MEMORY", "True").lower() == "true"  # Used to be True
PATH_TO_JOBLIB_CACHE = os.getenv("JOBLIB_PATH", os.path.join(PATH_TO_FTCAPI,"generatedfiles","joblibcache","joblib"))

# The following code was copied and modified from viniciusarrud on GitHub https://github.com/joblib/joblib/issues/1496#issuecomment-1788968714
# It is a fix for a bug in Windows where it throws errors if you try to access a path longer than ~250 chars.
PATH_TO_JOBLIB_CACHE = str(pathlib.Path(PATH_TO_JOBLIB_CACHE).parent.resolve())

if os.name == "nt":
    #PATH_TO_JOBLIB_CACHE = os.path.join(PATH_TO_JOBLIB_CACHE, "cache")
    if PATH_TO_JOBLIB_CACHE.startswith("\\\\"):
        PATH_TO_JOBLIB_CACHE = "\\\\?\\UNC\\" + PATH_TO_JOBLIB_CACHE[2:]
    else:
        PATH_TO_JOBLIB_CACHE = "\\\\?\\" + PATH_TO_JOBLIB_CACHE

#endregion Joblib


NUMBER_OF_DAYS_FOR_RECENT_OPR = 120 # 35 seemed to have weird problems (TODO: bug that needs fixing)

# TODO: make this and its correspondant in jsonparse all caps
accepted_match_types = ["Qualifier", "Championship", "League Tournament", "League Meet", "Super Qualifier", "FIRST Championship"]

# This is kind of dead code and needs to be replaced.
# If using the windows machine (more powerful)
if "win" in sys.platform:
    CRAPPY_LAPTOP  = False  # if True, inserts many more garbage collections to preserve RAM
    # Whether or not to calculate OPR based on all matches globally

# Otherwise, assume we're using a less powerful machine
else:
    CRAPPY_LAPTOP  = True
    # Whether or not to calculate OPR based on all matches globally


def get_json(path: str):
    """
    Returns the raw json for a given path.
    """
    try:
        with open(path, "r", encoding="utf-8-sig") as thefile:
            return json.load(thefile)  # output.json
    
    except Exception as e:
        log_error( f"[commonresources.py][get_json] Some Error occured with getting json of path {path}."
                    + f" Usually caused by an empty or malformed file. Raising this to the console. Full error message: {e}"
        )
        raise e
    
    #except json.decoder.JSONDecodeError as e:
    #    print(red_x()+"  get_json JSONDecodeError on path "+str(path))
    #    print()
    #    raise e

# The Colors class was taken from rene-d (2018)
# https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007
#region color stuffs
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED   = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE  = "\033[0;34m"
    PURPLE= "\033[0;35m"
    CYAN  = "\033[0;36m"
    LIGHT_GRAY  = "\033[0;37m"
    DARK_GRAY   = "\033[1;30m"
    LIGHT_RED   = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW      = "\033[1;33m"
    LIGHT_BLUE  = "\033[1;34m"
    LIGHT_PURPLE= "\033[1;35m"
    LIGHT_CYAN  = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD      = "\033[1m"
    FAINT     = "\033[2m"
    ITALIC    = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK     = "\033[5m"
    NEGATIVE  = "\033[7m"
    CROSSED   = "\033[9m"
    END = "\033[0m"


def make_printable(s: str) -> str:
    """ Makes strings printable, reducing UnicodeDecodeErrors"""
    return s.encode(sys.stdout.encoding, errors="replace").decode()


def green_check() -> str:
    return make_printable("["+Colors.LIGHT_GREEN+"✓"+Colors.END+"]")

def red_x() -> str:
    return make_printable("["+Colors.RED+"X"+Colors.END+"]")

def info_i() -> str:
    return make_printable("["+Colors.BLUE+"i"+Colors.END+"]")
#endregion color stuffs


def byte_to_gb(bytes) -> float:
    """Returns the amount of Gb for a given amount of bytes"""
    return round((bytes / (10**9)), 4)


def seconds_to_time(seconds, roundto=3) -> str:
    
    minutes = int(seconds//60)
    if seconds >= 60:
        seconds_remainder = (int(round(seconds - (minutes*60), roundto)) if roundto==0 else round(seconds - (minutes*60), roundto))
    else:
        seconds_remainder = (int(round(seconds, roundto)) if roundto==0 else round(seconds, roundto))

        return f"{seconds_remainder} seconds"


    if minutes >= 60:
        hours = int(minutes//60)
        minutes = int(minutes- (hours*60))
        return f"{hours} hours, {minutes} minutes, and {seconds_remainder} seconds"

    else:
        return f"{minutes} minutes, {seconds_remainder} seconds"



#region Logging
# With help from 
# https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
# and https://stackoverflow.com/a/57205433/25598210
# for logging

# Set some settings for optimization and speed
logging.logThreads = False


# create logger
logger = logging.getLogger("common_resources")
logger.setLevel(logging.DEBUG)

# create console handler
cons_h = logging.StreamHandler()
cons_h.setLevel(logging.INFO)

# Create Error handler
err_h = logging.FileHandler(filename=os.path.join(PATH_TO_FTCAPI,"generatedfiles","errors.log"))
err_h.setLevel(logging.WARNING)

# Create debug handler (overwrites to new file)
deb_h = logging.FileHandler(
    filename=os.path.join(PATH_TO_FTCAPI,"generatedfiles","debug.log"),
    mode="w")
deb_h.setLevel(logging.DEBUG)

# Create formatters
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
if DO_COLOR:
    console_formatter = logging.Formatter(
        Colors.DARK_GRAY
        + "%(asctime)s"
        + Colors.DARK_GRAY 
        + " - "
        + Colors.END
        + "%(name)s - %(levelname)s - %(message)s")
else:
    console_formatter = formatter

# Add formatters
cons_h.setFormatter(console_formatter)
err_h.setFormatter(formatter)
deb_h.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(cons_h)
logger.addHandler(err_h)
logger.addHandler(deb_h)

#endregion Logging




if __name__ == "__main__":
    logger.warning("common_resources.py was called as __main__, which should not happen!")
    logger.info("    Displaying constants and their values:")
    a = {
        "NUMBER_OF_DAYS_FOR_RECENT_OPR" : NUMBER_OF_DAYS_FOR_RECENT_OPR,
        "EVENTCODE"       : EVENT_CODE,
        "PATH_TO_FTCAPI"  : PATH_TO_FTCAPI,
        "CRAPPY_LAPTOP"   : CRAPPY_LAPTOP,
        "DO_JOBLIB_MEMORY": DO_JOBLIB_MEMORY,
        "PATH_TO_JOBLIB_CACHE"  : PATH_TO_JOBLIB_CACHE,
        "SERVICE_ACCOUNT_FILE"  : SERVICE_ACCOUNT_FILE,
        "SPREADSHEET_ID": SPREADSHEET_ID,
        "sys.path"    : sys.path,
        "sys.platform": sys.platform
    }
    for i in a.keys():
        logger.info(info_i()+f"      - {i:<30} {str(type(a[i])):<15} = {a[i]}")



# -- End of file --