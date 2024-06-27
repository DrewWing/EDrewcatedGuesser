
# ftcapiv4.ps1
# by Drew Wingfield
# forked from ftcapiv4 on June 6th, 2024
# because i guess i need to have windows support.

# This program uses the official FIRST API for match info
# You can find more info on it here: https://frc-events.firstinspires.org/services/API

# Making REST API requests in Powershell with help from
# https://www.reddit.com/r/PowerShell/comments/18dx1pp/intro_to_rest_api_with_powershell/

# If you are having trouble with the virtualenvironment or python scripts just not running,
# I suggest you check out https://stackoverflow.com/a/18713789


#region setup
param (
    [string]$EventCode = "FTCCMP1FRAN", # FTCCMP1 !!! REMEMBER TO ALSO CHANGE IT IN COMMONRESOURCES.PY !!! - "USTXCMPTESL" for testing
    [float]$Delayseconds = 120,
    [switch]$help = $false,
    [switch]$h = $false,
    [switch]$OneCycle = $false,
    [switch]$DryRun = $false,
    [switch]$rankingsonly = $false,
    [switch]$ShowDebugText = $false,
    [switch]$NoApiCalls = $false,
    [bool]$FieldMode = $true,
    [int]$DebugLevel = 0 # Debug level of python scripts
)

if ($ShowDebugText -eq $true){
    Write-Output "User parameters collected."
}

Set-Location "E:\DrewFTCAPI\ftcapi-branch47-1" #TODO: alwasys update this to the latest version

# Activate the virtual environment where we installed the required python packages (mostly google sheets api stuff).
. "E:\DrewFTCAPI\ftcapivenvwindows\scripts\activate.ps1" # NOTE: this is a windows-specific venv because of weird bugs in the other one.

python init_settings.py -EventCode "$EventCode" -DebugLevel "$DebugLevel" -FieldMode "$FieldMode"

if ($ShowDebugText -eq $true){
    Write-Output "Virtual Environment activated. Starting..."
}

$iteration=1
$status="OK"
$LastUpdate="0000-00-00 00:00:00"
$UpdateTeams=$true
$SeasonYear="2023" # First year of the season. For instance, the 2023-2024 school year is just "2023"


# gets the PersonalAccessToken
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
    Write-Output "FieldMode is $FieldMode"
}
#endregion setup

#region functions
function PrintStatus {
    param (
        [string]$message
    )

    #Write-Output '\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F'
    Write-Output "`n`n`n"
    Write-Output ' @------------------------------------@'
    Write-Output ' @ FTC API V47.1  -  Drew Wingfield   @'
    Write-Output ' @------------------------------------@'
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
    $response = Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "eventdata/eventmatches.json"
    #$response | ConvertTo-Json -Depth 4
    #echo "Response: "
    #echo "$response"
    #Invoke-WebRequest `
    #    "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode" `
    #    -InformationAction SilentlyContinue -WarningAction Continue `
    #    -OutFile "$pathtoftcapi/eventdata/eventmatches.json" `
    #    "-X" -Method Get `
    #    -Headers  "$AuthorizationHeader"
    #echo "First curl request complete!"
    # Get the teams for the event
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/teams?EventCode=$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "eventdata/eventteams.json"

    # Get the event as a whole and put it into opr/all-events/EVENTCODE (needed for event-only OPR calculation)
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/matches/$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "opr/all-events/$EventCode.json"
}


function GetRankings {
    # Gets the event rankings and saves it in eventdata
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/rankings/$EventCode" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "eventdata/eventrankings.json"
}


function GetSchedule {
    # Gets the event match schedule and saves it in eventdata
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/schedule/$($EventCode)?tournamentLevel=qual" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "eventdata/eventschedule-qual.json"
    
    Invoke-RestMethod -uri "https://ftc-api.firstinspires.org/v2.0/$SeasonYear/schedule/$($EventCode)?tournamentLevel=playoff" `
                    -Method Get -ContentType "application/json" `
                    -headers $AuthorizationHeader `
                    -OutFile "eventdata/eventschedule-playoff.json"
}


function cycle {
    Start-Sleep -Seconds 0.1

    if (($DryRun -eq $false) -and ($NoApiCalls -eq $false)) {
        PrintStatus "Getting FTC event data...  l"
        GetMatches
        PrintStatus "Getting FTC event data  2/3 l"
        GetSchedule
        PrintStatus "Getting FTC event data  3/3 l"
        GetRankings
    
    }
    
    Start-Sleep -Seconds 0.3
    
    # If updating the team data, calculate and push the team OPR data
    if (($UpdateTeams -eq $true) -and ($DryRun -eq $false)) {
        # update teams here
        PrintStatus "Calculating OPRs...        l"
        python "OPRv4.py" # NOTE: Needs to be done before pushing matches
        # Pushing matches includes calculating predictions, which relies on OPR and recentOPR stats
        PrintStatus "Pushing team data...       l"
        python "sheetsapi.py" teams

    }
    
    PrintStatus "Pushing match data...      l"

    if (($DryRun -eq $false) -and ($NoApiCalls -eq $false)){
        # Push the matches and rankings data to the google sheet
        python "sheetsapi.py" matches rankings
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
    Write-Output "ftcapiv4.sh"
    Write-Output "by Drew Wingfield"
    Write-Output "  - Make sure to see the documentation in the README.md file"
    Write-Output "  - This program uses the official FIRST API for match info"
    Write-Output "    You can find it here: https://frc-events.firstinspires.org/services/API"
    Write-Output ""
    Write-Output "Syntax: "
    Write-Output "  . ftcapifinal.sh -EventCode FTCCMP1FRAN"
    Write-Output "Parameters: "
    Write-Output "  EventCode [string] Use a specific event code"
    Write-Output "  h     Print this Help."
    Write-Output "  help  Print this Help."
    #printf "  T     Update the team stats. \n"
    Write-Output "  OneCycle      Do only one cycle."
    Write-Output "  RankingsOnly  Get rankings data for event, then push rankings data to sheets."
    Write-Output "  DryRun        Do a dry run, where nothing actually runs, just the visual output."
    Write-Output "  NoAPICalls    Disables calls to the FTC API. Usually good for debug."
    Write-Output "  DebugLevel <int>  Sets the debug_level for all python scripts."
    Write-Output "  FieldMode <bool>  Default true, uses last calculations for global OPR stats, instead of calculating it."

    #printf "V     Print software version and exit. \n\n"
}

#endregion functions


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
    python "$pathtoftcapi/sheetsapi.py" rankings
    return 0
}

#printf "EventCode: $EventCode\n"
#printf "one\n"
#return 1

#Write-Output " REMEMBER TO CHECK THIS (should be latest version!!!):"
#Write-Output " pathtoftcapi =" "$pathtoftcapi"
#Write-Output "\n\n\n\n\n\n\n\n\n\n\n\n\n\n" # needs to be here to offset the "going up" of the cursor


if ($OneCycle -eq $true){
    cycle

}
    
else {
    while ($true){
        cycle
    }
}



#deactivate the virtual environment
deactivate


Write-Output "[ftcapiv4] Program complete!"
