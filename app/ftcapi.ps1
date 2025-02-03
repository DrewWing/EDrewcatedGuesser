<#
.SYNOPSIS
    Gets match data from the FTC API, calculates statistics, and pushes data and predictions to the Google Sheets spreadsheet.

.DESCRIPTION
    Activates the Virtual Environment, gets content from the secrets.txt file.
    Uses the FIRST Tech Challenge API to get a match schedule, match results, and rankings data for a certain event.
    Then calls the python scripts to calculate the statistics. After that, it calls the python scripts to predict the match
    outcomes and push the data to the Google Sheets spreadsheet.
    Finally deactivates the Virtual Environment
    
    Forked from ftcapiv4.sh on June 6th, 2024

    AUTHOR: Drew Wingfield
    VERSION: 49.0
    COPYRIGHT: 
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


.PARAMETER DelaySeconds
    The amount of seconds, as an integer, spent waiting between each cycle.
    Defaults to 120

.PARAMETER OneCycle
    If true, do only one cycle of getting matches, calculating stats, and pushing data.
    Defaults to false

.PARAMETER DryRun
    If true, do a dry run, where no scripts or API calls actually run, just the visual output. This is mainly a parameter for debug/development.
    Defaults to false

.PARAMETER rankingsonly
    Get rankings data for event, then push rankings data to sheets. TODO: Revisit this parameter.
    Defaults to false

.PARAMETER ShowDebugText
    Shows debug text relating to this script.
    Defaults to false

.PARAMETER NoAPICalls
    If true, disables calls to the FTC API. This is mainly a parameter for debug use.
    Defaults to false

.PARAMETER VenvDir
    Uses the given path (local or absolute, as a string) for the Virutal Environment to use.
    Defaults to ".venv"

.EXAMPLE
    . ftcapi.ps1 -OneCycle

.EXAMPLE
    . ftcapi.ps1 -DelaySeconds 300 -VenvDir "C:\path_to_my_virtual_environment"


.NOTES
    This program uses the official FIRST Tech Challenge API for match info
    You can find it here: https://ftc-events.firstinspires.org/services/API

    Making REST API requests in Powershell with help from
    https://www.reddit.com/r/PowerShell/comments/18dx1pp/intro_to_rest_api_with_powershell/

    If you are having trouble with the virtualenvironment or python scripts just not running,
    I suggest you check out https://stackoverflow.com/a/18713789

#>


#region setup
param (
    [float]$Delayseconds = 120,
    [switch]$help = $false,
    [switch]$h = $false,
    [switch]$OneCycle = $false,
    [switch]$DryRun = $false,
    [switch]$rankingsonly = $false,
    [switch]$ShowDebugText = $false,
    [switch]$NoApiCalls = $false,
    [string]$VenvDir = ".venv" # The directory of virtual environment to use
)

$version="49.0 Alpha"

$currentLocation=Get-Location # The current location, should be the working directory

if ($DryRun -eq $true) {
    Write-Output "DryRun is true."
}

if ($ShowDebugText -eq $true) {
    Write-Output "User parameters collected."
    Write-Output "Current location $currentLocation"
    Write-Output "Now initializing correct directories"
}

python ".\__init__.py" # Creates required directories

if ($ShowDebugText -eq $true) {
    Write-Output "Directories initialized. Now activating virtual environment."
}


# Activate the virtual environment where we installed the required python packages (mostly google sheets api stuff).
. "$VenvDir\scripts\activate.ps1" # NOTE: this is a windows-specific venv because of weird bugs in the other one.

if ($ShowDebugText -eq $true) {
    Write-Output "Virtual Environment activated. Starting..."
}

$iteration=1
$status="OK"
$LastUpdate="0000-00-00 00:00:00"
$UpdateTeams=$true


# gets the PersonalAccessToken from secrets.txt
Get-Content secrets.txt | Foreach-Object{
    $var = $_.Split('=')
    Remove-Variable -Name $var[0]
    New-Variable -Name $var[0] -Value $var[1]
 }

# API Authorization - This token is the one you recieve from the official FTC website when setting up API access.
#$token = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f $user, $PersonalAccessToken)))
$AuthorizationHeader = @{authorization = "Basic $PersonalAccessToken"}


if (($ShowDebugText -eq $true) -or ($true -eq $true)){
    Write-Output "Initial variables set."
    Write-Output "PersonalAccessToken is $PersonalAccessToken"
}
#endregion setup

#region functions
function PrintStatus {
    param (
        [string]$message
    )

    #Write-Output '\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F'
    Write-Output "`n`n`n"
    Write-Output " @------------------------------------@"
    Write-Output " @ FTC API v$global:version  -  Drew Wingfield   @"
    Write-Output " @------------------------------------@"
    Write-Output " @ Iteration: $iteration   "
    Write-Output " @ Last Update:  $global:LastUpdate "
    Write-Output " @ Current Time: $((Get-Date).ToString())"
    Write-Output " @ Status:  $status                       "
    Write-Output " @ EventCode: $EventCode  "
    Write-Output " @ "
    #Write-Output ''
    
    #Write-Output "\033[F\033[F"
    Write-Output   " @----------------------------@"
    Write-Output " @ $message "
    Write-Output   " @----------------------------@"
}


function countdown {
    for ($i = $Delayseconds; $i -ge 0; $i--) {
        PrintStatus "Counting down...   $i     l"
        Start-Sleep -Seconds 1
        }
}


function GetMatches {
    # Gets the list of matches and teams for the event and puts it in eventdata

    #echo "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode"
    # Get all event matches
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "app/generatedfiles/eventdata/event_matches.json"
    #$response | ConvertTo-Json -Depth 4
    #echo "Response: "
    #echo "$response"
    #Invoke-WebRequest `
    #    "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode" `
    #    -InformationAction SilentlyContinue -WarningAction Continue `
    #    -OutFile "$pathtoftcapi/eventdata/event_matches.json" `
    #    "-X" -Method Get `
    #    -Headers  "$AuthorizationHeader"
    #echo "First curl request complete!"
    # Get the teams for the event
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/teams?EventCode=$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "app/generatedfiles/eventdata/event_teams.json"

    # Get the event as a whole and put it into opr/all-events/EVENTCODE (needed for event-only OPR calculation)
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "app/generatedfiles/opr/all-events/$EventCode.json"
}


function GetRankings {
    # Gets the event rankings and saves it in eventdata
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/rankings/$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "app/generatedfiles/eventdata/event_rankings.json"
}


function GetSchedule {
    # Gets the event match schedule and saves it in eventdata
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/schedule/$($EventCode)?tournamentLevel=qual" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "app/generatedfiles/eventdata/eventschedule_qual.json"
    
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/schedule/$($EventCode)?tournamentLevel=playoff" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "app/generatedfiles/eventdata/eventschedule_playoff.json"
}


function cycle {
    Start-Sleep -Seconds 0.1

    if (($DryRun -eq $false) -and ($NoApiCalls -eq $false)) {
        PrintStatus "Getting FTC event data...  l"
        GetMatches
        PrintStatus "Getting FTC event data 2/3 l"
        GetSchedule
        PrintStatus "Getting FTC event data 3/3 l"
        GetRankings
    
    }
    
    Start-Sleep -Seconds 0.3
    
    # If updating the team data, calculate and push the team OPR data
    if (($UpdateTeams -eq $true) -and ($DryRun -eq $false)) {
        # update teams here
        PrintStatus "Calculating OPRs...        l"
        python "app/OPR.py" # NOTE: Needs to be done before pushing matches
        # Pushing matches includes calculating predictions, which relies on OPR and recentOPR stats
        PrintStatus "Pushing team data...       l"
        python "app/sheetsapi.py" teams

    }
    
    PrintStatus "Pushing match data...      l"

    if (($DryRun -eq $false) -and ($NoApiCalls -eq $false)){
        # Push the matches and rankings data to the google sheet
        python "app/sheetsapi.py" matches rankings
    }

    Start-Sleep -Seconds 0.5
    PrintStatus "Done!                      l"

    # Add one to the iterations and reset the LastUpdate timestamp
    $iteration++
    $global:LastUpdate="$((Get-Date).ToString())"

    #sleep 1
    if ($OneCycle -eq $false) {
        countdown
    }
    
}


function DisplayHelp {
    # Display Help
    Write-Output "FTCAPI v$Version"
    Write-Output "by Drew Wingfield"
    Write-Output "  - Make sure to see the documentation in the README.md file"
    Write-Output "  - This program uses the official FIRST API for match info"
    Write-Output "    You can find it here: https://ftc-events.firstinspires.org/services/API"
    Write-Output ""
    Write-Output "Syntax: "
    Write-Output "  . ftcapifinal.sh -EventCode FTCCMP1FRAN"
    Write-Output "Parameters: "
    Write-Output "  EventCode [string] Use a specific event code"
    Write-Output "  h     Print this Help."
    Write-Output "  help  Print this Help."
    #printf "  T     Update the team stats. \n"
    Write-Output "  OneCycle      Do only one cycle of getting matches, calculating stats, and pushing data."
    Write-Output "  RankingsOnly  Get rankings data for event, then push rankings data to sheets."
    Write-Output "  DryRun        Do a dry run, where nothing actually runs, just the visual output (for debug/testing)."
    Write-Output "  NoAPICalls    Disables calls to the FTC API (for debug)."
    Write-Output "  DebugLevel <int>  Sets the debug_level for all python scripts. The info printed increases with the number."
    Write-Output "  VenvDir <str>     Uses the given path (local or absolute) for the parent directory of the used Virutal Environment."
    Write-Output "  SeasonYear <int>  First year of the season. For instance, the 2023-2024 school year is just '2023'"

    #printf "V     Print software version and exit. \n\n"
}

#endregion functions

#region procedural
if ($ShowDebugText -eq $true){
    Write-Output "User parameters collected."
}

if (($help -eq $true) -or ($h -eq $true)) {
    DisplayHelp
    return 0
}



if ($rankingsonly -eq $true) {
    Write-Output "  Only getting and pushing rankings data."
    GetRankings
    python "$pathtoftcapi/sheets_api.py" rankings
    return 0
}


if ($OneCycle -eq $true){
    cycle
} else {
    while ($true){
        cycle
    }
}



# Deactivate the virtual environment
deactivate


Write-Output "[ftcapi] Program complete!"
#endregion procedural
