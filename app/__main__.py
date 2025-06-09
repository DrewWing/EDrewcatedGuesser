#
# -*- coding: utf-8 -*-
# __main__.py
# Started 02-03-2025
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
The main program that runs everything else. Replaces the old PowerShell scripts.

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

Replaces the old PowerShell and BASH scripts.
"""


# Standard Imports
import os
import sys
import datetime
import time
import json
import logging

# Third-Party Imports
import requests
from dotenv import load_dotenv

# Local Imports
from common_resources import PROJECT_PATH, EVENT_CODE, SEASON_YEAR, create_logger
from common_resources import __version__, make_required_directories, CALCULATION_MODE, DEBUG_LEVEL
make_required_directories() # Make the required directories if they don't exist already.
import sheets_api


#region setup
FLUSH_DEBUG_LOG = os.getenv("FLUSH_DEBUG_LOG","true").lower() == "true"

logger = create_logger("__main__",flush_debug_log=FLUSH_DEBUG_LOG)
logger.info("Setting up...")

load_dotenv() # Load environment variables

DELAY_SECONDS   = int(os.getenv("DELAY_SECONDS", 120)) # Seconds between each cycle
ONE_CYCLE_ONLY  = os.getenv("ONE_CYCLE_ONLY", "False").lower() == "true" # Bool, if true only does one cycle
DRY_RUN         = os.getenv("DRY_RUN","False").lower() == "true"
DISABLE_API_CALLS       = os.getenv("DISABLE_API_CALLS","False").lower() == "true"
DISABLE_GOOGLE_API_CALLS= os.getenv("DISABLE_GOOGLE_API_CALLS","False").lower() == "true"
DISABLE_FTC_API_CALLS   = os.getenv("DISABLE_FTC_API_CALLS","False").lower() == "true"
AUTHORIZATION_HEADER    = {"authorization":"Basic "+os.getenv("PERSONAL_ACCESS_TOKEN", "<placeholder personal access token>")}

last_update = 0
last_update_display = "0000-00-00 00:00:00"
current_iteration = 1

logger.info("EDrewcated Guesser by Drew Wingfield")
logger.info("(c) 2025, Drew Wingfield")
logger.info(f"Running version {__version__}")
logger.info("Environment variables collected.")
logger.debug(f"CALCULATION_MODE is {CALCULATION_MODE}")


#endregion setup

#region functions

def print_status(message:str):
    logger.info("")
    logger.info( " @--------------------------------------@")
    logger.info( " @ EDrewcated Guesser by Drew Wingfield @")
    logger.info(f" @ v{__version__:16}                    @")
    logger.info( " @--------------------------------------@")
    logger.info(f" @ Iteration: {current_iteration:20}      @")
    logger.info(f" @ Last Update:    {last_update_display:20} @")
    logger.info(f" @ Current Time:   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):20} @")
    #logger.info(f" @ Status:  $status                   ")
    logger.info(f" @ EventCode:      {EVENT_CODE:20} @")
    logger.info( " @--------------------------------------@")
    logger.info(f" @ {message} ")
    logger.info( " @--------------------------------------@")



def count_down():
    for i in range(DELAY_SECONDS, 0, -1):
        logger.info(f"Counting down... {i}")
        time.sleep(1)


def save_response(response:requests.Response, path):
    """
    Saves a response json to a json file. path is relative. 
    If the filepath doesn't exist, it will be created. 
    """

    # Detect bad status code
    if response.status_code != requests.status_codes.codes.ok:
        logger.error(f"Got an invalid response code ({response.status_code}) while making an API request.")
        logger.error(f"save_response got a status code of {response.status_code} while attempting to save to {path}")
        logger.error(f"save_response Response headers (should contain error info): {response.headers}")
        raise Exception(f"save_response got a status code of {response.status_code}")
    
    # Detect bad response type
    if "Content-Type" not in response.headers or response.headers["Content-Type"].lower() != "application/json; charset=utf-8":
        logger.warning(f"save_response - response type is not 'application/json; charset=utf-8' - headers: {response.headers}")

    try:
        data = response.json()
    
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"save_response was unable to decode the json of a response (response status code {response.status_code}) (saving to path {path}).")
        logger.error(f"Headers of response: {response.headers}")
        raise e
    
    except Exception as e:
        logger.error(f"save_response was unable to get the json of a response (saving to path {path})")
        raise e
    
    with open(os.path.join(PROJECT_PATH,path),"w") as writer:
        json.dump(data, writer, indent=4)

def get_matches(year:str|int =SEASON_YEAR, code:str =EVENT_CODE):
    """ Gets the list of matches and teams for the event and puts it in the eventdata dir. """
    code = code.replace('/','_')

    # Get list of matches and teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{year}/matches/{code}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/{year}/eventdata/event_matches.json")
    # Get the event as a whole and put it into opr/all_events/EVENTCODE (needed for event-only OPR calculation)
    save_response(response, f"app/generatedfiles/{year}/opr/all_events/{code}.json")


    # Get the teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{year}/teams?EventCode={code}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/{year}/eventdata/event_teams.json")

def get_season_events_list(year:str|int =SEASON_YEAR):
    """ Gets the list of all events in the season and saves it to season_events.json """
    
    # Get list of matches and teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{year}/events",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/{year}/season_events.json")


def get_season_events_matches(year:str|int =SEASON_YEAR):
    """ 
    Pulls the season events list, filters out valid events, then 
    pulls the matches from FIRST API for each event into 
    generatedfiles/{year}/opr/all_events/{event_code}
    """
    logger.info(f"[get_season_events_matches] Getting all matches for all events in season {year}... (could take a minute or two)")
    logger.debug("[get_season_events_matches] Getting list of events for season and saving into season_events.json")

    # Get the list of all events in the season, saving to season_events.json
    get_season_events_list(year=year)

    # Filter the events and save into needed_event_ids.csv
    logger.debug("[get_season_events_matches] Filtering events and saving into needed_event_ids.csv")
    import json_parse
    season_events = json_parse.SeasonEvents(json_parse.get_json(os.path.join(PROJECT_PATH,"app","generatedfiles",str(SEASON_YEAR),"season_events.json")))
    all_season_event_ids = json_parse.filter_event_ids(season_events=season_events)

    logger.debug("[get_season_events_matches] Filtering done. Now iterating over every event and getting matches from FIRST API...")
    
    counter: int = 0
    tot = len(all_season_event_ids)
    for code in all_season_event_ids:
        counter += 1
        if DEBUG_LEVEL > 0: logger.debug(f"[get_season_events_matches] Event {counter:8}/{tot:8} - {code}") # For heavy debug use only
        # Get list of matches and teams for the event
        response = requests.get(
            url=f"https://ftc-api.firstinspires.org/v2.0/{year}/matches/{code}",
            headers=AUTHORIZATION_HEADER
        )
        # Get the event as a whole and put it into opr/all_events/EVENTCODE (needed for event-only OPR calculation)
        save_response(response, f"app/generatedfiles/{year}/opr/all_events/{code}.json")

    logger.info("[get_season_events_matches] This function is complete.")




def get_rankings():
    """ Gets the event rankings and saves them in eventdata. """
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/rankings/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/{SEASON_YEAR}/eventdata/event_rankings.json")
    


def get_schedule():
    """ Gets the event match schedule and saves it in eventdata. """
    # Quals
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/schedule/{EVENT_CODE}?tournamentLevel=qual",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/{SEASON_YEAR}/eventdata/eventschedule_qual.json")

    # Playoffs
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/schedule/{EVENT_CODE}?tournamentLevel=playoff",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/{SEASON_YEAR}/eventdata/eventschedule_playoff.json")



def cycle():
    global current_iteration
    global last_update
    global last_update_display

    time.sleep(0.1)

    if not(DISABLE_API_CALLS) and not(DISABLE_FTC_API_CALLS):
        logger.info("Getting FTC Event data 1/3 - Matches")
        if not DRY_RUN: get_matches()
        
        logger.info("Getting FTC event data 2/3 - Schedule")
        if not DRY_RUN: get_schedule()
        
        logger.info("Getting FTC event data 3/3 - Rankings")
        if not DRY_RUN: get_rankings()


        # GLOBAL or ALL modes, always retrieve and replace data
        if CALCULATION_MODE in ["GLOBAL","ALL"]:
            # Fetch and replace all events in season
            logger.debug(f"Fetching and replacing all events data in season {SEASON_YEAR}...")
            get_season_events_matches(year=SEASON_YEAR)
            logger.info("Season events matches retrieved.")
        
        # AUTO mode, retrieve event data that doesn't exist, and only replace events that are within 7 days (possibly ongoing events)
        if CALCULATION_MODE in ["AUTO", "AUTO_CONSERVATIVE"]:
            # Fetch
            #TODO: implement functionality of checking
            logger.warning("TODO: implement functionality")
            logger.debug(f"Fetching and replacing all events data in season {SEASON_YEAR}...")
            get_season_events_matches(year=SEASON_YEAR)
            logger.info("Season events matches retrieved.")

    else:
        logger.info("DISABLE_API_CALLS or DISABLE_FTC_API_CALLS is True. Skipped getting FIRST API data.")
    
    time.sleep(0.2)

    logger.info("Calculating OPRs... ")
    
    if DRY_RUN:
        logger.info("  (OPR calculation disabled because DRY_RUN is True)")

    else:
        logger.info("Setting up OPR calculation...")
        import OPR as opr_module
        
        logger.info("Performing OPR calculation...")
        opr_module.master_function()
        logger.info("OPR calculations commplete.")
        logger.info("Deleting unused OPR funtions")
        del opr_module
        logger.info("Unused OPR functions deleted.")

    if not(DISABLE_API_CALLS) and not(DISABLE_GOOGLE_API_CALLS):
        logger.info("Pushing team data to Google Sheets... ")

        if DRY_RUN:
            logger.info("Disabled because DRY_RUN is True")
        else:
            sheets_api.master_function(["teams"])

        logger.info("Pushing matches and rankings data to Google Sheets...")

        if DRY_RUN:
            logger.info("Disabled because DRY_RUN is True")
        else:
            sheets_api.master_function(["matches","rankings"])


    
    current_iteration += 1
    last_update = time.time()
    last_update_display = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


#endregion functions

#region procedural
# Display help
if "help" in [arg.lower().replace("-","") for arg in sys.argv]:
    logger.info(f"EDrewcated Guesser v{__version__}")
    logger.info(f" by Drew Wingfield")
    logger.info( "This project can be found at https://github.com/DrewWing/EDrewcatedGuesser")
    logger.info( "For more information, please consult the README.md page.")
    logger.info( "Syntax:")
    logger.info( "    python3 app/__main__.py")
    logger.info( "This script takes no arguments, and instead uses environment variables.")
    exit()

logger.info("Setup complete.")


# Warn user if the API data doesn't exist.
logger.debug("Checking for FIRST API data path existence...")
if os.path.exists(os.path.join(PROJECT_PATH,"app","generatedfiles",str(SEASON_YEAR),"eventdata","event_matches.json")):
    logger.debug("FIRST API data found!")

else:
    logger.critical("FIRST API data does not exist! Either FIRST API calls are disabled, or something went wrong with the FIRST API calls.")


# Get the list of season events if there's a possibility of using things
if CALCULATION_MODE in ["AUTO","AUTO_CONSERVATIVE","GLOBAL","ALL"] and not(DISABLE_API_CALLS) and not(DISABLE_FTC_API_CALLS):
    logger.info(f"Calculation mode is {CALCULATION_MODE} - getting season events list...")
    get_season_events_list()
    logger.info("Season events list retrieved.")

elif DISABLE_FTC_API_CALLS or DISABLE_API_CALLS:
    logger.warning(f"Calculation mode is set to {CALCULATION_MODE}, but API calls are disabled! Program will be unable to fetch global data!")

# Cycle
if ONE_CYCLE_ONLY:
    cycle()

else:
    while True:
        try:
            cycle()
            print_status("Waiting...")
            count_down()

        except KeyboardInterrupt:
            logger.warning("Breaking cycle due to keyboard interrupt.")
            break


logger.info("Program has completed.")
logger.debug("Flushing log buggers before exit.")
logging.shutdown() # Flush all log buffers before exiting.
#endregion procedural



