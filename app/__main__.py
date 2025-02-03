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
import datetime
import time
import json

# Third-Party Imports
import requests
from dotenv import load_dotenv

# Local Imports
from common_resources import PATH_TO_FTCAPI, EVENT_CODE, SEASON_YEAR, log_error, green_check, red_x, info_i
from common_resources import DEBUG_LEVEL, __version__


#region setup
load_dotenv() # Load environment variables

DELAY_SECONDS   = int(os.getenv("DELAY_SECONDS", 120)) # Seconds between each cycle
ONE_CYCLE_ONLY  = os.getenv("ONE_CYCLE_ONLY", "False").lower() == "true" # Bool, if true only does one cycle
DRY_RUN         = os.getenv("DRY_RUN","False").lower() == "true"
DISABLE_API_CALLS       = os.getenv("DISABLE_API_CALLS","False").lower() == "true"
AUTHORIZATION_HEADER    = "Basic "+os.getenv("PERSONAL_ACCESS_TOKEN", "<placeholder personal access token>")

last_update = 0
last_update_display = "0000-00-00 00:00:00"
current_iteration = 1

if DEBUG_LEVEL>0:
    print(info_i()+"EDrewcated Guesser by Drew Wingfield")
    print(info_i()+"(c) 2025, Drew Wingfield")
    print(green_check()+"User parameters collected. ")


#endregion setup

#region functions

def print_status(message:str):
    print(info_i()+"")
    print(info_i()+ " @--------------------------------------@")
    print(info_i()+ " @ EDrewcated Guesser by Drew Wingfield @")
    print(info_i()+f" @ v{__version__:16}                    @")
    print(info_i()+ " @--------------------------------------@")
    print(info_i()+f" @ Iteration: {current_iteration:20}      @")
    print(info_i()+f" @ Last Update:    {last_update_display:20} @")
    print(info_i()+f" @ Current Time:   {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):20} @")
    #print(info_i()+f" @ Status:  $status                   ")
    print(info_i()+f" @ EventCode:      {EVENT_CODE:20} @")
    print(info_i()+ " @--------------------------------------@")
    print(info_i()+f" @ {message} ")
    print(info_i()+ " @--------------------------------------@")



def count_down():
    for i in range(DELAY_SECONDS, 0, -1):
        print(info_i()+f"Counting down... {i}")
        time.sleep(1)


def save_response(response:requests.Response, path):
    """ Saves a response json to a json file. path is relative. """
    data = response.json()
    
    with open(os.path.join(PATH_TO_FTCAPI,path),"w") as writer:
        json.dump(data, writer, indent=4)

def get_matches ():
    """ Gets the list of matches and teams for the event and puts it in the eventdata dir. """
    
    # Get list of matches and teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/matches/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    #TODO: Detect invalid data and bad status codes and such.
    save_response(response, "generatedfiles/eventdata/event_matches.json")


    # Get the teams for the event
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/teams?EventCode={EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    #TODO: Detect invalid data and bad status codes and such.
    save_response(response, "generatedfiles/eventdata/event_teams.json")


    # Get the event as a whole and put it into opr/all-events/EVENTCODE (needed for event-only OPR calculation)
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/matches/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    #TODO: Detect invalid data and bad status codes and such.
    save_response(response, f"generatedfiles/opr/all-events/{EVENT_CODE.replace('/','_')}.json")
    


def get_rankings():
    """ Gets the event rankings and saves them in eventdata. """
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/rankings/{EVENT_CODE}",
        headers=AUTHORIZATION_HEADER
    )

    #TODO: Detect invalid data and bad status codes and such.
    save_response(response, f"generatedfiles/eventdata/event_rankings.json")
    


def get_schedule():
    """ Gets the event match schedule and saves it in eventdata. """
    # Quals
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/schedule/{EVENT_CODE}?tournamentLevel=qual",
        headers=AUTHORIZATION_HEADER
    )

    #TODO: Detect invalid data and bad status codes and such.
    save_response(response, f"generatedfiles/eventdata/eventschedule_qual.json")

    # Playoffs
    response = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{SEASON_YEAR}/schedule/{EVENT_CODE}?tournamentLevel=playoff",
        headers=AUTHORIZATION_HEADER
    )

    #TODO: Detect invalid data and bad status codes and such.
    save_response(response, f"generatedfiles/eventdata/eventschedule_playoff.json")



def cycle():
    global current_iteration
    global last_update
    global last_update_display

    time.sleep(0.1)

    if not DISABLE_API_CALLS:
        print(info_i()+"Getting FTC Event data... (1/3) ")
        if not DRY_RUN: get_matches()
        
        print("Getting FTC event data 2/3 ")
        if not DRY_RUN: get_schedule()
        
        print("Getting FTC event data 3/3 ")
        if not DRY_RUN: get_rankings()

    else:
        print(info_i()+"DISABLE_API_CALLS is True. Skipped getting FIRST API data.")
    
    time.sleep(0.2)

    print(info_i()+"Calculating OPRs... ")
    
    if DRY_RUN:
        print(info_i()+"  (Disabled because DRY_RUN is True)")

    else:
        #TODO: Run OPR stuff here (basic OPR program)
        raise NotImplementedError("TODO")

        print(green_check()+"OPRs calculated.")

    if not DISABLE_API_CALLS:
        print(info_i()+"Pushing team data... ")

        if DRY_RUN:
            print(info_i()+"Disabled because DRY_RUN is True")
        
        else:
            #TODO Run sheets_api stuff here (teams argument)
            raise NotImplementedError("TODO")

    
    current_iteration += 1
    last_update = time.time()
    last_update_display = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



# function DisplayHelp {
#     # Display Help
#     Write-Output "FTCAPI v$Version"
#     Write-Output "by Drew Wingfield"
#     Write-Output "  - Make sure to see the documentation in the README.md file"
#     Write-Output "  - This program uses the official FIRST API for match info"
#     Write-Output "    You can find it here: https://ftc-events.firstinspires.org/services/API"
#     Write-Output ""
#     Write-Output "Syntax: "
#     Write-Output "  . ftcapifinal.sh -EventCode FTCCMP1FRAN"
#     Write-Output "Parameters: "
#     Write-Output "  EventCode [string] Use a specific event code"
#     Write-Output "  h     Print this Help."
#     Write-Output "  help  Print this Help."
#     #printf "  T     Update the team stats. \n"
#     Write-Output "  OneCycle      Do only one cycle of getting matches, calculating stats, and pushing data."
#     Write-Output "  RankingsOnly  Get rankings data for event, then push rankings data to sheets."
#     Write-Output "  DryRun        Do a dry run, where nothing actually runs, just the visual output (for debug/testing)."
#     Write-Output "  NoAPICalls    Disables calls to the FTC API (for debug)."
#     Write-Output "  DebugLevel <int>  Sets the debug_level for all python scripts. The info printed increases with the number."
#     Write-Output "  VenvDir <str>     Uses the given path (local or absolute) for the parent directory of the used Virutal Environment."
#     Write-Output "  SeasonYear <int>  First year of the season. For instance, the 2023-2024 school year is just '2023'"

    #printf "V     Print software version and exit. \n\n"


#endregion functions

#region procedural
# if (($help -eq $true) -or ($h -eq $true)) {
#     DisplayHelp
#     return 0
# }


# if ($rankingsonly -eq $true) {
#     Write-Output "  Only getting and pushing rankings data."
#     GetRankings
#     python "$pathtoftcapi/sheets_api.py" rankings
#     return 0
# }



if ONE_CYCLE_ONLY:
    cycle()

else:
    while True:
        try:
            cycle()
            print_status("Waiting...")
            count_down()

        except KeyboardInterrupt:
            print(red_x()+"Breaking cycle due to keyboard interrupt.")
            break


print(green_check()+"[__main__] Program has complete")
#endregion procedura



