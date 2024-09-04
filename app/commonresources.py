#
# -*- coding: utf-8 -*-
# Common Resources
# Started 02-18-2024
# by Drew Wingfield
#

# A set of common constants and functions for Drew Wingfield's FTCAPI program.
# See the documentation in the README.md file.
# See the license in the LICENSE.txt file.

__all__ = [
    'get_json', 'log_error', 'byte_to_gb', 'seconds_to_time', 
    'NUMBER_OF_DAYS_FOR_RECENT_OPR', 'DO_JOBLIB_MEMORY', 
    'PATH_TO_FTCAPI', 'PATH_TO_JOBLIB_MEMORY', 'SERVICE_ACCOUNT_FILE', 
    'SPREADSHEET_ID' 
]
__version__ = '48.0 ALPHA'
__author__ = 'Drew Wingfield'

import sys
import json
import datetime
import os
import pathlib

from python_settings import PythonSettings
global_settings = PythonSettings()

slash = ('\\' if '\\' in global_settings.path_to_ftcapi else '/') # support both forwardslash and backslash type paths

PATH_TO_FTCAPI = global_settings.path_to_ftcapi+slash # Should have trailing slash!

#region joblibpath
PATH_TO_JOBLIB_CACHE = PATH_TO_FTCAPI+f"generatedfiles{slash}joblibcache{slash}joblib"

# The following code was copied and modified from viniciusarrud on GitHub https://github.com/joblib/joblib/issues/1496#issuecomment-1788968714
# It is a fix for a bug in Windows where it throws errors if you try to access a path longer than ~250 chars.
PATH_TO_JOBLIB_CACHE = str(pathlib.Path(PATH_TO_JOBLIB_CACHE).parent.resolve())

if os.name == "nt":
    #PATH_TO_JOBLIB_CACHE = os.path.join(PATH_TO_JOBLIB_CACHE, "cache")
    if PATH_TO_JOBLIB_CACHE.startswith("\\\\"):
        PATH_TO_JOBLIB_CACHE = "\\\\?\\UNC\\" + PATH_TO_JOBLIB_CACHE[2:]
    else:
        PATH_TO_JOBLIB_CACHE = "\\\\?\\" + PATH_TO_JOBLIB_CACHE
else:
    PATH_TO_JOBLIB_CACHE = os.path.join(folder, "cache")
#endregion joblibpath


NUMBER_OF_DAYS_FOR_RECENT_OPR = 120 # 35 seemed to have weird problems (TODO: bug that needs fixing)
EVENTCODE = global_settings.event_code

# TODO: make this and its correspondant in jsonparse all caps
accepted_match_types = ['Qualifier', 'Championship','League Tournament', 'League Meet', 'Super Qualifier', 'FIRST Championship']

# If using the windows machine (more powerful)
if 'win' in sys.platform:
    CRAPPY_LAPTOP  = False  # if True, inserts many more garbage collections to preserve RAM
    # Whether or not to calculate OPR based on all matches globally

# Otherwise, assume we're using a less powerful linux machine
else:
    CRAPPY_LAPTOP  = True
    # Whether or not to calculate OPR based on all matches globally


# whether or not to memorize functions using joblib.memory
DO_JOBLIB_MEMORY = True  # Used to be True

# used in sheetsapi (the -4 removes the "/app" from the path to ftcapi)
SERVICE_ACCOUNT_FILE = PATH_TO_FTCAPI[:-4] + 'service-account-key-ftc-api-for-sheets-19d729dc80e8.json'  # TODO: Remove before publication
SPREADSHEET_ID = "1KIox_wRJ0QdoUhu2oH1j6Q2Cj-mTO0PEnwTQ97-7wqY" #TODO: change this every event.
# A spreadsheet id is found in the URL of the given sheet:
# https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit



def get_json(path: str):
    """
    Returns the raw json for a given path.
    """
    try:
        with open(path, 'r', encoding='utf-8-sig') as thefile:
            return json.load(thefile)  # output.json
    
    except Exception as e:
        log_error( f'[commonresources.py][get_json] Some Error occured with getting json of path {path}.'
                    + f' Usually caused by an empty or malformed file. Raising this to the console. Full error message: {e}'
        )
        raise e
    
    #except json.decoder.JSONDecodeError as e:
    #    print(red_x()+'  get_json JSONDecodeError on path '+str(path))
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
    return make_printable('['+Colors.LIGHT_GREEN+'✓'+Colors.END+']')

def red_x() -> str:
    return make_printable('['+Colors.RED+'X'+Colors.END+']')

def info_i() -> str:
    return make_printable('['+Colors.BLUE+'i'+Colors.END+']')
#endregion color stuffs


def byte_to_gb(bytes) -> float:
    """Returns the amount of Gb for a given amount of bytes"""
    return round((bytes / (10**9)), 4)


def log_error(message: str, level="ERROR") -> None:
    """
    Logs an error message (with timestamp) to the error log at PATH_TO_FTCAPI/errors.log
    """
    with open(PATH_TO_FTCAPI+f"generatedfiles{slash}errors.log", "a") as myfile:
        myfile.write(f'[{datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}][{level}!] '+str(message)+'\n')


def seconds_to_time(seconds, roundto=3) -> str:
    
    minutes = int(seconds//60)
    if seconds >= 60:
        seconds_remainder = (int(round(seconds - (minutes*60), roundto)) if roundto==0 else round(seconds - (minutes*60), roundto))
    else:
        seconds_remainder = (int(round(seconds, roundto)) if roundto==0 else round(seconds, roundto))

        return f'{seconds_remainder} seconds'


    if minutes >= 60:
        hours = int(minutes//60)
        minutes = int(minutes- (hours*60))
        return f'{hours} hours, {minutes} minutes, and {seconds_remainder} seconds'

    else:
        return f'{minutes} minutes, {seconds_remainder} seconds'
    


if __name__ == "__main__":
    print(info_i()+'[commonresources] This file was called as __main__, which usually does not happen.')
    print(info_i()+'    Displaying constants and their values:')
    a = {
        'NUMBER_OF_DAYS_FOR_RECENT_OPR' : NUMBER_OF_DAYS_FOR_RECENT_OPR,
        'EVENTCODE'       : EVENTCODE,
        'PATH_TO_FTCAPI'  : PATH_TO_FTCAPI,
        'CRAPPY_LAPTOP'   : CRAPPY_LAPTOP,
        'DO_JOBLIB_MEMORY': DO_JOBLIB_MEMORY,
        'PATH_TO_JOBLIB_CACHE'  : PATH_TO_JOBLIB_CACHE,
        'SERVICE_ACCOUNT_FILE'  : SERVICE_ACCOUNT_FILE,
        'SPREADSHEET_ID': SPREADSHEET_ID,
        'sys.path'    : sys.path,
        'sys.platform': sys.platform
    }
    for i in a.keys():
        print(info_i()+f'      - {i}={a[i]} ({type(a[i])})')



# -- End of file --