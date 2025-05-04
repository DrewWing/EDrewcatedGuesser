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
import logging

# Internal Imports
import json_parse
from common_resources import PATH_TO_FTCAPI, NUMBER_OF_DAYS_FOR_RECENT_OPR, EVENT_CODE, PATH_TO_JOBLIB_CACHE, DO_JOBLIB_MEMORY
from common_resources import DEBUG_LEVEL, FIELD_MODE
from common_resources import byte_to_gb, seconds_to_time, create_logger

logger = create_logger("OPR")

logger.debug("Internal and builtin imports complete.")
logger.debug("Now importing external imports (pandas, numpy, joblib)")

# External imports
try:
    import pandas as pd
    import numpy
    import joblib

except ImportError as e:
    logger.error("Error with importing Pandas, Numpy, or Joblib. Are you using the correct virtual environment? Full error message: "+str(e))
    raise e
#endregion imports

starttime = time.time()

#region joblib
# Set up joblib's cache memory location
try:
    if DO_JOBLIB_MEMORY:
        memory = joblib.Memory(PATH_TO_JOBLIB_CACHE, verbose=0)

        logger.debug(f"Joblib memory set up (path {PATH_TO_JOBLIB_CACHE})")
    
    else:
        memory = None

        logger.debug(f"Joblib memory disabled (DO_JOBLIB_MEMORY=False)")
    

# If the location is malformed, dne, or etc log the error, print to terminal and raise the error.
except Exception as e:
    logger.error( "[setup] Joblib memory creation had an error. Some info:")
    logger.error(f"  PATH_TO_JOBLIB_CACHE={PATH_TO_JOBLIB_CACHE}")
    logger.error(f"  Error: {e}")
    logger.error( "  The most likely cause for this is if you put your joblib cache somewhere other than the working directory.")
    logger.error( "  The error has been printed to the console and raised, reguardless of the debug_level.")
    raise e
#endregion joblib


logger.info("All imports successful. Setup complete.")
logger.info(f"field_mode is {FIELD_MODE}. Global calcs will {'' if (FIELD_MODE) else 'NOT '}be run.")


if __name__ == "__main__":
    logger.warning("This program was called as __main__")


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
    
    #logger.info("All matches:"")
    #logger.info(all_matches)
    #logger.info("\n\n")
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
    logger.info("DO_JOBLIB_MEMORY is True. Caching calculate_opr, build_m, and build_scores.")

    calculate_opr_r = memory.cache(calculate_opr_f)
    build_m_r       = memory.cache(build_m_f)
    build_scores_r  = memory.cache(build_scores_f)
    create_and_sort_stats_r = memory.cache(create_and_sort_stats_f)

    logger.info("Memory successfully cached.")
    
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
    logger.info("Building Matrix M for teams in alliances.")
    
    logger.debug("[build_m] Arguments to build_m:")
    logger.debug("  load_m:"+str(load_m))
    logger.debug("  matches:\n"+str(matches))
    logger.debug("  DEBUG_LEVEL:"+str(DEBUG_LEVEL))
    logger.debug("  teams:"+str(teams))

    if load_m:
        logger.debug("[build_m]  Loading matrix from file, not building it.")
            
        M = numpy.load(os.path.join(PATH_TO_FTCAPI,"generatedfiles","OPR-m.npy"))

        logger.debug("[build_m]  Matrix M successfully loaded from file OPR-m.npy")

    else:
        #TODO: Possibly redo this section to make it one line?
        # Maybe create a dataframe full of zeroes and somehow one-line
        # add ones where applicable? Look into this.
        logger.debug("[build_m] load_m is false; manually building the matrix M.")
        
        M = []

        total_l = matches.shape[0]
        counter = 0
        #for match in matches:
        for row in matches.itertuples(index=False):
            # Display progress
            if (counter%50==0) and (logger.isEnabledFor(logging.INFO)):
                logger.info(f"    Match {counter}/{total_l}    {round(100*(counter/total_l), 2)}%   ")
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
        

        # Only enable for heavy debug - will spit out lots of stuff on the terminal
        #if debug>1:
        #    logger.debug(info_i()+"M before matricizing:")
        #    logger.debug(M)

        # Matricize
        M = numpy.matrix(M, dtype=numpy.ubyte) # type uint8, Unsigned 8-bit integer (0-255)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("M after matricizing:")
            logger.debug(M)
        

        # save the matrix to a file for later loading
        numpy.save(os.path.join(PATH_TO_FTCAPI,"generatedfiles","OPR-m"),M)

    if (logger.isEnabledFor(logging.DEBUG)):
        logger.debug("  M:")
        logger.debug(str(M)+"\n")
        #TODO re-enable this?
        # if (DEBUG_LEVEL>3):
        #     logger.debug(info_i()+"  Saving M to generatedfiles/M_debug.csv for debug purposes... (this could take a little bit if it is big)")
        #     numpy.savetxt(os.path.join(PATH_TO_FTCAPI,"generatedfiles","M_debug.csv"), M, delimiter=",")
        #     logger.debug(green_check()+"  Saved.")

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
        logger.error("TypeError occured in build_scores most likely due to indices in the input dataframe (which should not be there)")
        logger.error("This is most likely because you forgot to cut out the index of the dataframe.")
        logger.error("Row:")
        logger.error(row)
        logger.error("types:")
        for i in row:
            logger.error(f"  - {i} - {type(i)}")
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
    logger.info("[calculate_opr] Getting OPRs, Autos, and CCWMs")
    
    logger.debug(" Getting OPRs")
    
    OPRs = numpy.linalg.lstsq(M, Scores, rcond=None)[0]

    logger.debug(" Getting Autos")
    
    AUTOs = numpy.linalg.lstsq(M, Autos, rcond=None)[0]

    logger.debug(" Getting CCWMs")

    CCWMs = numpy.linalg.lstsq(M, Margins, rcond=None)[0]

    return OPRs, AUTOs, CCWMs # Items in the matrices are of type float64, which have around 15 digits of accuracy


def create_and_sort_stats(teamsList, OPRs, AUTOs, CCWMs) -> pd.DataFrame:
    """
    Takes the list of teams and the statistics dataframes and sorts all by OPR.
    Returns a sorted results pandas DataFame object.
    """
    logger.info("[create_and_sort_stats] Sorting reuslts...")


    if (logger.isEnabledFor(logging.DEBUG)):
        logger.info("[create_and_sort_stats] Creating sorted_results_pd")
    
        logger.info("  Sizes of lists:")
        logger.info("  teamsList len: "+str(len(teamsList)))
        logger.info("  OPRs len:  "+str(len(OPRs)))
        logger.info("  AUTOs len: "+str(len(AUTOs)))
        logger.info("  CCWMs len: "+str(len(CCWMs)))
        

    # Cretae the sorted pandas array of teams and their respective stats
    try:
        sorted_results_pd = pd.DataFrame({
            "Team"   :list(teamsList),
            "OPR"    :convertToList(OPRs),
            "AutoOPR":convertToList(AUTOs),
            "CCWM"   :convertToList(CCWMs)
        })

    except Exception as e:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("teamsList:"+str(teamsList))
            logger.debug("OPR:"+str(convertToList(OPRs)))
            logger.debug("AUTOs:"+str(convertToList(AUTOs)))
            logger.debug("CCWMs:"+str(convertToList(CCWMs)))
        
        logger.error("[create_and_sort_stats] Some weird value happened with this function and an exception occured. No idea why, good luck! Full error info:"+str(e))
        logger.error("[create_and_sort_stats] More info is logged to DEBUG. If these numbers arent the same, that is bad:")
        logger.error("    length of teamsList: "+str(len(teamsList)))
        logger.error("    length of OPR: "+str(len(convertToList(OPRs))))
        logger.error("    length of AUTOs: "+str(len(convertToList(AUTOs))))
        logger.error("    length of CCWMs: "+str(len(convertToList(CCWMs))))
        raise e

    logger.debug("  | Stripping column strings of sorted_results_pd")

    # Strip the columns. Really I'm not sure why I do this but I found it somewhere
    # and they told me to do it, and it supposedly stops a few things from breaking.
    sorted_results_pd.columns=sorted_results_pd.columns.str.strip()

    logger.debug("  | Sorting sorted_results_pd")

    # Actually sort the pandas results
    sorted_results_pd.sort_values(by="OPR", ascending=False, inplace=True)

    logger.debug("  | Done sorting sorted_results_pd. Now removing brackets.")
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
        logger.error("[create_and_sort_stats] Some other error occured while processing sorted_results_pd. Full error message: "+str(e))
        logger.error("  sorted_results_pd: "+str(sorted_results_pd))
        logger.error("  teamsList: "+str(teamsList))

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("[create_and_sort_stats] Exception occured while processing sorted_results_pd. Displaying debug info:")
            logger.debug("sorted_results_pd:")
            logger.debug(sorted_results_pd)
            #logger.debug("matches:")
            #logger.debug(matches)
        
        raise e
        
    logger.debug("  | create_and_sort_stats is done. Now returning sorted_results_pd")

    return sorted_results_pd


def do_all_opr_stuff(matches: pd.DataFrame, output_file_path: str, teams:list=loadTeamNumbers(), load_m=False, fallback=None):
    """
    Calculates OPR based on input matches (from load_matches), and saves the sorted results to the output filepath (csv).
    If fallback is set to the string 'zeroes', and there are empty dataframes, it will fill them with zeroes. Otherwise, it
    returns an error.
    """
    # Build M
    if (DO_JOBLIB_MEMORY):
        logger.info("    build_m.check_call_in_cache (will func use joblib cache?) = "+str(build_m.check_call_in_cache(load_m, matches, teams=loadTeamNumbers())))

    M = build_m(load_m, matches, teams=teams) # Type numpy.matrix with ones and zeroes

    logger.info("[do_all_opr_stuff]   Building Scores")

    # Build scores
    Scores, Autos, Margins = build_scores(matches)

    if (logger.isEnabledFor(logging.DEBUG)) and DEBUG_LEVEL>1:
        logger.debug("[do_all_opr_stuff]  Scores, Autos, and Margins calculated. Displaying below:")
        logger.debug("Scores")
        logger.debug(Scores)
        logger.debug("")
        logger.debug("Autos")
        logger.debug(Autos)
        logger.debug("")
        logger.debug("Margins")
        logger.debug(Margins)
        logger.debug("")

    if (logger.isEnabledFor(logging.DEBUG)):
        logger.debug("[do_all_opr_stuff] Debug info:")
        logger.debug("    M type: "+str(type(M)))
        logger.debug("    M:")
        logger.debug(M)
        # Convert all matrices from type list to type matrix using numpy
        logger.debug("    Memory Update:")
        logger.debug(f"        |  - M (int8) - {M.nbytes}b or {byte_to_gb(M.nbytes)}GB - Sizeof {sys.getsizeof(M)} - M.size (# of elements) {M.size}")
        logger.debug("        |  - Scores  - " + str(Scores.nbytes)  + "b  - " + str(sys.getsizeof(Scores)))
        logger.debug("        |  - Autos   - " + str(Autos.nbytes)   + "b  - " + str(sys.getsizeof(Autos)))
        logger.debug("        |  - Margins - " + str(Margins.nbytes) + "b  - " + str(sys.getsizeof(Margins)))
        logger.debug("    Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...")

    
    # This is the real intense operation...
    # Actually calculate the OPR
    if (DO_JOBLIB_MEMORY):
        logger.info("    calculate_opr.check_call_in_cache (will func use joblib cache?) = "+str(calculate_opr.check_call_in_cache(M, Scores, Autos, Margins)))

    OPRs, AUTOs, CCWMs = calculate_opr(M, Scores, Autos, Margins)

    logger.info(" Raw OPRs, AUTOs, and CCWMS calculated.")

    if (logger.isEnabledFor(logging.DEBUG)) and DEBUG_LEVEL>1:
        logger.debug("  Displaying raw ones below:")
        logger.debug("OPRs")
        logger.debug(OPRs)
        logger.debug("")
        logger.debug("AUTOs")
        logger.debug(AUTOs)
        logger.debug("")
        logger.debug("CCWMs")
        logger.debug(CCWMs)
        logger.debug("")
    
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
        
        if (logger.isEnabledFor(logging.DEBUG)) and (used_fallback):
            logger.debug("  Fallback to zeroes used. Displaying new ones below:")
            logger.debug(f"OPRs (shape {OPRs.shape})")
            logger.debug(OPRs)
            logger.debug("")
            logger.debug(f"AUTOs (shape {AUTOs.shape})")
            logger.debug(AUTOs)
            logger.debug("")
            logger.debug(f"CCWMs (shape {CCWMs.shape})")
            logger.debug(CCWMs)
            logger.debug("")

    logger.debug("    Rounding OPRs, AUTOs, and CCWMs to 14 places (prevents extremely near-zero values such as 10^-16)")

    OPRs  = OPRs.round(14)
    AUTOs = AUTOs.round(14)
    CCWMs = CCWMs.round(14)


    if (DO_JOBLIB_MEMORY):
        logger.info(" create_and_sort_stats.check_call_in_cache (will func use joblib cache?) = "+str(create_and_sort_stats.check_call_in_cache(teamsList, OPRs, AUTOs, CCWMs)))
    
    
    # Put everything into a pandas dataframe and sort by OPR
    sorted_results_pd = create_and_sort_stats(teamsList, OPRs, AUTOs, CCWMs)
    
    # Now write to the csv file
    logger.debug(f"[d0_all_opr_stuff] Writing to the pandas csv file {output_file_path}...")
    
    sorted_results_pd.to_csv(output_file_path, index=False)

    logger.info(f"[do_all_opr_stuff] Saved sorted statistics to {output_file_path.replace(PATH_TO_FTCAPI,'')}")

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

    else:
        logger.info("NOT doing joblib memory caching - the respective variable in commonresources is False.")
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
        logger.info("__________________________________________________")
        logger.info("Preparing for OPR calculation for global calculation...")

        # Use all matches data (no specific_event)
        json_parse.prepare_opr_calculation()  # specific_event=event_code)


        # Load teams and matches from txt files
        logger.info("Loading teams")

        teams   = loadTeamNumbers()  # Uses team_list_filtered.csv (created in jsonparse)
        matches = loadMatches()  # Uses all_matches.csv


        logger.info("Number of teams:"+str(len(teams)))
        logger.info("Calculating global OPR for all matches.")

        do_all_opr_stuff(
            matches=matches,
            teams=teams, 
            output_file_path=os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_global_result_sorted.csv"),  
            load_m=False
        )



    if do_opr_for_all_time:
        logger.info("__________________________________________________")
        logger.info("Preparing for OPR calculation (all-time OPR for teams in given event only)...")

        # for the first one, use all matches data
        json_parse.prepare_opr_calculation(specific_event_teams=EVENT_CODE)#specific_event=event_code)



        # Load teams and matches from txt files
        logger.info("Loading teams")

        teams   = loadTeamNumbers()
        #logger.debug("teams")
        #logger.debug(teams)
        
        matches = loadMatches(filter_by_teams=teams)


        logger.info("Number of teams:"+str(len(teams)))
        logger.info("Calculating all-time OPR for all matches.")

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
        logger.info("__________________________________________________")
        logger.info("Preparing for OPR calculation recent only...")

        # for the first one, use all matches data
        json_parse.prepare_opr_calculation(specific_event_teams=EVENT_CODE)#specific_event=event_code)



        # Load teams and matches from txt files
        logger.info("Loading teams")

        teams   = loadTeamNumbers()
        matches = loadMatchesByRecent(filter_by_teams=teams)



        logger.info("Number of teams:"+str(len(teams)))
        logger.info("Calculating recent OPR for all matches.")

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
        #logger.debug(green_check()+"Calculated OPR for all matches.")
        logger.info("__________________________________________________")
        logger.info("Preparing for OPR calculation with specific event code "+str(EVENT_CODE))


        # Prepares the OPR calculation
        #Arguments:
        #  - specific_event (list) - returns only the data pertaining to the specified event code.
        #  - specific_teams (list) - filters all matches by the given teams
        #  - specific_event_teams (str) - returns data only for all teams in specified event code.
        json_parse.prepare_opr_calculation(specific_event=EVENT_CODE)

        teams   = loadTeamNumbers() # load teams from matches_per_team.csv
        matches = loadMatches(filter_by_teams=teams)

        logger.info("Calculating OPR for matches within event...")
        logger.info("Loading teams")
        
        #logger.debug(matches.shape)
        #logger.debug("matches by recent:")
        #logger.debug(matches)
        do_all_opr_stuff(
            matches = matches,
            teams=teams,
            output_file_path = os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_event_result_sorted.csv"),  
            load_m  = False
        )

        logger.info("Calculated OPR for event only.")



    logger.info(f"Total OPRv4 program took {seconds_to_time(time.time()-starttime)}")
    logger.info("Done!    Next probable step: to push the data to the sheets via sheets_api.py")


if __name__ == "__main__":
    master_function()

else:
    logger.info("Setup complete. Script was not called as main.")

# -- End of file --