#
# -*- coding: utf-8 -*-
# OPR
# 
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
Calculates Offensive Power Rating (OPR), AutoOPR, and Calculated Contribution to Winning Margin (CCWM).

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

OPR = Offensive Power Rating
CCWM = Calculated Contribution to Winning Margin
Thanks to The Blue Alliance
    https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/

and owsorber (on Github)
    https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/

for help with OPR calculation.
"""


#region imports
# Builtin imports
import time
import sys
import os

# Internal Imports
import json_parse
from common_resources import PATH_TO_FTCAPI, NUMBER_OF_DAYS_FOR_RECENT_OPR, EVENT_CODE, PATH_TO_JOBLIB_CACHE, DO_JOBLIB_MEMORY
from common_resources import DEBUG_LEVEL, FIELD_MODE
from common_resources import log_error, green_check, info_i, red_x, byte_to_gb, seconds_to_time


if (DEBUG_LEVEL > 1):
    print(green_check()+" [OPRv4.py] Internal and builtin imports complete")
    print(info_i()+"    Now importing external imports (pandas, numpy, joblib)")

# External imports
try:
    import pandas as pd
    import numpy
    import joblib

except ImportError as e:
    log_error("[OPRv4.py][imports] Error with importing Pandas, Numpy, or Joblib. Are you using the correct virtual environment? Full error message: "+str(e))
    print(red_x()+" [OPRv4][imports] ImportError with Pandas! Are you using the correct virtual environment?\n\n")
    raise e
#endregion imports

starttime = time.time()

#region joblib
# Set up joblib's cache memory location
try:
    if DO_JOBLIB_MEMORY:
        memory = joblib.Memory(PATH_TO_JOBLIB_CACHE, verbose=0)

        if DEBUG_LEVEL > 0:
            print(info_i()+f" [OPRv4py] Joblib memory set up (path {PATH_TO_JOBLIB_CACHE})")
    
    else:
        memory = None

        if DEBUG_LEVEL>0:
            print(info_i()+f" [OPRv4py] Joblib memory disabled (DO_JOBLIB_MEMORY=False)")
    

# If the location is malformed, dne, or etc log the error, print to terminal and raise the error.
except Exception as e:
    log_error( "[OPRv4.py][setup stuff] Joblib memory creation had an error. Some info:")
    log_error(f"                              PATH_TO_JOBLIB_CACHE={PATH_TO_JOBLIB_CACHE}")
    log_error( "                              The most likely cause for this is if you put your joblib cache somewhere other than the working directory.")
    log_error( "                              The error has been printed to the console and raised, reguardless of the debug_level.")
    
    print(red_x()+ " [OPRv4][setup] Joblib memory creation had an error. Some info:")
    print(red_x()+f"                 PATH_TO_JOBLIB_CACHE={PATH_TO_JOBLIB_CACHE}")
    print(red_x()+ "   The most likely cause for this is if you put your joblib cache somewhere other than the working directory.\n")
    raise e
#endregion joblib


if DEBUG_LEVEL>0:
    print(green_check()+" [OPRv4.py] All imports successful.")
    print(info_i()+f" [OPRv4.py] field_mode is {FIELD_MODE}. Global calcs will {'' if (FIELD_MODE) else 'NOT '}be run.")


if __name__ == "__main__" and DEBUG_LEVEL>0:
    print(info_i()+" [OPRv4.py] This program was called as __main__")


#region functions
#region utils
def convertToList(statMatrix) -> list:
    """ Converts any stat represented by a matrix into a list, used later for sorting."""
    return statMatrix.tolist()


def loadTeamNumbers() -> list:
    """
    Loads teams from a csv file team_list_filtered.csv (created in jsonparse.py)
    """
    return list(pd.read_csv(os.path.join(PATH_TO_FTCAPI,"generatedfiles","team_list_filtered.csv"))["teamNumber"])


def filterMatchesByTeams(matches, teams: list):
    """
    """
    return matches[
            matches["Red1" ].isin(teams) |
            matches["Red2" ].isin(teams) |
            matches["Blue1"].isin(teams) |
            matches["Blue2"].isin(teams)
        ]


def loadMatches(filter_by_teams: list = []):
    """
    Returns a pandas object of the all_matches.csv file containing all matches.
    \nRelies on generatedfiles/all_matches.csv
    \nParameters:
    \n\t filter_by_teams (list) - Filters the matches only including the team numbers in the list
    
    """
    #TODO: Update everything else that relies on this function's output to accomodate pandas
    all_matches = pd.read_csv(os.path.join(PATH_TO_FTCAPI,"generatedfiles","all_matches.csv")) # Get the csv data

    # Make the start time column use the datetime format
    all_matches["actualStartTime"] = pd.to_datetime(all_matches["actualStartTime"], format="mixed")
    # format="%Y-%m-%"+"dT%H:%M:%S.%"+"f")

    # If filter_by_teams isn't none, filter the matches
    # by only the teams specified
    if filter_by_teams != []:
        all_matches = filterMatchesByTeams(all_matches, filter_by_teams)
    
    #print("All matches:"")
    #print(all_matches)
    #print("\n\n")
    return all_matches


def filter_dataframe_by_time(df: pd.DataFrame, days_before_now=None, start_date=None, end_date=None, days_before_end_date=None) -> pd.DataFrame:
    """
    Filters dataframe by time. Profided dataframe must have datetime column labeled as actualStartTime.
    days_before_now should be an integer
    start_date and end_date should be a string in format of yyyy-mm-dd
    Returns a filtered pandas dataframe.
    """
    if days_before_now != None:
        df = df[df.actualStartTime > pd.Timestamp.today() - pd.Timedelta(str(days_before_now)+"D")]
    
    if days_before_end_date != None:
        df = df[df.actualStartTime > pd.Timestamp(end_date) - pd.Timedelta(str(days_before_end_date)+"D")]

    if start_date != None:
        df = df[df.actualStartTime > pd.Timestamp(start_date)]

    if end_date != None:
        df = df[df.actualStartTime < pd.Timestamp(end_date)]
    
    return df


def cache_heavy_functions(
        memory:joblib.Memory, 
        calculate_opr_f, 
        build_m_f, 
        build_scores_f, 
        create_and_sort_stats_f):
    """
    Turns all heavy functions into joblib memorized functions.
    NOTE that memorized functions will not read or write to files, so
    any func that deals in files shouldn't be cached.
    Returns cached func versions of calculate_opr, build_m, build_scores, create_and_sort_stats
    """
    if DEBUG_LEVEL>0:
        print(info_i()+" [OPRv4] DO_JOBLIB_MEMORY is True. Caching calculate_opr, build_m, and build_scores.")

    calculate_opr_r = memory.cache(calculate_opr_f)
    build_m_r       = memory.cache(build_m_f)
    build_scores_r  = memory.cache(build_scores_f)
    create_and_sort_stats_r = memory.cache(create_and_sort_stats_f)

    if DEBUG_LEVEL>0:
        print(green_check()+" [OPRv4] Memory successfully cached.")
    
    return calculate_opr_r, build_m_r, build_scores_r, create_and_sort_stats_r
#endregion utils

""" 
Build M, a matrix of alliances x teams, where each row indicates the teams in that alliance.
A value of 1 means the team was in that alliance and a value of 0 means the team was not.
First loop through each red alliance and then loop through each blue alliance.
The resulting matrix should have 2 * len(matches) rows.
"""
def build_m(load_m: bool, matches: pd.DataFrame, teams: list) -> numpy.matrix:
    """
    Reuturns a matrix of type numpy.matrix M, with each row representing a match
    and each column representing a team. Ones for teams that participate, zeroes
    for teams that don't.
    """
    if DEBUG_LEVEL>0:
        print(info_i()+" [OPRv4] Building Matrix M for teams in alliances.")
    
    if DEBUG_LEVEL>1:
        print(info_i()+" [OPRv4][build_m] Arguments to build_m:")
        print(info_i()+"     load_m:"+str(load_m))
        print(info_i()+"     matches:\n"+str(matches))
        print(info_i()+"     DEBUG_LEVEL:"+str(DEBUG_LEVEL))
        print(info_i()+"     teams:"+str(teams))

    if load_m:
        if (DEBUG_LEVEL>1):
            print(info_i()+" [OPRv4][build_m]  Loading matrix from file, not building it.")
            
        M = numpy.load(os.path.join(PATH_TO_FTCAPI,"generatedfiles","OPR-m.npy"))

        if DEBUG_LEVEL>1:
            print(green_check()+" [OPRv4][build_m]  Matrix M successfully loaded from file OPR-m.npy")

    else:
        #TODO: Possibly redo this section to make it one line?
        # Maybe create a dataframe full of zeroes and somehow one-line
        # add ones where applicable? Look into this.
        if DEBUG_LEVEL>1:
            print(info_i()+" [OPRv4][build_m] load_m is false; manually building the matrix M.")
        
        M = []

        total_l = matches.shape[0]
        counter = 0
        #for match in matches:
        for row in matches.itertuples(index=False):
            # Display progress
            if (DEBUG_LEVEL>0) and (counter%10==0):
                print(info_i() + f"    Match {counter}/{total_l}    {round(100*(counter/total_l), 2)}%   ", end="\r")
            counter += 1
            
            r = []
            for team in teams:
                # red
                if team in [row[7],row[8]]:
                    r.append(1)
                else:
                    r.append(0)
            M.append(r)
        
            b = []
            for team in teams:
                # blue
                if team in [row[9], row[10]]:
                    b.append(1)
                else:
                    b.append(0)
            M.append(b)

        row=None
        r  =None
        b  =None
        

        if DEBUG_LEVEL>0:
            print() # add a linebreak to offset the \r printed in progress
        
        # Only enable for heavy debug - will spit out lots of stuff on the terminal
        #if debug>1:
        #    print(info_i()+"M before matricizing:")
        #    print(M)

        # Matricize
        M = numpy.matrix(M, dtype=numpy.ubyte) # type uint8, Unsigned 8-bit integer (0-255)

        if DEBUG_LEVEL>1:
            print(info_i()+"M after matricizing:")
            print(M)
        

        # save the matrix to a file for later loading
        numpy.save(os.path.join(PATH_TO_FTCAPI,"generatedfiles","OPR-m"),M)

    if (DEBUG_LEVEL>2):
        print(info_i()+"  M:")
        print(M)
        print()
        if (DEBUG_LEVEL>3):
            print(info_i()+"  Saving M to generatedfiles/M_debug.csv for debug purposes... (this could take a little bit if it is big)")
            numpy.savetxt(os.path.join(PATH_TO_FTCAPI,"generatedfiles","M_debug.csv"), M, delimiter=",")
            print(green_check()+"  Saved.")

    return M


def build_scores(matches: pd.DataFrame) -> tuple:
    """
    Outputs a tuple of Scores, Autos, and Margins as type numpy.matrix for the given matches dataframe.

    Builds 
      - Scores, a matrix of alliances x 1, where each row indicates the score of that alliance.
      - Autos, a matrix of alliances x 1, where each row indicates the autonomous score of that alliance.
      - Margins, a matrix of alliances x 1, where each row indicates the margin of victory/loss 
    of that alliance (e.g. if an alliance wins 60-50, the value is +10).

    The alliance represented by each row corresponds to the alliance represented by each row
    in the matrix M.
    """
    Scores  = []
    Autos   = []
    Margins = []
    try:
        # for match in matches, append the scores
        for row in matches.itertuples(index=False):
            Scores.append( [row[3]]) # red alliance score
            Scores.append( [row[5]]) # blue score
            Autos.append(  [row[4]]) # red auto
            Autos.append(  [row[6]]) # blue auto
            Margins.append([row[3] - row[5]]) # red score - blue score
            Margins.append([row[5] - row[3]]) # blue score - red score
    
    except TypeError as e:
        log_error("[OPRv4][build_scores] TypeError occured most likely due to indices in the input dataframe (which should not be there)")
        print("\n"+red_x()+" TypeError! This is most likely because you forgot to cut out the index of the dataframe.")
        print("\nRow:")
        print(row)
        print("types:")
        for i in row:
            print(f"  - {i} - {type(i)}")
        raise e

    # Return the scores matrices
    return numpy.matrix(Scores, dtype=numpy.short), numpy.matrix(Autos, dtype=numpy.short), numpy.matrix(Margins, dtype=numpy.short) # type short, or signed int16


def loadMatchesByRecent(
        filter_by_teams=None,
        number_of_days_from_today=NUMBER_OF_DAYS_FOR_RECENT_OPR) -> pd.DataFrame:
    """
    Loads matches, then filters by teams and number of days before today.
    Returns a pandas array containing all matches within NUMBER_OF_DAYS_FOR_RECENT_OPR (defined in commonresources.py)
    """
    allmatches = loadMatches(filter_by_teams=filter_by_teams)
    return filter_dataframe_by_time(allmatches, days_before_now=number_of_days_from_today)


def calculate_opr(M: numpy.matrix, Scores: numpy.matrix, Autos: numpy.matrix, Margins: numpy.matrix):
    """ 
    Uses numpy's linalg.lstsq method to solve the oprs for OPR, AutoOPR, and CCWM.
    This method is MUCH faster and better than using a pseudoinverse.
    Returns a tuple of OPRs, AUTOs, CCWMs
    This is used in prepare-machinelearning.py to reduce cycle times.
    
    Inspired by this guide for OPR calculation: https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/
    """
    if (DEBUG_LEVEL>0):
        print(info_i()+"  [OPRv4.py][calculate_opr] Getting OPRs, Autos, and CCWMs")
    
        if (DEBUG_LEVEL>1):
            print(info_i()+"        Getting OPRs")
    
    OPRs = numpy.linalg.lstsq(M, Scores, rcond=None)[0]

    if (DEBUG_LEVEL>1):
        print(info_i()+"        Getting Autos")
    
    AUTOs = numpy.linalg.lstsq(M, Autos, rcond=None)[0]

    if (DEBUG_LEVEL>1):
        print(info_i()+"        Getting CCWMs")

    CCWMs = numpy.linalg.lstsq(M, Margins, rcond=None)[0]

    return OPRs, AUTOs, CCWMs # Items in the matrices are of type float64, which have around 15 digits of accuracy


def create_and_sort_stats(teamsList, OPRs, AUTOs, CCWMs) -> pd.DataFrame:
    """
    Takes the list of teams and the statistics dataframes and sorts all by OPR.
    Returns a sorted results pandas DataFame object.
    """
    if (DEBUG_LEVEL>0):
        print(info_i()+" [OPRv4][create_and_sort_stats] Sorting reuslts...")


    if (DEBUG_LEVEL>2):
        print(info_i()+" [OPRv4][create_and_sort_stats] Creating sorted_results_pd")
    
        print(info_i()+"    Sizes of lists:")
        print(info_i()+"    teamsList len: "+str(len(teamsList)))
        print(info_i()+"    OPRs len:  "+str(len(OPRs)))
        print(info_i()+"    AUTOs len: "+str(len(AUTOs)))
        print(info_i()+"    CCWMs len: "+str(len(CCWMs)))
        

    # Cretae the sorted pandas array of teams and their respective stats
    try:
        sorted_results_pd = pd.DataFrame({
            "Team"   :list(teamsList),
            "OPR"    :convertToList(OPRs),
            "AutoOPR":convertToList(AUTOs),
            "CCWM"   :convertToList(CCWMs)
        })

    except Exception as e:
        if DEBUG_LEVEL>1:
            print(red_x()+" [OPRv4][create_and_sort_stats] Exception occured. Printing info for debug:")
            print("teamsList:"+str(teamsList))
            print("OPR:"+str(convertToList(OPRs)))
            print("AUTOs:"+str(convertToList(AUTOs)))
            print("CCWMs:"+str(convertToList(CCWMs)))
        
        else:
            print(red_x()+" [OPRv4][create_and_sort_stats] Exception occured. Please set debug_level to 2 or above for full info.")
        
        log_error("[OPRv4.py][create_and_sort_stats] Some weird value happened with this function and an exception occured. No idea why, good luck! Full error info:"+str(e))
        log_error("[OPRv4.py][create_and_sort_stats] More info on the inputs. If these numbers arent the same, that is bad:")
        log_error("    length of teamsList: "+str(len(teamsList)))
        log_error("    length of OPR: "+str(len(convertToList(OPRs))))
        log_error("    length of AUTOs: "+str(len(convertToList(AUTOs))))
        log_error("    length of CCWMs: "+str(len(convertToList(CCWMs))))
        raise e

    if (DEBUG_LEVEL>2):
        print(info_i()+"  | Stripping column strings of sorted_results_pd")

    # Strip the columns. Really I'm not sure why I do this but I found it somewhere
    # and they told me to do it, and it supposedly stops a few things from breaking.
    sorted_results_pd.columns=sorted_results_pd.columns.str.strip()

    if (DEBUG_LEVEL>2):
        print(info_i()+"  | Sorting sorted_results_pd")

    # Actually sort the pandas results
    sorted_results_pd.sort_values(by="OPR", ascending=False, inplace=True)

    if DEBUG_LEVEL>2:
        print(info_i()+"  | Done sorting sorted_results_pd. Now removing brackets.")
    # Remove the extra brackets
    try:
        sorted_results_pd["OPR"    ] = sorted_results_pd["OPR"    ].str.get(0)
        sorted_results_pd["AutoOPR"] = sorted_results_pd["AutoOPR"].str.get(0)
        sorted_results_pd["CCWM"   ] = sorted_results_pd["CCWM"   ].str.get(0)

    # AttributeError raised whenever sorted_results_pd is an empty dataframe
    except AttributeError as e:
        # So just do nothing - It's completely fine for this to happen.
        sorted_results_pd["OPR"    ] = sorted_results_pd["OPR"    ]
        sorted_results_pd["AutoOPR"] = sorted_results_pd["AutoOPR"]
        sorted_results_pd["CCWM"   ] = sorted_results_pd["CCWM"   ]
    
    # Any other exceptions, raise the error and print debug info
    except Exception as e:
        log_error("[OPRv4][create_and_sort_stats] Some other error occured while processing sorted_results_pd. Full error message: "+str(e))
        log_error("                                        sorted_results_pd: "+str(sorted_results_pd))
        #log_error("                                        matches: "+str(matches))
        log_error("                                        teamsList: "+str(teamsList))

        if DEBUG_LEVEL>1:
            print("[OPRv4][create_and_sort_stats] Exception occured while processing sorted_results_pd. Displaying debug info:")
            print("sorted_results_pd:")
            print(sorted_results_pd)
            #print("matches:")
            #print(matches)
        
        else:
            print("[OPRv4][create_and_sort_stats] Exception occured while processing sorted_results_pd. Set debug_level to 2 or more for full debug info.")

        print("\n\n\n\nn\n\n\n\n\n\n")
        raise e
        
    if DEBUG_LEVEL>1:
        print(green_check()+"  | create_and_sort_stats is done. Now returning sorted_results_pd")

    return sorted_results_pd


def do_all_opr_stuff(matches: pd.DataFrame, output_file_path: str, teams:list=loadTeamNumbers(), load_m=False, fallback=None):
    """
    Calculates OPR based on input matches (from load_matches), and saves the sorted results to the output filepath (csv).
    If fallback is set to the string 'zeroes', and there are empty dataframes, it will fill them with zeroes. Otherwise, it
    returns an error.
    """
    # Build M
    if (DO_JOBLIB_MEMORY and DEBUG_LEVEL>0):
        print(info_i()+"    build_m.check_call_in_cache (will func use joblib cache?) = "+str(build_m.check_call_in_cache(load_m, matches, teams=loadTeamNumbers())))

    M = build_m(load_m, matches, teams=teams) # Type numpy.matrix with ones and zeroes

    if (DEBUG_LEVEL>0):
        print()
        print(info_i()+" [OPRv4][do_all_opr_stuff]   Building Scores")

    # Build scores
    Scores, Autos, Margins = build_scores(matches)

    if (DEBUG_LEVEL>2):
        print(green_check()+" [OPRv4][do_all_opr_stuff]  Scores, Autos, and Margins calculated. Displaying below:")
        print(info_i()+"Scores")
        print(Scores)
        print()
        print(info_i()+"Autos")
        print(Autos)
        print()
        print(info_i()+"Margins")
        print(Margins)
        print()

    if (DEBUG_LEVEL>1):
        print(info_i()+" [OPRv4][do_all_opr_stuff] Debug info:")
        print(info_i()+"    M type: "+str(type(M)))
        print(info_i()+"    M:")
        print(M)
        # Convert all matrices from type list to type matrix using numpy
        print(info_i()+"    Memory Update:")
        print(info_i()+f"        |  - M (int8) - {M.nbytes}b or {byte_to_gb(M.nbytes)}GB - Sizeof {sys.getsizeof(M)} - M.size (# of elements) {M.size}")
        print(info_i()+"        |  - Scores  - " + str(Scores.nbytes)  + "b  - " + str(sys.getsizeof(Scores)))
        print(info_i()+"        |  - Autos   - " + str(Autos.nbytes)   + "b  - " + str(sys.getsizeof(Autos)))
        print(info_i()+"        |  - Margins - " + str(Margins.nbytes) + "b  - " + str(sys.getsizeof(Margins)))
        print(info_i()+"    Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...")

    
    # This is the real intense operation...
    # Actually calculate the OPR
    if (DO_JOBLIB_MEMORY and DEBUG_LEVEL>0):
        print(info_i()+"    calculate_opr.check_call_in_cache (will func use joblib cache?) = "+str(calculate_opr.check_call_in_cache(M, Scores, Autos, Margins)))

    OPRs, AUTOs, CCWMs = calculate_opr(M, Scores, Autos, Margins)

    if DEBUG_LEVEL>0:
        print(green_check()+" Raw OPRs, AUTOs, and CCWMS calculated.")

    if (DEBUG_LEVEL>2):
        print(green_check()+"  Displaying raw ones below:")
        print(info_i()+"OPRs")
        print(OPRs)
        print()
        print(info_i()+"AUTOs")
        print(AUTOs)
        print()
        print(info_i()+"CCWMs")
        print(CCWMs)
        print()
    
    # Initialize the unsorted list of teams
    teamsList = list(teams)

    if fallback=="zeroes":
        used_fallback = False

        if OPRs.size == 0:
            used_fallback = True
            OPRs = numpy.zeros((len(teamsList), 1))
        
        if AUTOs.size == 0:
            used_fallback = True
            AUTOs = numpy.zeros((len(teamsList), 1))
        
        if CCWMs.size == 0:
            used_fallback = True
            CCWMs = numpy.zeros((len(teamsList), 1))
        
        if (DEBUG_LEVEL>2) and (used_fallback):
            print(green_check()+"  Fallback to zeroes used. Displaying new ones below:")
            print(info_i()+f"OPRs (shape {OPRs.shape})")
            print(OPRs)
            print()
            print(info_i()+f"AUTOs (shape {AUTOs.shape})")
            print(AUTOs)
            print()
            print(info_i()+f"CCWMs (shape {CCWMs.shape})")
            print(CCWMs)
            print()

    if DEBUG_LEVEL>1:
        print(info_i()+"    Rounding OPRs, AUTOs, and CCWMs to 14 places (prevents extremely near-zero values such as 10^-16)")

    OPRs  = OPRs.round(14)
    AUTOs = AUTOs.round(14)
    CCWMs = CCWMs.round(14)


    if (DO_JOBLIB_MEMORY and DEBUG_LEVEL>0):
        print(info_i()+" create_and_sort_stats.check_call_in_cache (will func use joblib cache?) = "+str(create_and_sort_stats.check_call_in_cache(teamsList, OPRs, AUTOs, CCWMs)))
    
    
    # Put everything into a pandas dataframe and sort by OPR
    sorted_results_pd = create_and_sort_stats(teamsList, OPRs, AUTOs, CCWMs)
    
    # Now write to the csv file
    if (DEBUG_LEVEL>0):
        print(info_i()+f" Writing to the pandas csv file {output_file_path}...")
    
    sorted_results_pd.to_csv(output_file_path, index=False)

    if (DEBUG_LEVEL>0):
        print(green_check()+f" Saved to the csv file.")

#endregion functions

def master_function(memory=memory):
    global calculate_opr, build_m, build_scores, create_and_sort_stats
    #region Joblib memory
    # Turn all heavy functions into joblib memorized functions
    # NOTE that memorized functions will not read or write to files, so
    # any func that deals in files shouldn't be cached.
    if (DO_JOBLIB_MEMORY):
        calculate_opr, build_m, build_scores, create_and_sort_stats = cache_heavy_functions(
            memory=memory,
            calculate_opr_f=calculate_opr,
            build_m_f=build_m,
            build_scores_f=build_scores,
            create_and_sort_stats_f=create_and_sort_stats
        ) # Doesn't work non-locally

    elif DEBUG_LEVEL>0:
        print(info_i()+" [OPRv4] NOT doing joblib memory caching - the respective variable in commonresources is False.")
    #endregion Joblib memory

    #region set settings

    # While in "field_mode" (during an event), global calcs take waaay to long.
    # We instead assume that the person was smart and ran a global calc session
    # very recently before the event, and use the previous global stats.
    if FIELD_MODE:
        do_opr_for_all_time = True
        do_opr_event_only   = True
        do_opr_recent       = True
        do_opr_global       = False

    else:
        # Not in field_mode, enable all calculations
        do_opr_for_all_time = True
        do_opr_event_only   = True
        do_opr_recent       = True
        do_opr_global       = True


    if ("recentonly" in sys.argv) or ("recent_only" in sys.argv) or ("recent-only" in sys.argv):
        do_opr_for_all_time = False
        do_opr_event_only   = False
        do_opr_recent       = True
        do_opr_global       = False
        do_team_stats       = False

    elif ("alltimeonly" in sys.argv) or ("alltime_only" in sys.argv) or ("alltime-only" in sys.argv):
        do_opr_for_all_time = True
        do_opr_event_only   = False
        do_opr_recent       = False
        do_opr_global       = False
        do_team_stats       = False


    if ("eventonly" in sys.argv) or ("event_only" in sys.argv) or ("event-only" in sys.argv):
        do_opr_for_all_time = False
        do_opr_event_only   = True
        do_opr_recent       = False
        do_opr_global       = False
        do_team_stats       = False


    if ("teamstatsonly" in sys.argv) or ("teamstats_only" in sys.argv) or ("teamstats-only" in sys.argv):
        do_opr_for_all_time = False
        do_opr_event_only   = False
        do_opr_recent       = False
        do_opr_global       = False
        do_team_stats       = True
    #endregion set settings

    if do_opr_global:

        if DEBUG_LEVEL>0:
            print(info_i()+" OPRv4.py")
            print(info_i()+"  --  --  --  --  --  --  --  --  --")
            print(info_i()+" Preparing for OPR calculation for global...")
            print(info_i())

        # Use all matches data (no specific_event)
        json_parse.prepare_opr_calculation()  # specific_event=event_code)


        # Load teams and matches from txt files
        if DEBUG_LEVEL>0:
            print(info_i()+" [OPRv4.py] Loading teams")

        teams   = loadTeamNumbers()  # Uses team_list_filtered.csv (created in jsonparse)
        matches = loadMatches()  # Uses all_matches.csv


        if DEBUG_LEVEL>0:
            print(info_i()+"    Number of teams:"+str(len(teams)))
            print(info_i()+"    Calculating global OPR for all matches.")

        do_all_opr_stuff(
            matches=matches,
            teams=teams, 
            output_file_path=os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_global_result_sorted.csv"),  
            load_m=False
        )



    if do_opr_for_all_time:
        if DEBUG_LEVEL>0:
            print(info_i()+" OPRv4.py")
            print(info_i()+"  --  --  --  --  --  --  --  --  --")
            print(info_i()+" Preparing for OPR calculation (all-time OPR for teams in given event only)...")
            print(info_i())

        # for the first one, use all matches data
        json_parse.prepare_opr_calculation(specific_event_teams=EVENT_CODE)#specific_event=event_code)



        # Load teams and matches from txt files
        if DEBUG_LEVEL>0:
            print(info_i()+" 1 Loading teams")

        teams   = loadTeamNumbers()
        #print("teams")
        #print(teams)
        
        matches = loadMatches(filter_by_teams=teams)


        if DEBUG_LEVEL>0:
            print(info_i()+"Number of teams:"+str(len(teams)))
            print(info_i()+"Calculating all-time OPR for all matches.")

        do_all_opr_stuff(
            matches=matches,
            teams=teams,
            output_file_path=os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_result_sorted.csv"),  
            load_m=False
        )



    #
    # Now calculate RECENT OPR
    #
    #
    #event_code=sys.argv[-1]

    if do_opr_recent:
        if DEBUG_LEVEL>0:
            print(info_i()+" OPRv4.py")
            print(info_i()+"  --  --  --  --  --  --  --  --  --")
            print(info_i()+" Preparing for OPR calculation recent only...")
            print(info_i())

        # for the first one, use all matches data
        json_parse.prepare_opr_calculation(specific_event_teams=EVENT_CODE)#specific_event=event_code)



        # Load teams and matches from txt files
        if DEBUG_LEVEL>0:
            print(info_i()+" 1 Loading teams")

        teams   = loadTeamNumbers()
        matches = loadMatchesByRecent(filter_by_teams=teams)



        if DEBUG_LEVEL>0:
            print(info_i()+" Number of teams:"+str(len(teams)))
            print(info_i()+" Calculating recent OPR for all matches.")

        do_all_opr_stuff(
            matches=matches,
            teams=teams,
            output_file_path=os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_recent_result_sorted.csv"), 
            load_m=False,
            fallback="zeroes"
        )


    #
    # Now calculate OPR within event
    #
    #
    if do_opr_event_only:

        if DEBUG_LEVEL>0:
            #print(green_check()+"Calculated OPR for all matches.")
            
            print(info_i()+"  --  --  --  --  --  --  --  --  --")
            print(info_i()+" Preparing for OPR calculation with specific event code "+str(EVENT_CODE))
            print(info_i()+" ")


        # Prepares the OPR calculation
        #Arguments:
        #  - specific_event (list) - returns only the data pertaining to the specified event code.
        #  - specific_teams (list) - filters all matches by the given teams
        #  - specific_event_teams (str) - returns data only for all teams in specified event code.
        json_parse.prepare_opr_calculation(specific_event=EVENT_CODE)

        teams   = loadTeamNumbers() # load teams from matches_per_team.csv
        matches = loadMatches(filter_by_teams=teams)

        if DEBUG_LEVEL>0:
            print(info_i()+"Calculating OPR for matches within event...")
            print(info_i()+" 1 Loading teams")
        
        #print(matches.shape)
        #print("matches by recent:")
        #print(matches)
        do_all_opr_stuff(
            matches = matches,
            teams=teams,
            output_file_path = os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_event_result_sorted.csv"),  
            load_m  = False
        )

        if DEBUG_LEVEL>0:
            print(green_check()+"Calculated OPR for event only.")



    if DEBUG_LEVEL>0:
        print(info_i()+f" [OPRv4.py] Total OPRv4 program took {seconds_to_time(time.time()-starttime)}")
        print(green_check()+" [OPRv4.py] Done!    Next probable step: to push the data to the sheets via sheets_api.py")


if __name__ == "__main__":
    master_function()

elif DEBUG_LEVEL>0:
    print(green_check()+"[OPR.py] Setup complete.")

# -- End of file --