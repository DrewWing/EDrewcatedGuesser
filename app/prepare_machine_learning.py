#
# -*- coding: utf-8 -*-
# Prepare Machine Learning
# Started 2024-02-14
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
Prepares data for machine learning algorithm training.

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

# To profile it, use:
# scalene --profile-only OPRv4, jsonparse, prepare-machinelearning, commonresources  --json --outfile pythonprofile /home/wingfield/ftcapi-branch45-1/prepare-machinelearning.py

if __name__ == "__main__":
    print("   [prepare-machinelearning.py] This script was called as __main__")
    print("         Importing...")

from common_resources import PATH_TO_FTCAPI, DO_JOBLIB_MEMORY, NUMBER_OF_DAYS_FOR_RECENT_OPR, get_json, byte_to_gb, seconds_to_time
from common_resources import DEBUG_LEVEL, create_logger

import logging

logger = create_logger("prepare_machine_learning")

logger.info("Logger initialized.")

if DEBUG_LEVEL>0 and logger.isEnabledFor(logging.DEBUG):
    logger.warning(" !! DEBUG_LEVEL is greater than zero !!")
    logger.warning(" This will likely cause tens of thousands of extra print statements from OPRv4.py and jsonparse.py")
    logger.warning(" The reccomondation is to set it to zero in settings.config (this script will still output progress statements)")
    logger.warning(" If you really want to continue, type YES. Otherwise, the program will exit.")
    usrinput = input("  Continue? >")
    if usrinput.lower() in ["yes","y"]:
        pass

    else:
        exit()


from OPR import loadMatches, filterMatchesByTeams, filter_dataframe_by_time, build_m, build_scores, calculate_opr
import json_parse  # For OPR calculation preparation

import os
import sys
import time  # For process time estimations

import pandas as pd

if __name__ == "__main__":
    logger.info(" [prepare-machinelearning.py] Done importing.")

script_start_time = time.time()
last_cycle = time.time()
cycle_times = []

TRIM_CYCLE_TIMES = True

def dataframe_remove_zeroes(df: pd.DataFrame, column_names: list):
    """
    Removes the rows with zeroes in the given colums with column_names
    With help from ComputerFellow on StackOverflow
    https://stackoverflow.com/questions/34243194/filter-rows-of-pandas-dataframe-whose-values-are-lower-than-0
    """
    for col_name in column_names:
        df[col_name] = df[df[col_name] > 0][col_name]
    
    df = df.dropna()
    return df

#region OPR
# For each match, calculate the stats of the match teams for all matches before the given match
# and replace the match teams with their respective stats
json_parse.prepare_opr_calculation()  # Creates the all_matches.csv file
all_matches_to_train_on = loadMatches()  # Gets the matches from the all_matches.csv file

#logger.debug(all_matches_to_train_on)
#logger.debug("\niterrows version:")
#logger.debug(all_matches_to_train_on.iterrows())
#logger.debug("  exiting now")
#exit()

# Iterating over pandas DataFrame with help from waitingkuo on StackOverflow
# https://stackoverflow.com/questions/16476924/how-can-i-iterate-over-rows-in-a-pandas-dataframe
all_matches_to_train_on = all_matches_to_train_on.reset_index()  # make sure indexes pair with number of rows
total_shape = all_matches_to_train_on.shape

new_matches_to_train_on = {
    "actualStartTime":[], "description"  :[], "tournamentLevel":[],
    "scoreRedFinal"  :[], "scoreRedAuto" :[],
    "scoreBlueFinal" :[], "scoreBlueAuto":[],
    "redOPR" :[], "redAutoOPR" :[], "redCCWM" :[],
    "blueOPR":[], "blueAutoOPR":[], "blueCCWM":[],
    "recentredOPR" :[], "recentredAutoOPR" :[], "recentredCCWM" :[],
    "recentblueOPR":[], "recentblueAutoOPR":[], "recentblueCCWM":[],
    "whoWon":[]
}

time_left = 0

for index, match in all_matches_to_train_on.iterrows():

    #region times
    if index>0:
        cycle_times.append(time.time()-last_cycle)

        if len(cycle_times) > 500 and TRIM_CYCLE_TIMES:
            cycle_times = cycle_times[2:]
        

        time_left = round(sum(cycle_times)/len(cycle_times),3) * (total_shape[0] - index)
    
    last_cycle = time.time()
    #endregion times

    #region debug code
    #if index==50:
    #    debug=4
    #else:
    #    debug=0
    
    #if index==51:
    #    rename_this_variable_dataframe = pd.DataFrame(new_matches_to_train_on) #TODO: actually save this as csv, then go to ml-test.py and make sure that it works
    #    logger.debug("rename_this_variable_dataframe:")
    #    logger.debug(rename_this_variable_dataframe)
    #    
    #    exit()
    #endregion debug code

    logger.debug(f" Preparing match {index}/{total_shape[0]} ({ round(100*(index/total_shape[0]), 2) }%) - approx. {seconds_to_time(time_left, roundto=0)} left                      ", end=("\n" if DEBUG_LEVEL>1 else "\r"))

    date_of_match = match["actualStartTime"]

    if DEBUG_LEVEL>4 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" match:")
        logger.debug(match)

    only_the_teams_in_that_match = [
        match["Red1"],
        match["Red2"],
        match["Blue1"],
        match["Blue2"]
    ]

    if DEBUG_LEVEL>4 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" Date of match:")
        logger.debug(date_of_match)
        logger.debug(" only_the_teams_in_that_match:")
        logger.debug(only_the_teams_in_that_match)
    
    # Filter the matches by teams and date
    filtered_matches_teams = filterMatchesByTeams(all_matches_to_train_on, only_the_teams_in_that_match)
    
    if DEBUG_LEVEL>4 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" Matches filtered by teams:")
        logger.debug(filtered_matches)
    
    filtered_matches = filter_dataframe_by_time(filtered_matches_teams, end_date=date_of_match)
    filtered_matches_recent = filter_dataframe_by_time(filtered_matches, end_date=date_of_match, days_before_end_date=NUMBER_OF_DAYS_FOR_RECENT_OPR)

    if DEBUG_LEVEL>4 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" Matches filtered by time:")
        logger.debug(filtered_matches)

    #region actual OPR calc
    # Build M
    # NOTE that the teams variable in this function is VERY important and determines the order
    # that the OPRs, AutoOPRs, and CCWMS are in the resulting lists once calculated.
    M = build_m(False, filtered_matches, teams=only_the_teams_in_that_match) # NOTE that M is now type numpy.matrix

    if DEBUG_LEVEL>1 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" [prepare-machinelearning.py] 4 Building Scores")

    # Remove indexes from the filtered matches dataframe - prevents errors while building scores
    del filtered_matches["index"]

    # Build scores
    Scores, Autos, Margins = build_scores(filtered_matches)

    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        logging.debug("  Scores, Autos, and Margins calculated. Displaying below:")
        logging.debug("Scores")
        logging.debug(Scores)
        logging.debug()
        logging.debug("Autos")
        logging.debug(Autos)
        logging.debug()
        logging.debug("Margins")
        logging.debug(Margins)
        logging.debug()

    if DEBUG_LEVEL>2 and logger.isEnabledFor(logging.DEBUG):
        # Convert all matrices from type list to type matrix using numpy
        logging.debug( " Memory Update:")
        logging.debug(f"    |  - M (int8) - {M.nbytes}b or {byte_to_gb(M.nbytes)}GB - Sizeof {sys.getsizeof(M)} - M.size (# of elements) {M.size}")
        logging.debug( "    |  - Scores  - " + str(Scores.nbytes)  + "b  - " + str(sys.getsizeof(Scores)))
        logging.debug( "    |  - Autos   - " + str(Autos.nbytes)   + "b  - " + str(sys.getsizeof(Autos)))
        logging.debug( "    |  - Margins - " + str(Margins.nbytes) + "b  - " + str(sys.getsizeof(Margins)))

    
    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        logger.debug("  Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...")
    
    # This is the real RAM-intense operation...
    # Actually calculate the OPR
    if DO_JOBLIB_MEMORY and DEBUG_LEVEL>2:
        logger.debug(" calculate_opr.check_call_in_cache (will func use joblib cache?) = "+str(calculate_opr.check_call_in_cache(M, Scores, Autos, Margins)))

    OPRs, AUTOs, CCWMs = calculate_opr(M, Scores, Autos, Margins)


    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        logger.debug("  raw (unrounded) OPRs, AUTOs, and CCWMS calculated. Displaying below:")
        logger.debug("OPRs")
        logger.debug(OPRs)
        logger.debug()
        logger.debug("AUTOs")
        logger.debug(AUTOs)
        logger.debug()
        logger.debug("CCWMs")
        logger.debug(CCWMs)
        logger.debug()

    if DEBUG_LEVEL>2 and logger.isEnabledFor(logging.DEBUG):
        logger.debug("  Rounding OPRs, AUTOs, and CCWMs to 10 places (prevents extremely near-zero values such as 10^-16)")

    # Round each to 10 places
    OPRs  = list(i[0] for i in list(OPRs.round(10)))
    AUTOs = list(i[0] for i in list(AUTOs.round(10)))
    CCWMs = list(i[0] for i in list(CCWMs.round(10)))

    # Replace empty lists generated by the early matches when no previous matches have been played.
    # These will be filtered out later
    if OPRs == []:
        OPRs = [0, 0, 0, 0]
    
    if AUTOs == []:
        AUTOs = [0, 0, 0, 0]
    
    if CCWMs == []:
        CCWMs = [0, 0, 0, 0]
    
    
    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" OPRs type:")
        logger.debug(type(OPRs))
        logger.debug(" and its string form")
        logger.debug(OPRs)

    #endregion actual OPR calc
    
    
    #region actual RECENT OPR calc
    # Build M
    # NOTE that the teams variable in this function is VERY important and determines the order
    # that the OPRs, AutoOPRs, and CCWMS are in the resulting lists once calculated.
    M_recent = build_m(False, filtered_matches_recent, teams=only_the_teams_in_that_match) # NOTE that M is now type numpy.matrix

    if DEBUG_LEVEL>1 and logger.isEnabledFor(logging.DEBUG):
        logger.debug("    Building Scores")

    # Remove indexes from the filtered matches dataframe - prevents errors while building scores
    del filtered_matches_recent["index"]

    # Build scores
    RecentScores, RecentAutos, RecentMargins = build_scores(filtered_matches_recent)

    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        logger.debug("  Scores, Autos, and Margins calculated. Displaying below:")
        logger.debug("RecentScores")
        logger.debug(RecentScores)
        logger.debug()
        logger.debug("RecentAutos")
        logger.debug(RecentAutos)
        logger.debug()
        logger.debug("RecentMargins")
        logger.debug(RecentMargins)
        logger.debug()

    if DEBUG_LEVEL>2 and logger.isEnabledFor(logging.DEBUG):
        # Convert all matrices from type list to type matrix using numpy
        logger.debug(info_i()+" Memory Update:")
        logger.debug(f"    |  - M_recent (int8) - {M_recent.nbytes}b or {byte_to_gb(M_recent.nbytes)}GB - Sizeof {sys.getsizeof(M_recent)} - M.size (# of elements) {M_recent.size}")
        logger.debug("    |  - RecentScores  - " + str(RecentScores.nbytes)  + "b  - " + str(sys.getsizeof(RecentScores)))
        logger.debug("    |  - RecentAutos   - " + str(RecentAutos.nbytes)   + "b  - " + str(sys.getsizeof(RecentAutos)))
        logger.debug("    |  - RecentMargins - " + str(RecentMargins.nbytes) + "b  - " + str(sys.getsizeof(RecentMargins)))

    
    # collect garbage to save RAM
    #gc.collect() #removed to reduce cycle times
    
    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        #logger.debug(info_i()+"  Garbage collected")
        logger.debug("  Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...")
    
    # This is the real RAM-intense operation...
    # Actually calculate the OPR
    if DO_JOBLIB_MEMORY and DEBUG_LEVEL>2 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" calculate_opr.check_call_in_cache (will func use joblib cache?) = "+str(calculate_opr.check_call_in_cache(M_recent, RecentScores, RecentAutos, RecentMargins)))

    RecentOPRs, RecentAUTOs, RecentCCWMs = calculate_opr(M_recent, RecentScores, RecentAutos, RecentMargins)


    if (DEBUG_LEVEL>3):
        logger.debug("  raw (unrounded) RecentOPRs, RecentAUTOs, and RecentCCWMS calculated. Displaying below:")
        logger.debug("RecentOPRs")
        logger.debug(RecentOPRs)
        logger.debug()
        logger.debug("RecentAUTOs")
        logger.debug(RecentAUTOs)
        logger.debug()
        logger.debug("RecentCCWMs")
        logger.debug(RecentCCWMs)
        logger.debug()

    if DEBUG_LEVEL>2:
        logger.debug("  Rounding RecentOPRs, RecentAUTOs, and RecentCCWMs to 10 places (prevents extremely near-zero values such as 10^-16)")

    # Round each to 10 places
    RecentOPRs  = list(i[0] for i in list(RecentOPRs.round(10)))
    RecentAUTOs = list(i[0] for i in list(RecentAUTOs.round(10)))
    RecentCCWMs = list(i[0] for i in list(RecentCCWMs.round(10)))

    # Replace empty lists generated by the early matches when no previous matches have been played.
    # These will be filtered out later
    if RecentOPRs == []:
        RecentOPRs = [0, 0, 0, 0]
    
    if RecentAUTOs == []:
        RecentAUTOs = [0, 0, 0, 0]
    
    if RecentCCWMs == []:
        RecentCCWMs = [0, 0, 0, 0]
    
    
    if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" RecentOPRs type:")
        logger.debug(type(RecentOPRs))
        logger.debug(" and its string form")
        logger.debug(RecentOPRs)

    #endregion actual RECENT OPR calc
    
    if (match["scoreRedFinal"] > match["scoreBlueFinal"]):
        whowon = "Red"
    
    elif (match["scoreRedFinal"] < match["scoreBlueFinal"]):
        whowon = "Blue"
    
    else:
        whowon = "Tie"

    # The OPRs, AUTOs, and CCWMs are in the form of Red1, Red2, Blue1, Blue2
    # Get the OPR, AutoOPR, and CCWM of each particular team
    new_matches_to_train_on["actualStartTime"].append(match["actualStartTime"])
    new_matches_to_train_on["description"].append(match["description"])
    new_matches_to_train_on["tournamentLevel"].append(match["tournamentLevel"])
    new_matches_to_train_on["scoreRedFinal"  ].append(match["scoreRedFinal"])
    new_matches_to_train_on["scoreRedAuto"   ].append(match["scoreRedAuto"])
    new_matches_to_train_on["scoreBlueFinal" ].append(match["scoreBlueFinal"])
    new_matches_to_train_on["scoreBlueAuto"  ].append(match["scoreBlueAuto"])
    new_matches_to_train_on["redOPR"     ].append(OPRs[0] + OPRs[1])
    new_matches_to_train_on["redAutoOPR" ].append(AUTOs[0] + AUTOs[1])
    new_matches_to_train_on["redCCWM"    ].append(CCWMs[0] + CCWMs[1])
    new_matches_to_train_on["blueOPR"    ].append(OPRs[2] + OPRs[3])
    new_matches_to_train_on["blueAutoOPR"].append(AUTOs[2] + AUTOs[3])
    new_matches_to_train_on["blueCCWM"   ].append(CCWMs[2] + CCWMs[3])
    new_matches_to_train_on["recentredOPR"     ].append(RecentOPRs[0]  + RecentOPRs[1]) #  Recent stats
    new_matches_to_train_on["recentredAutoOPR" ].append(RecentAUTOs[0] + RecentAUTOs[1])
    new_matches_to_train_on["recentredCCWM"    ].append(RecentCCWMs[0] + RecentCCWMs[1])
    new_matches_to_train_on["recentblueOPR"    ].append(RecentOPRs[2]  + RecentOPRs[3])
    new_matches_to_train_on["recentblueAutoOPR"].append(RecentAUTOs[2] + RecentAUTOs[3])
    new_matches_to_train_on["recentblueCCWM"   ].append(RecentCCWMs[2] + RecentCCWMs[3])
    new_matches_to_train_on["whoWon"].append(whowon)

    if DEBUG_LEVEL>5 and logger.isEnabledFor(logging.DEBUG):
        logger.debug(" new matches to train on:")
        logger.debug(new_matches_to_train_on)

    #if CRAPPY_LAPTOP:
    #    gc.collect()

training_data_matches = pd.DataFrame(new_matches_to_train_on) 
# We have to make it a pandas DataFrame because
# saving it as a csv is faster than using numpy arrays.
#endregion OPR


#region Saving
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f" Training data matches is assembled with shape {training_data_matches.shape}")
    logger.debug(" Now removing matches with zero OPR (the first matches before OPR was calculatable)")

if DEBUG_LEVEL>3 and logger.isEnabledFor(logging.DEBUG):
    logger.debug("training_data_matches:")
    logger.debug(training_data_matches)


training_data_matches = dataframe_remove_zeroes(training_data_matches, ["redOPR","blueOPR"])

logger.debug(f" Training data matches end shape {training_data_matches.shape}")
logger.debug(f" Now saving machine file as {os.path.join(PATH_TO_FTCAPI,"machine_file.csv")}")

training_data_matches.to_csv(os.path.join(PATH_TO_FTCAPI,"machine_file.csv"), index=False)

logger.info(" Saved to machine_file.csv.")
#endregion Saving


logger.info(" Machine learning preparation done.")
logger.info(" The next step is probably going to be to run the actual machine learning! (ml-test.py).")
logger.info(" Total prepare-machinelearning.py program took "+str(seconds_to_time(time.time()-script_start_time)))


# -- end of file --