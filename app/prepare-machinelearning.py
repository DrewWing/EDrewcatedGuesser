#
# -*- coding: utf-8 -*-

# Prepare-machinelearning.py
# Started 2024-02-14
# by Drew Wingfield

# To profile it, use:
# scalene --profile-only OPRv4, jsonparse, prepare-machinelearning, commonresources  --json --outfile pythonprofile /home/wingfield/ftcapi-branch45-1/prepare-machinelearning.py

if __name__ == "__main__":
    print('   [prepare-machinelearning.py] This script was called as __main__')
    print('         Importing...')

from common_resources import PATH_TO_FTCAPI, DO_JOBLIB_MEMORY, NUMBER_OF_DAYS_FOR_RECENT_OPR, get_json, red_x, green_check, info_i, byte_to_gb, seconds_to_time


from python_settings import PythonSettings
settings = PythonSettings()

if settings.debug_level>0:
    print(red_x()+" !! settings.debug_level is greater than zero !!")
    print(info_i()+" This will likely cause tens of thousands of extra print statements from OPRv4.py and jsonparse.py")
    print(info_i()+" The reccomondation is to set it to zero in settings.config (this script will still output progress statements)")
    print(info_i()+" If you really want to continue, type YES. Otherwise, the program will exit.")
    usrinput = input("  Continue? >")
    if usrinput.lower() in ['yes','y']:
        pass

    else:
        exit()


from OPR import loadMatches, filterMatchesByTeams, filter_dataframe_by_time, build_m, build_scores, calculate_opr
import jsonparse  # For OPR calculation preparation

import os
import sys
import time  # For process time estimations

import pandas as pd

if __name__ == "__main__":
    print(info_i()+' [prepare-machinelearning.py] Done importing.')

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
jsonparse.prepare_opr_calculation()  # Creates the all-matches.csv file
all_matches_to_train_on = loadMatches()  # Gets the matches from the all-matches.csv file

#print(all_matches_to_train_on)
#print('\niterrows version:')
#print(all_matches_to_train_on.iterrows())
#print('  exiting now')
#exit()

# Iterating over pandas DataFrame with help from waitingkuo on StackOverflow
# https://stackoverflow.com/questions/16476924/how-can-i-iterate-over-rows-in-a-pandas-dataframe
all_matches_to_train_on = all_matches_to_train_on.reset_index()  # make sure indexes pair with number of rows
total_shape = all_matches_to_train_on.shape

new_matches_to_train_on = {
    'actualStartTime':[], 'description'  :[], 'tournamentLevel':[],
    'scoreRedFinal'  :[], 'scoreRedAuto' :[],
    'scoreBlueFinal' :[], 'scoreBlueAuto':[],
    'redOPR' :[], 'redAutoOPR' :[], 'redCCWM' :[],
    'blueOPR':[], 'blueAutoOPR':[], 'blueCCWM':[],
    'recentredOPR' :[], 'recentredAutoOPR' :[], 'recentredCCWM' :[],
    'recentblueOPR':[], 'recentblueAutoOPR':[], 'recentblueCCWM':[],
    'whoWon':[]
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
    #    print('rename_this_variable_dataframe:')
    #    print(rename_this_variable_dataframe)
    #    
    #    exit()
    #endregion debug code

    print(info_i()+f' Preparing match {index}/{total_shape[0]} ({ round(100*(index/total_shape[0]), 2) }%) - approx. {seconds_to_time(time_left, roundto=0)} left                      ', end=('\n' if settings.debug_level>1 else '\r'))

    date_of_match = match['actualStartTime']

    if settings.debug_level>4:
        print(' match:')
        print(match)

    only_the_teams_in_that_match = [
        match['Red1'],
        match['Red2'],
        match['Blue1'],
        match['Blue2']
    ]

    if settings.debug_level>4:
        print(' Date of match:')
        print(date_of_match)
        print(' only_the_teams_in_that_match:')
        print(only_the_teams_in_that_match)
    
    # Filter the matches by teams and date
    filtered_matches_teams = filterMatchesByTeams(all_matches_to_train_on, only_the_teams_in_that_match)
    
    if settings.debug_level>4:
        print(' Matches filtered by teams:')
        print(filtered_matches)
    
    filtered_matches = filter_dataframe_by_time(filtered_matches_teams, end_date=date_of_match)
    filtered_matches_recent = filter_dataframe_by_time(filtered_matches, end_date=date_of_match, days_before_end_date=NUMBER_OF_DAYS_FOR_RECENT_OPR)

    if settings.debug_level>4:
        print(' Matches filtered by time:')
        print(filtered_matches)

    #region actual OPR calc
    # Build M
    # NOTE that the teams variable in this function is VERY important and determines the order
    # that the OPRs, AutoOPRs, and CCWMS are in the resulting lists once calculated.
    M = build_m(False, filtered_matches, teams=only_the_teams_in_that_match) # NOTE that M is now type numpy.matrix

    if (settings.debug_level >1):
        print()
        print(info_i()+" [prepare-machinelearning.py] 4 Building Scores")

    # Remove indexes from the filtered matches dataframe - prevents errors while building scores
    del filtered_matches['index']

    # Build scores
    Scores, Autos, Margins = build_scores(filtered_matches)

    if (settings.debug_level>3):
        print(green_check()+'  Scores, Autos, and Margins calculated. Displaying below:')
        print(info_i()+'Scores')
        print(Scores)
        print()
        print(info_i()+'Autos')
        print(Autos)
        print()
        print(info_i()+'Margins')
        print(Margins)
        print()

    if (settings.debug_level>2):
        # Convert all matrices from type list to type matrix using numpy
        print(info_i()+" Memory Update:")
        print(f'    |  - M (int8) - {M.nbytes}b or {byte_to_gb(M.nbytes)}GB - Sizeof {sys.getsizeof(M)} - M.size (# of elements) {M.size}')
        print('    |  - Scores  - ' + str(Scores.nbytes)  + 'b  - ' + str(sys.getsizeof(Scores)))
        print('    |  - Autos   - ' + str(Autos.nbytes)   + 'b  - ' + str(sys.getsizeof(Autos)))
        print('    |  - Margins - ' + str(Margins.nbytes) + 'b  - ' + str(sys.getsizeof(Margins)))

    
    if (settings.debug_level>3):
        print(info_i()+'  Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...')
    
    # This is the real RAM-intense operation...
    # Actually calculate the OPR
    if (DO_JOBLIB_MEMORY and settings.debug_level>2):
        print(info_i()+' calculate_opr.check_call_in_cache (will func use joblib cache?) = '+str(calculate_opr.check_call_in_cache(M, Scores, Autos, Margins)))

    OPRs, AUTOs, CCWMs = calculate_opr(M, Scores, Autos, Margins)


    if (settings.debug_level>3):
        print(green_check()+'  raw (unrounded) OPRs, AUTOs, and CCWMS calculated. Displaying below:')
        print(info_i()+'OPRs')
        print(OPRs)
        print()
        print(info_i()+'AUTOs')
        print(AUTOs)
        print()
        print(info_i()+'CCWMs')
        print(CCWMs)
        print()

    if settings.debug_level>2:
        print(info_i()+'  Rounding OPRs, AUTOs, and CCWMs to 10 places (prevents extremely near-zero values such as 10^-16)')

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
    
    
    if settings.debug_level>3:
        print(' OPRs type:')
        print(type(OPRs))
        print(' and its string form')
        print(OPRs)

    #endregion actual OPR calc
    
    
    #region actual RECENT OPR calc
    # Build M
    # NOTE that the teams variable in this function is VERY important and determines the order
    # that the OPRs, AutoOPRs, and CCWMS are in the resulting lists once calculated.
    M_recent = build_m(False, filtered_matches_recent, teams=only_the_teams_in_that_match) # NOTE that M is now type numpy.matrix

    if (settings.debug_level >1):
        print()
        print(info_i()+"    Building Scores")

    # Remove indexes from the filtered matches dataframe - prevents errors while building scores
    del filtered_matches_recent['index']

    # Build scores
    RecentScores, RecentAutos, RecentMargins = build_scores(filtered_matches_recent)

    if (settings.debug_level>3):
        print(green_check()+'  Scores, Autos, and Margins calculated. Displaying below:')
        print(info_i()+'RecentScores')
        print(RecentScores)
        print()
        print(info_i()+'RecentAutos')
        print(RecentAutos)
        print()
        print(info_i()+'RecentMargins')
        print(RecentMargins)
        print()

    if (settings.debug_level>2):
        # Convert all matrices from type list to type matrix using numpy
        print(info_i()+" Memory Update:")
        print(f'    |  - M_recent (int8) - {M_recent.nbytes}b or {byte_to_gb(M_recent.nbytes)}GB - Sizeof {sys.getsizeof(M_recent)} - M.size (# of elements) {M_recent.size}')
        print('    |  - RecentScores  - ' + str(RecentScores.nbytes)  + 'b  - ' + str(sys.getsizeof(RecentScores)))
        print('    |  - RecentAutos   - ' + str(RecentAutos.nbytes)   + 'b  - ' + str(sys.getsizeof(RecentAutos)))
        print('    |  - RecentMargins - ' + str(RecentMargins.nbytes) + 'b  - ' + str(sys.getsizeof(RecentMargins)))

    
    # collect garbage to save RAM
    #gc.collect() #removed to reduce cycle times
    
    if (settings.debug_level>3):
        #print(info_i()+'  Garbage collected')
        print(info_i()+'  Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...')
    
    # This is the real RAM-intense operation...
    # Actually calculate the OPR
    if (DO_JOBLIB_MEMORY and settings.debug_level>2):
        print(info_i()+' calculate_opr.check_call_in_cache (will func use joblib cache?) = '+str(calculate_opr.check_call_in_cache(M_recent, RecentScores, RecentAutos, RecentMargins)))

    RecentOPRs, RecentAUTOs, RecentCCWMs = calculate_opr(M_recent, RecentScores, RecentAutos, RecentMargins)


    if (settings.debug_level>3):
        print(green_check()+'  raw (unrounded) RecentOPRs, RecentAUTOs, and RecentCCWMS calculated. Displaying below:')
        print(info_i()+'RecentOPRs')
        print(RecentOPRs)
        print()
        print(info_i()+'RecentAUTOs')
        print(RecentAUTOs)
        print()
        print(info_i()+'RecentCCWMs')
        print(RecentCCWMs)
        print()

    if settings.debug_level>2:
        print(info_i()+'  Rounding RecentOPRs, RecentAUTOs, and RecentCCWMs to 10 places (prevents extremely near-zero values such as 10^-16)')

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
    
    
    if settings.debug_level>3:
        print(' RecentOPRs type:')
        print(type(RecentOPRs))
        print(' and its string form')
        print(RecentOPRs)

    #endregion actual RECENT OPR calc
    
    if (match['scoreRedFinal'] > match['scoreBlueFinal']):
        whowon = 'Red'
    
    elif (match['scoreRedFinal'] < match['scoreBlueFinal']):
        whowon = 'Blue'
    
    else:
        whowon = 'Tie'

    # The OPRs, AUTOs, and CCWMs are in the form of Red1, Red2, Blue1, Blue2
    # Get the OPR, AutoOPR, and CCWM of each particular team
    new_matches_to_train_on['actualStartTime'].append(match['actualStartTime'])
    new_matches_to_train_on['description'].append(match['description'])
    new_matches_to_train_on['tournamentLevel'].append(match['tournamentLevel'])
    new_matches_to_train_on['scoreRedFinal'  ].append(match['scoreRedFinal'])
    new_matches_to_train_on['scoreRedAuto'   ].append(match['scoreRedAuto'])
    new_matches_to_train_on['scoreBlueFinal' ].append(match['scoreBlueFinal'])
    new_matches_to_train_on['scoreBlueAuto'  ].append(match['scoreBlueAuto'])
    new_matches_to_train_on['redOPR'     ].append(OPRs[0] + OPRs[1])
    new_matches_to_train_on['redAutoOPR' ].append(AUTOs[0] + AUTOs[1])
    new_matches_to_train_on['redCCWM'    ].append(CCWMs[0] + CCWMs[1])
    new_matches_to_train_on['blueOPR'    ].append(OPRs[2] + OPRs[3])
    new_matches_to_train_on['blueAutoOPR'].append(AUTOs[2] + AUTOs[3])
    new_matches_to_train_on['blueCCWM'   ].append(CCWMs[2] + CCWMs[3])
    new_matches_to_train_on['recentredOPR'     ].append(RecentOPRs[0]  + RecentOPRs[1]) #  Recent stats
    new_matches_to_train_on['recentredAutoOPR' ].append(RecentAUTOs[0] + RecentAUTOs[1])
    new_matches_to_train_on['recentredCCWM'    ].append(RecentCCWMs[0] + RecentCCWMs[1])
    new_matches_to_train_on['recentblueOPR'    ].append(RecentOPRs[2]  + RecentOPRs[3])
    new_matches_to_train_on['recentblueAutoOPR'].append(RecentAUTOs[2] + RecentAUTOs[3])
    new_matches_to_train_on['recentblueCCWM'   ].append(RecentCCWMs[2] + RecentCCWMs[3])
    new_matches_to_train_on['whoWon'].append(whowon)

    if settings.debug_level>5:
        print(' new matches to train on:')
        print(new_matches_to_train_on)

    #if CRAPPY_LAPTOP:
    #    gc.collect()

training_data_matches = pd.DataFrame(new_matches_to_train_on) 
# We have to make it a pandas DataFrame because
# saving it as a csv is faster than using numpy arrays.
#endregion OPR


#region Saving
if settings.debug_level>0:
    print(info_i()+f' Training data matches is assembled with shape {training_data_matches.shape}')
    print(info_i()+' Now removing matches with zero OPR (the first matches before OPR was calculatable)')

if settings.debug_level>3:
    print('training_data_matches:')
    print(training_data_matches)


training_data_matches = dataframe_remove_zeroes(training_data_matches, ['redOPR','blueOPR'])

if settings.debug_level>0:
    print(info_i()+f' Training data matches end shape {training_data_matches.shape}')
    print(info_i()+f' Now saving machine file as {os.path.join(PATH_TO_FTCAPI,"machinefile.csv")}')

training_data_matches.to_csv(os.path.join(PATH_TO_FTCAPI,'machinefile.csv'), index=False)

print(green_check()+' Saved to machinefile.csv.')
#endregion Saving


print(green_check()+' Machine learning preparation done.')
print(green_check()+' The next step is probably going to be to run the actual machine learning! (ml-test.py).')
print(green_check()+' Total prepare-machinelearning.py program took '+str(seconds_to_time(time.time()-script_start_time)))


# -- end of file --