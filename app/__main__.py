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
from common_resources import __version__
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
    """ Saves a response json to a json file. path is relative. """

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

def get_matches ():
    """ Gets the list of matches and teams for the event and puts it in the eventdata dir. """
    
    # Get list of matches and teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/matches/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, "app/generatedfiles/eventdata/event_matches.json")


    # Get the teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/teams?EventCode={EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, "app/generatedfiles/eventdata/event_teams.json")


    # Get the event as a whole and put it into opr/all_events/EVENTCODE (needed for event-only OPR calculation)
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/matches/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/opr/all_events/{EVENT_CODE.replace('/','_')}.json")
    


def get_rankings():
    """ Gets the event rankings and saves them in eventdata. """
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/rankings/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/eventdata/event_rankings.json")
    


def get_schedule():
    """ Gets the event match schedule and saves it in eventdata. """
    # Quals
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/schedule/{EVENT_CODE}?tournamentLevel=qual",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/eventdata/eventschedule_qual.json")

    # Playoffs
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/schedule/{EVENT_CODE}?tournamentLevel=playoff",
        headers=AUTHORIZATION_HEADER
    )

    save_response(response, f"app/generatedfiles/eventdata/eventschedule_playoff.json")



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



