#
# -*- coding: utf-8 -*-
# Sheets API
# Started on an unmarked date
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
This script provides an interface for pulling and pushing data to/from a Google Sheets spreadsheet.

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

Lots of help from https://github.com/googleapis/google-api-python-client/blob/main/samples/service_account/tasks.py
    and https://developers.google.com/sheets/api/quickstart/python
    as well as lots of documentation.
"""



#region Imports
# Builtins
import datetime
import pickle
import logging


# Intraproject imports
from common_resources import PATH_TO_FTCAPI, SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, create_logger
from common_resources import DEBUG_LEVEL

from json_parse import *

logger = create_logger("sheets_api")
logger.info("Setting up...")

# External imports
import pandas as pd

# Import Google stuff
try:
    from google.oauth2 import service_account
    import google.auth.exceptions
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

except ImportError as e:
    logger.error("[imports] ImportError while importing the google apiclient modules - Are you using the correct virtual environment? Full error info:"+str(e))
    raise e

#endregion Imports


#region Constants

# Don't change scopes unless modifying this script to access a google service other than spreadsheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

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
    Builds and returns Google credentials.

    Arguments:
    credentials -- Any existing credentials (default: None)
    """
    if DEBUG_LEVEL>1:
        logger.info("[build_credentials] Starting to build credentials.")
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            if DEBUG_LEVEL>1:
                logger.info("[build_credentials] Credentials are expired. Refreshing.")
            
            logger.error("[build_credentials] I raised a UserWarning because Request() is not defined and I'm not sure why. This has to do with google api credentials validation. Please do not ignore this error.")
            raise UserWarning("This should be changed")
            #credentials.refresh(Request())
        
        else:
            if DEBUG_LEVEL>1:
                logger.debug("[build_credentials] Credentials are nonexistent. Using the service account file")
            
            
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            
            except FileNotFoundError as e:
                logger.error(f"[build_credentials] FIleNotFoundError while building credentials for the Google Sheets API, probably because either the variable SERVICE_ACCOUNT_KEY_PATH in .env is malformed or because you haven't made a service account file.")
                logger.error(f'  SERVICE_ACCOUNT_FILE="{SERVICE_ACCOUNT_FILE}" Full error info: "{str(e)}"')
                raise e

            #flow = InstalledAppFlow.from_client_secrets_file(
            #  SERVICE_ACCOUNT_FILE, SCOPES
            #)
            #creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        #with open("token.json", "w") as token:
        #    token.write(creds.to_json())

    elif DEBUG_LEVEL>1:
        logger.debug("[build_credentials] Credentials already exist and are valid. Returning current credentials.")

    return credentials


def add_timestamp(lst: list):
    """ Adds a timestamp to the beginning of a given list. """
    lst = lst[::-1]
    lst.append([datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")])
    lst = lst[::-1]
    return lst
#endregion utils


#region gets
def get_data(service, sheetid: str, range: str, credentials=build_credentials()):
    """ Uses Google's Sheets API to pull data from a spreadsheet.

    Arguments:
    service -- A service object built via build()
    sheetid -- A string containing the unique id of the Google Sheet
    range -- A string containing the range of cells to pull data from
    credentials -- Credentials built using the build_credentials() function
    """
    logger.debug(f"[get_data] Getting data from range {range}...")

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
            logger.debug("[get_data] No data found. Returning None.")

            return None

        return values

        #logger.debug("Values raw: ")
        #logger.debug(values)
         
    except HttpError as err:
        logger.error("[get_data] HttpError while calling the Sheets API. Full Error: "+str(err))
        raise err

def get_elims_matches(service, credentials):
    """
    Pulls elims match data.

    Pulls the Eliminations match data from the Google Sheets, and returns a Pandas Dataframe containing the team numbers for each team.
    
    Arguments:
    service -- A service object built via build()
    credentials -- Credentials built using the build_credentials() function
    """
    logger.debug("[get_elims_matches] Getting matches in the elims combinations.")
    
    elims_data_raw = get_data(service, sheetid=SPREADSHEET_ID, range=MATCHES_READ_ELIMS_RANGE, credentials=credentials)

    if DEBUG_LEVEL>1:
        logger.debug("[get_elims_matches] Data recieved. Processing data...")
    
    elims_match_teams = {"Red1":[],"Red2":[],"Blue1":[],"Blue2":[]}


    for row in elims_data_raw:
        #if debug:
        #    logger.debug("\n"+"    "", end="")

        #for col in row:
            #if debug:
            #    logger.debug(col, end=" | ")
            
        if type(row) != type(None) and len(row) > 0:
            elims_match_teams["Red1"].append(row[0])
            elims_match_teams["Red2"].append(row[2])
            elims_match_teams["Blue1"].append(row[5])
            elims_match_teams["Blue2"].append(row[7])

    elims_match_teams = pd.DataFrame(elims_match_teams)

    if DEBUG_LEVEL>1:
        logger.debug("[get_elims_matches] Data processed. and dataframed.")
        #logger.debug(elims_match_teams)
    
    return elims_match_teams

def get_event_data(event_object, event_schedule_qual, event_schedule_playoff, playoff_only=False):
    """
    Returns data about matches in an event, in >2D list format.
    
    Arguments:
    event_object -- TODO: Add this description
    event_schedule_qual -- TODO: Add this description
    event_schedule_playoff -- TODO: Add this description
    playoff_only (optional) --  (default: False)
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
    """ Returns a pandas DataFrame from a given filepath to a .csv file """
    return pd.read_csv(filepath)
#endregion gets


#region pushes
def push_data(service, sheetid: str, range: str, credentials, data):
    """
    Pushes data to a Google Sheets spreadsheet.
    

    Arguments:
    service -- A service object built via build()
    sheetid -- A string containing the unique id of the Google Sheet
    range -- A string containing the range of cells to push data to
    credentials -- Credentials built using the build_credentials() function
    data -- A 2D list, see the format below:
    The data is in the format of a 2d list;
    [
        #row
        [
            #column, column, column
        ]
    ]
    """
    if DEBUG_LEVEL>1:
        logger.debug("[push_data] Pushing data to range {}...".format(range))
    
    try:
        
        # First, clear all the cells to prevent overlap
        # with help from https://stackoverflow.com/questions/41986898/google-sheets-api-python-clear-sheet
        body = {}
        resultClear = service.spreadsheets().values().clear(spreadsheetId=sheetid, range=range, body=body).execute()
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
        if DEBUG_LEVEL>1:
            logger.debug(f"[push_data] {result.get('updatedCells')} cells updated.")
        
        return result
    
    except HttpError as error:
        logger.error(f"[push_data] Some HttpError occured! range={range}, sheetid={sheetid}, service={service}, Full error info:{error}")
        logger.debug("    data:"+str(data))
        
        return error
    
    except google.auth.exceptions.TransportError as error:
        logger.error( " [push_data] Google Authentication TransportError! Most likely due to a weak connection or incorrectly set up DNS.")
        logger.error(f" Full error info: {error}")
        raise error
    
    except KeyboardInterrupt as error:
        raise error
    
    except Exception as error:
        logger.error(f" [push_data] Some unknown Exception occured! Not a HttpError or google.auth.exceptions.TransportError. Full error info: {error}")
        raise error



def push_matches(service):
    """
    Pushes match data to a Google Spreadsheet.

    More specifically, this function gathers data from the machinelearning/eventdata
    folder, predicts the matches, and pushes the data to the Google Sheets.

    Arguments:
    service -- A service object built via build()
    """
    
    logger.info("[push_matches] Pushing matches data to sheets")
        
    if DEBUG_LEVEL>1:
        logger.debug(" This function uses:")
        logger.debug("   - eventdata/event_matches.json")
        logger.debug("   - eventdata/eventschedule_qual.json")
        logger.debug("   - eventdata/eventschedule_playoff.json")
    
    write_to_range = MATCHES_WRITE_RANGE

    # Get the data
    event_object   = EventMatches(get_json(os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_matches.json")))
    event_schedule_qual    = EventSchedule(get_json(os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","eventschedule_qual.json")))
    event_schedule_playoff = EventSchedule(get_json(os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","eventschedule_playoff.json")))


    with open(os.path.join(PATH_TO_FTCAPI,"gsNeigh.pkl"), "rb") as f:
        gsNeigh = pickle.load(f)
    
    with open(os.path.join(PATH_TO_FTCAPI,"gsSVC.pkl"),"rb") as f:
        gsSVC = pickle.load(f)
    
    predictors = [gsNeigh, gsSVC]

    # Predict the outcomes of the matches
    logger.info(" [push_matches] Predicting matches")

    event_object.predict_outcomes(          predictors=predictors, inplace=True)
    event_schedule_qual.predict_outcomes(   predictors=predictors, inplace=True)
    event_schedule_playoff.predict_outcomes(predictors=predictors, inplace=True, level="playoff") # the "level" flag is set to ignore the warning that comes from an empty dataframe before playoff schedules are released.


    data_to_push   = get_event_data(event_object, event_schedule_qual, event_schedule_playoff)
    
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push)
    
    logger.info(" Pushing data")

    
    # Push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )

    logger.info(" Done pushing matches data!")


def push_teams(service):
    """
    Pushes team data to a Google Spreadsheet
    
    More specifically, this function gathers data from the sorted stats in
    the generatedfiles/opr folder and pushes the data to the Google Sheets.

    Arguments:
    service -- A service object built via build()
    """
    logger.info("[push_teams] Pushing teams data to sheets")

    if DEBUG_LEVEL>1:
        logger.debug(" This function uses:")
        logger.debug("   - opr_result_sorted.csv")
        logger.debug("   - opr_recent_result_sorted.csv")
        logger.debug("   - opr_event_result_sorted.csv")
    #
    # Write season-long OPR data
    #
    if DEBUG_LEVEL>1:
        logger.debug("    Writing season-long OPR data")
        
    write_to_range = TEAMS_WRITE_RANGE
    data_to_push   = get_team_data(os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_result_sorted.csv"))
    
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push.values.tolist())

    if DEBUG_LEVEL>1:
        logger.debug("    Pushing data")
        
    # Push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )

    
    #
    # Write event OPR data
    #
    if DEBUG_LEVEL>1:
        logger.debug("    Writing event OPR data")
        
    write_to_range = TEAMS_EVENT_WRITE_RANGE
    data_to_push   = get_team_data(os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_event_result_sorted.csv"))
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push.values.tolist())

    if DEBUG_LEVEL>1:
        logger.debug("    Pushing data")
        
    # Push the data
    if len(data_to_push)==1:
        logger.debug("[push_teams] There is no data for the event OPR! Pushing a timestamp with a message.")
        logger.warning("[push_teams] No data exists for event OPR. This is normal if no match scores are out.")
        data_to_push.append(["Event has no OPR data","Event has probably not started yet."])
        
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )


    #
    # Write recent OPR data
    #
    if DEBUG_LEVEL>1:
        logger.debug("    Writing recent OPR  data")
        
    write_to_range = TEAMS_RECENT_WRITE_RANGE
    data_to_push   = get_team_data(os.path.join(PATH_TO_FTCAPI,"generatedfiles","opr","opr_recent_result_sorted.csv"))
    # Add the timestamp to the begining of the data
    data_to_push = add_timestamp(data_to_push.values.tolist())

    if DEBUG_LEVEL>1:
        logger.debug("    Pushing data")
    
    # push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )

    logger.info(" done pushing teams data!")



def push_rankings(service):
    """
    Pushes ranking data to a Google Spreadsheet.

    More specifically, this function gathers data from the machinelearning/eventdata
    folder and pushes the data to the Google Sheets.

    Arguments:
    service -- A service object built via build()
    """
    logger.info(" [push_rankings] Pushing rankings data to sheets")
    
    if DEBUG_LEVEL>1:
        logger.debug("  This function uses:")
        logger.debug("    -",os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_rankings.json"))
        logger.debug("  This function creates:")
        logger.debug("    -",os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_rankings.csv"))
        
    #
    # Write event ranking data
    #
    if DEBUG_LEVEL>1:
        logger.debug(" Writing event ranking data")
        
    # from jsonparse, save the rankings dataframe as a csv
    try:
        rankings_dataframe(os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_rankings.json"),os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_rankings.csv"))

    except IndexError as e:
        logger.warning(f"[push_rankings] IndexError with rankngs_dataframe in jsonparse. This indicates that eventdata/event_rankings.json is either empty or malformed. This is normal if the event hasn\'t started yet. full error msg: {e}")
        raise e
    
    write_to_range = TEAMS_RANKING_WRITE_RANGE
    
    try:
        data_to_push   = pd.read_csv(os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_rankings.csv"))
        # Dropping multiple columns with help from 
        # https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
        data_to_push.drop(
            ["displayTeamNumber","sortOrder1","sortOrder2","sortOrder3","sortOrder4","sortOrder5","sortOrder6"], 
            axis=1, 
            inplace=True
        )

        # Add the timestamp to the begining of the data
        data_to_push = add_timestamp(data_to_push.values.tolist())

    except pd.errors.EmptyDataError:
        # if the file is empty
        data_to_push = [["No rankings for the given event"],[f'({os.path.join(PATH_TO_FTCAPI,"generatedfiles","eventdata","event_rankings.csv")} is empty)']]
        logger.warning("[push_rankings] generatedfiles/eventdata/event_rankings.csv is empty. This is normal if an event hasn\'t started yet, but is bad if the rankings are out.")
    
    

    if DEBUG_LEVEL>1:
        logger.debug("    Pushing data")
        
    # push the data
    push_data(
        service, SPREADSHEET_ID, write_to_range, credentials, 
        data_to_push
    )


    logger.info(" Done pushing rankings data!")


def push_elims_predictions(service):
    """
    Pushes the predictions for the elims based on the input predictions (DataFrame).
    """
    logger.info(" [push_elims_predictions] Pushing elims prediction data to sheets.")
    
    # get the data
    elims_matches = get_elims_matches(service, credentials)

    jsonified_elims_matches = {"schedule":[]}

    #if debug:
    #    logger.debug("elims_matches iterrows stuff") #TODO remove this debug print
    for index, i in elims_matches.iterrows():

        #if debug:
        #    logger.debug(i)
        jsonified_elims_matches["schedule"].append(
            {"description": "<placeholder>",
          "field": "<placeholder>",
          "tournamentLevel": "<placeholder elims>",
          "startTime": "2000-01-01T00:00:00.000Z",
          "matchNumber": 0,
          "teams": [
            {
              "teamNumber": i["Red1"],
              "station": "Red1"
            }, {
              "teamNumber": i["Red2"],
              "station": "Red2"
            }, {
              "teamNumber": i["Blue1"],
              "station": "Blue1"
            }, {
              "teamNumber": i["Blue2"],
              "station": "Blue2"
            }
           ],
           "modifiedOn": "2000-01-01T00:00:00.000Z"
         }
        )

    if DEBUG_LEVEL>1:
        logger.debug(" [push_elims_predictions] Elims matches data recieved. Now loading models.")

    with open(os.path.join(PATH_TO_FTCAPI,"gsNeigh.pkl"), "rb") as f:
        gsNeigh = pickle.load(f)
    
    with open(os.path.join(PATH_TO_FTCAPI,"gsSVC.pkl"),"rb") as f:
        gsSVC = pickle.load(f)
    
    predictors = [gsNeigh, gsSVC]

    # Predict the outcomes of the matches
    logger.info(" [push_elims_predictions] Predicting matches.")

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
    
    if logger.isEnabledFor(logging.DEBUG):
        debug_text = ""
        for row in data_to_push:
            debug_text.append("  ")
            for column in row:
                debug_text.append(str(column)+" | ")
        
        logger.debug(debug_text)

    if DEBUG_LEVEL>1:
        logger.debug(" Pushing data")

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

    logger.info(" Done pushing matches data!")


#endregion pushes

#region Procedural

def master_function(arguments:list):
    global credentials
    global service

    # Get the credentials
    credentials = build_credentials()

    # Build the service
    service = build("sheets", "v4", credentials=credentials)


    if ("matches" in arguments):
        push_matches(service)

    if ("elims" in arguments):
        push_elims_predictions(service)

    if ("teams" in arguments):
        push_teams(service)

    if ("rankings" in arguments):
        push_rankings(service)


    if ("help" in arguments) or ("-help" in arguments) or ("--help" in arguments):
        logger.info("   Sheetsapi.py")
        logger.info("   By Drew Wingfield")
        logger.info(" Usage: python3 sheetsapi.py [teams/matches/elims/rankings/help]")
        logger.info(" If something is going wrong, check the id of the spreadsheet we are pushing data to.")
        logger.info("    quiet - Don\'t print output unless there is an error")


    elif ("matches" not in arguments) and ("teams" not in arguments) and ("rankings" not in arguments) and ("elims" not in arguments):
        logger.error(" master_function called without correct arguments! arguments="+str(arguments))
        raise Exception("\n\n\nYou must call master_function with arguments! (matches and/or teams) - Please use the -help modifier to see the help menu.\n")



if __name__ == "__main__":
    import sys
    logger.debug("sheets_api was called as __main__")
    master_function(sys.argv)


#endregion Procedural

# -- End of file --