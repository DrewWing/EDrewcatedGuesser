#
# -*- coding: utf-8 -*-
# sheetsapi.py
# by Drew Wingfield

# lots of help from https://github.com/googleapis/google-api-python-client/blob/main/samples/service_account/tasks.py
# and https://developers.google.com/sheets/api/quickstart/python
# as well as lots of documentation and random other stuff.


#region Imports

# common resources
from commonresources import PATH_TO_FTCAPI, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, log_error

from python_settings import PythonSettings
settings = PythonSettings()

# import google stuff
try:
    from google.oauth2 import service_account
    import google.auth.exceptions
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

except ImportError as e:
    log_error('[sheetsapi.py][imports] ImportError while importing the google apiclient modules - Are you using the correct virtual environment? Full error info:'+str(e))
    print("\n\n------\nIf you're seeing this, the googleapiclient module couldn't be imported")
    print("Try these things:")
    print("  - Activating the virtual environment before running this script (source virtenv1/bin/activate)")
    print("  - making sure the googleapiclient is installed to the virtual environment")
    print("    (/home/wingfield/virtenv1/bin/pip install google-api-python-client)")
    print("  - The source can be found at https://github.com/googleapis/google-api-python-client")
    print("  - Also see https://realpython.com/python-virtual-environments-a-primer/")
    print("Good luck!\n")
    raise e


import pandas as pd

# sys
import sys
import datetime

# import json parser
from jsonparse import *

#endregion Imports


#region Constants

# Don't change scopes unless modifying it to access something other than spreadsheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

# Write ranges
MATCHES_WRITE_RANGE  = "API Stuff!B5:Y"
MATCHES_WRITE_METADATA_RANGE  = "API Stuff!B1:G4"

TEAMS_WRITE_RANGE  = "API-Teams!B5:H"
TEAMS_EVENT_WRITE_RANGE     = "API-Teams!J5:Q"
TEAMS_RECENT_WRITE_RANGE    = "API-Teams!S5:Z"
TEAMS_RANKING_WRITE_RANGE   = "API-Teams!AC5:AL"

MATCHES_READ_ELIMS_RANGE = "Finals!C9:L"
PREDICTIONS_WRITE_ELIMS_RANGE = "Finals!N9:O"

TEAMS_WRITE_METADATA_RANGE  = "API-Teams!B1:G4"
#endregion Constants


#region utils
def build_credentials(credentials=None):
    """
    Builds the google credentials.
    Returns the credentials
    """
    if settings.debug_level>1:
        print(info_i()+"[sheetsapi.py] [build_credentials] Starting to build credentials.")
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            if settings.debug_level>1:
                print("[sheetsapi.py] [build_credentials] Credentials are expired. Refreshing.")
            
            log_error('[sheetsapi.py][build_credentials] I raised a UserWarning because Request() is not defined and I\'m not sure why. This has to do with google api credentials validation. Please do not ignore this error.')
            raise UserWarning('This should be changed')
            #credentials.refresh(Request())
        
        else:
            if settings.debug_level>1:
                print(info_i()+"[sheetsapi.py] [build_credentials] Credentials are nonexistent. Using the service account file")
            
            
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
            except FileNotFoundError as e:
                log_error(f'[sheetsapi][build_credentials] FIleNotFoundError while building credentials for the Google Sheets API, probably because either the variable SERVICE_ACCOUNT_FILE in commonresources.py is malformed or because you haven\'t made a service account file.')
                log_error(f'                               SERVICE_ACCOUNT_FILE: "{SERVICE_ACCOUNT_FILE}" Full error info: "{str(e)}"')
                raise e

            #flow = InstalledAppFlow.from_client_secrets_file(
            #  SERVICE_ACCOUNT_FILE, SCOPES
            #)
            #creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        #with open("token.json", "w") as token:
        #    token.write(creds.to_json())

    elif settings.debug_level>1:
        print(info_i()+"[sheetsapi.py] [build_credentials] Credentials already exist and are valid. Returning current credentials.")

    return credentials


def add_timestamp(lst: list):
    """
    Adds a timestamp to the beginning of a given list
    """
    lst = lst[::-1]
    lst.append([datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")])
    lst = lst[::-1]
    return lst
#endregion utils


#region gets
def get_data(service, sheetid: str, range: str, credentials=build_credentials()):
    if settings.debug_level>0:
        print(info_i()+" [sheetsapi.py] [get_data] Getting data from range {}...".format(range))

    try:
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=sheetid, range=range)
            #.batchGet(spreadsheetId=sheetid,ranges=[range],majorDimension="ROWS")
            .execute()
        )
        values = result.get("values", [])

        if not values:
            if settings.debug_level>0:
                print(info_i()+" [sheetsapi.py] [get_data] No data found. Returning None.")

            return None

        return values

        #print("Values raw: ")
        #print(values)
         
    except HttpError as err:
        log_error('[sheetsapi.py][get_data] HttpError while calling the Sheets API. Full Error: '+str(err))

        if settings.debug_level>0:
            print(red_x()+"[sheetsapi.py] [get_data] HTTPError occured! Printing error info...")
        print(err)
        raise err

def get_elims_matches(service, credentials):
    """
    Gets the elims match data from the sheets, and returns a Dataframe containing the team numbers for each team.
    """
    if settings.debug_level>0:
        print(info_i()+' [sheetsapi.py][get_elims_matches] Getting matches in the elims combinations.')
    
    e = get_data(service, sheetid=SPREADSHEET_ID, range=MATCHES_READ_ELIMS_RANGE, credentials=credentials)

    if settings.debug_level>1:
        print(info_i()+' [sheetsapi.py][get_elims_matches] Data recieved. Processing data...')
    
    elims_match_teams = {'Red1':[],'Red2':[],'Blue1':[],'Blue2':[],}


    for row in e:
        #if debug:
        #    print('\n'+info_i()+'    ', end='')

        #for col in row:
            #if debug:
            #    print(col, end=' | ')
            
        if type(row) != type(None) and len(row) > 0:
            elims_match_teams['Red1'].append(row[0])
            elims_match_teams['Red2'].append(row[2])
            elims_match_teams['Blue1'].append(row[5])
            elims_match_teams['Blue2'].append(row[7])

    elims_match_teams = pd.DataFrame(elims_match_teams)

    if settings.debug_level>1:
        print(info_i()+' [sheetsapi.py][get_elims_matches] Data processed. and dataframed.')
        #print(elims_match_teams)
    
    return elims_match_teams

def get_event_data(event_object, event_schedule_qual, event_schedule_playoff, playoff_only=False):
    """
    Returns data about matches in an event, in >2D list format.

    """
    data_to_push = []
    c=0 # total count of matches
    
    if not playoff_only:
        for i in event_object.matches_split:
            c+=1
            data_to_push.append(i)

        # If still in quals (scored matches < # of qual matches scheduled)
        if event_object.number_of_matches < event_schedule_qual.number_of_matches:
            d = 0
            # Iterate over matches in the schedule
            for i in event_schedule_qual.matches_split:
                d += 1
                if d > c: # if greater than total # of matches already appended, add it
                    data_to_push.append(i)

            for i in event_schedule_playoff.matches_split:
                data_to_push.append(i)
        
        # If in elims (# of matches scored < # of qual and playoff matches scheduled)
        elif event_object.number_of_matches < (event_schedule_qual.number_of_matches + event_schedule_playoff.number_of_matches):
            d = 0
            for i in event_schedule_playoff.matches_split:
                d += 1
                if d > c:
                    data_to_push.append(i)
    

    # If the playoff_only flag is set
    else:
        d = 0
        for i in event_schedule_playoff.matches_split:
            d += 1
            if d > c:
                data_to_push.append(i)

    return data_to_push


def get_team_data(filepath: str):
    """
    Returns a pandas DataFrame from a given filepath to a .csv file
    """
    return pd.read_csv(filepath)
#endregion gets


#region pushes
def push_data(service, sheetid: str, range: str, credentials, data):
    """
    Pushes data to a sheet.
    The data is in the format of a 2d list;
    [
        #row
        [
            #column, column, column
        ]
    ]
    """
    if settings.debug_level>1:
        print(info_i()+" [sheetsapi.py] [push_data] Pushing data to range {}...".format(range))
    
    try:
        
        # First, clear all the cells to prevent overlap
        # with help from https://stackoverflow.com/questions/41986898/google-sheets-api-python-clear-sheet
        body = {}
        resultClear = service.spreadsheets( ).values( ).clear( spreadsheetId=sheetid, range=range,
                                                       body=body ).execute( )
        # then push the data
        
        body = {"values": data}
        
        result = (
        service.spreadsheets()
            .values()
            .update(
                spreadsheetId = sheetid,
                range = range,
                valueInputOption = "USER_ENTERED",
                body  = body,
            )
            .execute()
        )
        if settings.debug_level>1:
            print(f"{info_i()}     {result.get('updatedCells')} cells updated.")
        
        return result
    
    except HttpError as error:
        log_error(f'[sheetsapi.py][push_data] Some HttpError occured! range={range}, sheetid={sheetid}, service={service}, Full error info:{error}')
        print(red_x()+" [sheetsapi.py][push_data] An error occurred!")
        print(red_x()+"    Some info:")
        print(red_x()+"    debug_level:"+str(settings.debug_level))
        print(red_x()+"    range:"+str(range))
        print(red_x()+"    sheetid:"+str(sheetid))
        print(red_x()+"    service:"+str(service))
        #print(red_x()+"    data:"+str(data))
        print()
        
        return error
    
    except google.auth.exceptions.TransportError as error:
        print(red_x()+" [sheetsapi][push_data] Google Authentication TransportError!")
        print(red_x()+"         Most likely due to a weak connection or incorrectly set up DNS.")
        print(red_x()+f"         Full error info: {error}")
        log_error("[sheetsapi][push_data] Google Authentication TransportError! Most likely due to weak connection or incorrectly set up DNS.")
        log_error(f"         Full error info: {error}")
        log_error("           Error has been printed and raised, irreguardless of debug_level setting.")
        raise error
    
    except KeyboardInterrupt as error:
        raise error
    
    except Exception as error:
        log_error(f" [sheetsapi][push_data] Some unknown Exception occured! Not a HttpError or google.auth.exceptions.TransportError. Full error info: {error}")
        raise error



def push_matches(service):
    if settings.debug_level>0:
        print(info_i()+' [sheetsapi.py][push_matches] Pushing matches data to sheets')
        
    if settings.debug_level>1:
        print(info_i()+'     Uses:')
        print(info_i()+'       - eventdata/eventmatches.json')
        print(info_i()+'       - eventdata/eventschedule-qual.json')
        print(info_i()+'       - eventdata/eventschedule-playoff.json')
    
    write_to_range = MATCHES_WRITE_RANGE

    # get the data
    event_object   = EventMatches(get_json(PATH_TO_FTCAPI+"eventdata/eventmatches.json"))
    event_schedule_qual    = EventSchedule(get_json(PATH_TO_FTCAPI+'eventdata/eventschedule-qual.json'))
    event_schedule_playoff = EventSchedule(get_json(PATH_TO_FTCAPI+'eventdata/eventschedule-playoff.json'))

    import pickle

    with open(PATH_TO_FTCAPI+'gsNeigh.pkl', 'rb') as f:
        gsNeigh = pickle.load(f)
    
    with open(PATH_TO_FTCAPI+'gsSVC.pkl','rb') as f:
        gsSVC = pickle.load(f)
    
    predictors = [gsNeigh, gsSVC]

    # Predict the outcomes of the matches
    if settings.debug_level>1:
        print(info_i()+' [sheetsapi.py][push_matches] Predicting matches.')

    event_object.predict_outcomes(          predictors=predictors, inplace=True)
    event_schedule_qual.predict_outcomes(   predictors=predictors, inplace=True)
    event_schedule_playoff.predict_outcomes(predictors=predictors, inplace=True, level="playoff") # the "level" flag is set to ignore the warning that comes from an empty dataframe before playoff schedules are released.


    data_to_push   = get_event_data(event_object, event_schedule_qual, event_schedule_playoff)
    
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push)
    
    if settings.debug_level>0:
        print(info_i()+' Pushing data')

    
    # push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )

    if settings.debug_level>0:
        print(green_check()+' [sheetsapi.py] Done pushing matches data!')



def push_all_matches_heatmap(service):
    if settings.debug_level>0:
        print(info_i()+' [sheetsapi.py] Pushing all matches data for sheets heatmap')
    if settings.debug_level>1:
        print(info_i()+'    Uses:')
        print(info_i()+'      - all-matches.csv')
    
    write_to_range = MATCHES_WRITE_RANGE

    # gets all matches and saves it to all-matches.csv
    import jsonparse
    jsonparse.prepare_opr_calculation()

    # get the data
    data_to_push   = pd.read_csv(PATH_TO_FTCAPI+'all-matches.csv').toList()
    
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push)
    
    if settings.debug_level>0:
        print(info_i()+' Pushing data')

    
    # push the data
    push_data(
        service, "1SNiuJIEgJQrqIv7QS6E5AlT3WDz73UXuF00aXiTCJw4", "'API Stuff'!B6:N26000", credentials, 
        data_to_push
    )

    if settings.debug_level>0:
        print(green_check()+' [sheetsapi.py] done pushing matches data!')



def push_teams(service):
    """
    Pushes the team data to the spreadsheet
    """
    if settings.debug_level>0:
        print(info_i()+' [sheetsapi.py] Pushing teams data to sheets')
    if settings.debug_level>1:
        print(info_i()+'    Uses:')
        print(info_i()+'      - opr-result-sorted.csv')
        print(info_i()+'      - opr-recent-result-sorted.csv')
        print(info_i()+'      - opr-event-result-sorted.csv')
    #
    # Write season-long OPR data
    #
    if settings.debug_level>1:
        print(info_i()+'    Writing season-long OPR data')
        
    write_to_range = TEAMS_WRITE_RANGE
    data_to_push   = get_team_data(PATH_TO_FTCAPI+'opr/opr-result-sorted.csv')
    
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push.values.tolist())

    if settings.debug_level>1:
        print(info_i()+'    Pushing data')
        
    # push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )

    
    #
    # Write event OPR data
    #
    if settings.debug_level>1:
        print(info_i()+'    Writing event OPR data')
        
    write_to_range = TEAMS_EVENT_WRITE_RANGE
    data_to_push   = get_team_data(PATH_TO_FTCAPI+'opr/opr-event-result-sorted.csv')
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push.values.tolist())

    if settings.debug_level>1:
        print(info_i()+'    Pushing data')
        
    # push the data
    if len(data_to_push)==1:
        if settings.debug_level>0:
            print(info_i()+'    There is no data for the event OPR! Pushing a timestamp with a message.')
            log_error('[sheetsapi.py][push_teams] No data exists for event OPR. This is normal if no match scores are out.',level='Info')
        data_to_push.append(['Event has no OPR data','Event has probably not started yet.'])
        
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )


    #
    # Write recent OPR data
    #
    if settings.debug_level>1:
        print(info_i()+'    Writing recent OPR  data')
        
    write_to_range = TEAMS_RECENT_WRITE_RANGE
    data_to_push   = get_team_data(PATH_TO_FTCAPI+'opr/opr-recent-result-sorted.csv')
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push.values.tolist())

    if settings.debug_level>1:
        print(info_i()+'    Pushing data')
    
    # push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )

    if settings.debug_level>0:
        print(green_check()+' [sheetsapi.py] done pushing teams data!')



def push_rankings(service):
    """
    Pushes ranking data to the sheet
    """
    if settings.debug_level>0:
        print(info_i()+' [sheetsapi.py] Pushing rankings data to sheets')
    if settings.debug_level>1:
        print(info_i()+'    Uses:')
        print(info_i()+'      - eventdata/eventrankings.json')
        print(info_i()+'    Creates:')
        print(info_i()+'      - eventdata/eventrankings.csv')
        
    #
    # Write event ranking data
    #
    if settings.debug_level>1:
        print(info_i()+'    Writing event ranking data')
        
    # from jsonparse, save the rankings dataframe as a csv
    try:
        rankings_dataframe(PATH_TO_FTCAPI+'eventdata/eventrankings.json',PATH_TO_FTCAPI+'eventdata/eventrankings.csv')

    except IndexError as e:
        log_error(f'[sheetsapi.py][push_rankings] IndexError with rankngs_dataframe in jsonparse. This indicates that eventdata/eventrankings.json is either empty or malformed. This is normal if the event hasn\'t started yet. full error msg: {e}')
        raise e
    
    write_to_range = TEAMS_RANKING_WRITE_RANGE
    
    try:
        data_to_push   = pd.read_csv(PATH_TO_FTCAPI+'eventdata/eventrankings.csv')
        # Dropping multiple columns with help from 
        # https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
        data_to_push.drop(
            ['displayTeamNumber','sortOrder1','sortOrder2','sortOrder3','sortOrder4','sortOrder5','sortOrder6'], 
            axis=1, 
            inplace=True
        )

        # Add the timestamp to the begining of the data
        data_to_push = add_timestamp(data_to_push.values.tolist())

    except pd.errors.EmptyDataError:
        # if the file is empty
        data_to_push = [['No rankings for the given event'],['(eventdata/eventrankings.csv is empty)']]
        log_error('[sheetsapi.py][push_rankings] eventdata/eventrankings.csv is empty. This is normal if an event hasn\'t started yet, but is bad if the rankings are out.',level="Warn")
    
    

    if settings.debug_level>1:
        print(info_i()+'    Pushing data')
        
    # push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )


    if settings.debug_level>0:
        print(green_check()+' [sheetsapi.py] done pushing rankings data!')


def push_elims_predictions(service):
    """
    Pushes the predictions for the elims based on the input predictions (DataFrame).
    """
    if settings.debug_level>0:
        print(info_i()+' [sheetsapi.py][push_elims_predictions] Pushing elims prediction data to sheets.')
    
    # get the data
    elims_matches = get_elims_matches(service, credentials)

    jsonified_elims_matches = {'schedule':[]}

    #if debug:
    #    print('elims_matches iterrows stuff') #TODO remove this debug print
    for index, i in elims_matches.iterrows():

        #if debug:
        #    print(i)
        jsonified_elims_matches['schedule'].append(
            {"description": "<placeholder>",
          "field": "<placeholder>",
          "tournamentLevel": "<placeholder elims>",
          "startTime": "2000-01-01T00:00:00.000Z",
          "matchNumber": 0,
          "teams": [
            {
              "teamNumber": i['Red1'],
              "station": "Red1"
            }, {
              "teamNumber": i['Red2'],
              "station": "Red2"
            }, {
              "teamNumber": i['Blue1'],
              "station": "Blue1"
            }, {
              "teamNumber": i['Blue2'],
              "station": "Blue2"
            }
           ],
           "modifiedOn": "2000-01-01T00:00:00.000Z"
         }
        )

    import pickle

    if settings.debug_level>1:
        print(info_i()+' [sheetsapi.py][push_elims_predictions] Elims matches data recieved. Now loading models.')

    with open(PATH_TO_FTCAPI+'gsNeigh.pkl', 'rb') as f:
        gsNeigh = pickle.load(f)
    
    with open(PATH_TO_FTCAPI+'gsSVC.pkl','rb') as f:
        gsSVC = pickle.load(f)
    
    predictors = [gsNeigh, gsSVC]

    # Predict the outcomes of the matches
    if settings.debug_level>1:
        print(info_i()+' [sheetsapi.py][push_elims_predictions] Predicting matches.')

    #     "schedule": [
    #     {
    #       "description": "string",
    #       "field": "string",
    #       "tournamentLevel": "string",
    #       "startTime": "2024-02-10T20:15:45.887Z",
    #       "series": 0,
    #       "matchNumber": 0,
    #       "teams": [
    #         {
    #           "teamNumber": 0,
    #           "displayTeamNumber": "string",
    #           "station": "string",
    #           "team": "string",
    #           "teamName": "string",
    #           "surrogate": true,
    #           "noShow": true
    #         }
    #       ],
    #       "modifiedOn": "2024-02-10T20:15:45.887Z"
    #     }
    #   ]

    event_schedule_elims = EventSchedule(raw_json=jsonified_elims_matches)

    event_schedule_elims.predict_outcomes(predictors=predictors, inplace=True, level="playoff") # the "level" flag is set to ignore the warning that comes from an empty dataframe before playoff schedules are released.


    data_to_push   = get_event_data(event_object=[], event_schedule_qual=[], event_schedule_playoff=event_schedule_elims, playoff_only=True)
    
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push)
    
    for row in data_to_push:
        print('  ')
        for column in row:
            print(column, end=' | ')

    if settings.debug_level>1:
        print(info_i()+' Pushing data')

    #
    #row [
    #    #column, column, column
    #]
    #]
    
    # push the data
    push_data(
        service, SPREADSHEET_ID, PREDICTIONS_WRITE_ELIMS_RANGE, credentials, 
        data_to_push
    )

    if settings.debug_level>0:
        print(green_check()+' [sheetsapi.py] Done pushing matches data!')


#endregion pushes



# Get the credentials
credentials = build_credentials()

#build the service
service = build('sheets', 'v4', credentials=credentials)


#region arguments
if ('matches' in sys.argv):
    push_matches(service)

if ('elims' in sys.argv):
    push_elims_predictions(service)


if ('allmatchesheatmap' in sys.argv):
    push_all_matches_heatmap(service)


if ('teams' in sys.argv):
    push_teams(service)

if ('rankings' in sys.argv):
    push_rankings(service)


if ('help' in sys.argv) or ('-help' in sys.argv) or ('--help' in sys.argv):
    print('   Sheetsapi.py')
    print('   By Drew Wingfield')
    print(' Usage: python3 sheetsapi.py [teams/matches/quiet/help]')
    print(' If something is going wrong, check the id of the spreadsheet we are pushing data to.')
    print('    quiet - Don\'t print output unless there is an error')


elif ('matches' not in sys.argv) and ('teams' not in sys.argv) and ('rankings' not in sys.argv) and ('elims' not in sys.argv):
    log_error('[sheetsapi.py] Sheetsapi.py either called without correct arguments or imported (you should not do that). sys.argv='+str(sys.argv))
    raise Exception("\n\n\nYou must call sheetsapi.py with arguments! (matches and/or teams) - Please use the -help modifier to see the help menu\n\n\n\n\n\n\n\n\n\n")

#endregion arguments

# -- End of file --