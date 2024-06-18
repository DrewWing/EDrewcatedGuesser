#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FTC Team Statistics Calculator
owsorber (on Github) was the original inspiration,
and their script was heavily modified by Drew Wingfield
This is version 4
Forked from OPRv3-event.py on 2024-02-26

OPR = Offensive Power Rating
CCWM = Calculated Contribution to Winning Margin
"""

# with help from many sources, including:
# https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/

# External imports
try:
    import pandas as pd
    import numpy

except ImportError as e:
    print("\n\n\nImportError with Pandas! Are you using the correct venv with pandas installed?\n\n")
    raise e

# Builtin imports
import time, sys, gc

# Internal Imports
import jsonparse
from commonresources import PATH_TO_FTCAPI, CRAPPY_LAPTOP, NUMBER_OF_DAYS_FOR_RECENT_OPR, EVENTCODE, green_check, info_i, red_x, byte_to_gb, Colors

starttime = time.time()


# Converts any stat represented by a matrix into a list, used later for sorting
def convertToList(statMatrix):
    return statMatrix.tolist()



def loadMatches(filter_by_teams=None):
    """
    Returns a pandas object of the csv file containing all matches.
    filter_by_teams (list) - filters the matches only including the team numbers in the list
    """
    #TODO: update everything else that relies on this function's output to accomodate pandas
    all_matches = pd.read_csv(PATH_TO_FTCAPI+'all-matches.csv')
    all_matches['actualStartTime'] = pd.to_datetime(all_matches['actualStartTime'], format='mixed')#format="%Y-%m-%"+"dT%H:%M:%S.%"+"f")

    # if filter_by_teams isn't none, filter the matches
    # by only the teams specified
    if filter_by_teams != None:
        all_matches = all_matches[
            all_matches['Red1'].isin(filter_by_teams) |
            all_matches['Red2'].isin(filter_by_teams) |
            all_matches['Blue1'].isin(filter_by_teams) |
            all_matches['Blue2'].isin(filter_by_teams)
        ]
    
    #print('All matches:')
    #print(all_matches)
    #print('\n\n')
    return all_matches



""" 
Build M, a matrix of alliances x teams, where each row indicates the teams in that alliance.
A value of 1 means the team was in that alliance and a value of 0 means the team was not.
First loop through each red alliance and then loop through each blue alliance.
The resulting matrix should have 2 * len(matches) rows.
"""
def build_m(load_m, matches, debug=0):
    """
    Reuturns a matrix M
    """
    if (debug>0):
        print(info_i()+" 3 Building Matrix M for teams in alliances.")

    if load_m:
        M = numpy.load(PATH_TO_FTCAPI+'OPR-m.npy')

        if (debug>1):
            print(info_i()+"  Loading matrix from file, not building it.")

    else:
        M = []
        #print(matches.shape[1])
        total_l = matches.shape[0]
        counter = 0
        #for match in matches:
        #for match_index in range(matches.shape[0]):
        for row in matches.itertuples(index=False):
            if (debug>0) and (counter%10==0):
                print(info_i() + '    Match {}/{}'.format(counter,total_l), end='\r')
            counter += 1
            # for debug
            #print('row:'+str(row))
            #print('row as list:'+str(list(row)))
            #exit()
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
        del row, r, b # save memory

        # matricize
        M = numpy.matrix(M, dtype=numpy.byte)
        

        # save the matrix to a file for later loading
        numpy.save(PATH_TO_FTCAPI+'OPR-m',M)

    if (debug>2):
        print(info_i()+'  M:')
        print(M)
        print()
        if (debug>3):
            print(info_i()+'  Saving M for debug purposes...')
            numpy.savetxt(PATH_TO_FTCAPI+"M-debug.csv", M, delimiter=",")
            print(green_check()+'  Saved.')


    return M


def build_scores(matches):
    """
    Build Scores, a matrix of alliances x 1, where each row indicates the score of that alliance.
    Build Autos, a matrix of alliances x 1, where each row indicates the autonomous score of that alliance.
    Build Margins, a matrix of alliances x 1, where each row indicates the margin of victory/loss 
    of that alliance (e.g. if an alliance wins 60-50, the value is +10).
    The alliance represented by each row corresponds to the alliance represented by each row
    in the matrix M.
    """
    Scores  = []
    Autos   = []
    Margins = []
    #for match in matches:
    for row in matches.itertuples(index=False):
        Scores.append( [row[3]]) # red alliance score
        Scores.append( [row[5]]) # blue score
        Autos.append(  [row[4]]) # red auto
        Autos.append(  [row[6]]) # blue auto
        Margins.append([row[3] - row[5]]) # red score - blue score
        Margins.append([row[5] - row[3]]) # blue score - red score


    Scores_recent_ten = Scores.copy()
    Scores_recent_ten = Scores_recent_ten[::-1]
    Scores_recent_ten = Scores_recent_ten[:10]
    Scores_recent_ten = Scores_recent_ten[::-1]

    # Return the matrix
    return numpy.matrix(Scores, dtype=numpy.float32), numpy.matrix(Autos, dtype=numpy.float32), numpy.matrix(Margins, dtype=numpy.float32)


def loadMatchesByRecent(filter_by_teams=None):
    """
    Returns a pandas array containing all matches within NUMBER_OF_DAYS_FOR_RECENT_OPR (defined in commonresources.py)
    """
    allmatches = loadMatches(filter_by_teams=filter_by_teams)
    return allmatches[allmatches.actualStartTime > pd.Timestamp.today() - pd.Timedelta(str(NUMBER_OF_DAYS_FOR_RECENT_OPR)+'D')]


def calculate_opr(M, Scores, Autos, Margins, debug=0):
    """ 
    Uses numpy's linalg.lstsq method to solve the oprs for OPR, AutoOPR, and CCWM.
    This method is MUCH faster and better than using a pseudoinverse.
    """
    # Inspired by this guide for OPR calculation: https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/
    if (debug>0):
        print(info_i()+"  Getting OPRs, Autos, and CCWMs")
    
        if (debug>1):
            print(info_i()+" 5.5 Getting OPRs")
    
    OPRs = numpy.linalg.lstsq(M, Scores, rcond=None)[0]

    if (debug>1):
        print(info_i()+" 5.6 Getting Autos")

    if CRAPPY_LAPTOP:
        gc.collect()
    
    AUTOs = numpy.linalg.lstsq(M, Autos, rcond=None)[0]

    if (debug>1):
        print(info_i()+" 5.7 Getting CCWMs")
    
    if CRAPPY_LAPTOP:
        gc.collect()

    CCWMs = numpy.linalg.lstsq(M, Margins, rcond=None)[0]

    if CRAPPY_LAPTOP:
        gc.collect()

    return OPRs, AUTOs, CCWMs



def create_and_sort_stats(teamsList, OPRs, AUTOs, CCWMs, debug=0):
    """
    """
    if (debug>0):
        print(info_i()+" 8 Sorting reuslts...")


    if (debug>2):
        print(info_i()+'  Creating sorted_results_pd')
    
        print(info_i()+'  Sizes of lists:')
        print(info_i()+'  teamsList len: '+str(len(teamsList)))
        print(info_i()+'  OPRs len:  '+str(len(OPRs)))
        print(info_i()+'  AUTOs len: '+str(len(AUTOs)))
        print(info_i()+'  CCWMs len: '+str(len(CCWMs)))
        

    # Cretae the sorted pandas array of teams and their respective stats
    sorted_results_pd = pd.DataFrame({
        'Team':list(teamsList),
        'OPR' :convertToList(   OPRs),
        'AutoOPR':convertToList(AUTOs),
        'CCWM':convertToList(   CCWMs)
    })

    if (debug>2):
        print(info_i()+'  stripping column strings of sorted_results_pd')

    # Strip the columns. Really I'm not sure why I do this but I found it somewhere
    # and they told me to do it, and it's not breaking anything so why not.
    sorted_results_pd.columns=sorted_results_pd.columns.str.strip()

    if (debug>2):
        print(info_i()+'  Sorting sorted_results_pd')

    # Actually sort the pandas results
    sorted_results_pd.sort_values(by='OPR', ascending=False, inplace=True)

    # Remove the extra brackets
    try:
        sorted_results_pd['OPR'    ] = sorted_results_pd['OPR'    ].str.get(0)
        sorted_results_pd['AutoOPR'] = sorted_results_pd['AutoOPR'].str.get(0)
        sorted_results_pd['CCWM'   ] = sorted_results_pd['CCWM'   ].str.get(0)

    # AttributeError raised whenever sorted_results_pd is an empty dataframe
    except AttributeError as e:
        # so just do nothing
        sorted_results_pd['OPR'    ] = sorted_results_pd['OPR'    ]
        sorted_results_pd['AutoOPR'] = sorted_results_pd['AutoOPR']
        sorted_results_pd['CCWM'   ] = sorted_results_pd['CCWM'   ]
    
    # Any other exceptions, raise the error but print info about it for debug
    except Exception as e:
        print('info:')
        print('output_file_path:'+str(output_file_path))
        print('sorted_results_pd:')
        print(sorted_results_pd)
        print('matches:')
        print(matches)
        print("M:")
        print(M)
        print('\n\n\n\nn\n\n\n\n\n\n')
        raise e
        
    return sorted_results_pd





def return_opr_for_matches(matches, specific_team, debug=0, load_m=False):
    """
    Calculates OPR based on input matchs
    """
    # Build M
    M = build_m(load_m, matches, debug=debug)

    if (debug >0):
        print()
        print(info_i()+" 4 Building Scores")

    # Build scores
    Scores, Autos, Margins = build_scores(matches)

    if (debug>2):
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

    if (debug>1):
        # Convert all matrices from type list to type matrix using numpy
        print(info_i()+" Memory Update:")
        print('    |  - M (int8) - {}b or {}GB - Sizeof {} - M.size (# of elements) {}'.format(M.nbytes,byte_to_gb(M.nbytes),sys.getsizeof(M), M.size))
        print('    |  - Scores  - ' + str(Scores.nbytes)  + 'b  - ' + str(sys.getsizeof(Scores)))
        print('    |  - Autos   - ' + str(Autos.nbytes)   + 'b  - ' + str(sys.getsizeof(Autos)))
        print('    |  - Margins - ' + str(Margins.nbytes) + 'b  - ' + str(sys.getsizeof(Margins)))

    
    # collect garbage to save RAM
    gc.collect()
    
    if (debug>2):
        print(info_i()+'  Garbage collected')
        print(info_i()+'  Now using calculate_opr() to calculate OPRs, AUTOs, and CCWMs...')
    
    # This is the real RAM-intense operation...
    # Actually calculate the OPR
    OPRs, AUTOs, CCWMs = calculate_opr(M, Scores, Autos, Margins, debug=debug)


    if (debug>2):
        print(green_check()+'  OPRs, AUTOs, and CCWMS calculated. Displaying below:')
        print(info_i()+'OPRs')
        print(OPRs)
        print()
        print(info_i()+'AUTOs')
        print(AUTOs)
        print()
        print(info_i()+'CCWMs')
        print(CCWMs)
        print()

    
    # create the unsorted list of teams
    teamsList   = list(teams) # unsorted list of teams

    #sorted_results_pd = create_and_sort_stats(teamsList, OPRs, AUTOs, CCWMs, debug=debug)

    teamsList.index
    raise IndentationError('I really have no clue what I\'m doing here. Good luck building this! It is not complete.')
    return ()
    #return sorted_results_pd





#
# Setup
#
#

#eventcode=sys.argv[-1]

debug_level = 1

do_opr_for_all_time = True
do_opr_event_only   = True
do_opr_recent       = True

try:
    team_to_get = int(sys.argv[-1])

except Exception as e:
    print('\n\n !!!!  You need to specify a team to get stats for! (specify teamnumber as the last argument to the script)\n\n')
    raise e


# !!!!!!! TODO: get all events for the team, then calculate OPRs for those events, then put everything into a pandas dataframe and save as csv !!!!






#
#
#
#
# Now calculate OPR within event
#
#
#

if ('quiet' not in sys.argv):
    #print(green_check()+'Calculated OPR for all matches.')
    
    print(info_i()+'  --  --  --  --  --  --  --  --  --')
    print(info_i()+' Preparing for OPR calculation with specific event code '+str(EVENTCODE))
    print(info_i()+' ')


if CRAPPY_LAPTOP:
    gc.collect()

# Prepares the OPR calculation
#Arguments:
#  - specific_event (list) - returns only the data pertaining to the specified event code.
#  - specific_teams (list) - filters all matches by the given teams
#  - specific_event_teams (str) - returns data only for all teams in specified event code.
jsonparse.prepare_opr_calculation(specific_teams=team_to_get, debug=bool(True if debug_level>0 else False))

matches = loadMatchesByRecent(filter_by_teams=[team_to_get])


if ('quiet' not in sys.argv):
    print(info_i()+'Calculating OPR for matches within event...')
    print(info_i()+" 1 Loading teams")

#print(matches.shape)
#print('matches by recent:')
#print(matches)
#do_all_opr_stuff(
#    matches = matches, 
#    output_file_path = PATH_TO_FTCAPI+'opr/team-stats.csv', 
#    debug   = debug_level, 
#    load_m  = False
#)

if ('quiet' not in sys.argv):
    print(green_check()+'Calculated stats for team '+str(team_to_get))





if ('quiet' not in sys.argv):
    print(info_i()+' That took '+str(time.time()-starttime) + ' seconds.')
    print(green_check()+' [OPRv3-event.py] Done!    Next probable step: to push the data to the sheets via sheetsapi.py')
    print('\n\n\n\n\n\n\n\n\n\n\n\n')




# -- End of file --