#!/bin/bash


# ftcapiv4.sh
# by Drew Wingfield
# started February 2024
# forked from ftcapiv3 on Feb 26th, 2024

# This program uses the official FIRST API for match info
# You can find more info on it here: https://frc-events.firstinspires.org/services/API


# printing with help from https://stackoverflow.com/questions/1898712/make-sure-int-variable-is-2-digits-long-else-add-0-in-front-to-make-it-2-digits

# activate the virtual environment where we installed the required packages (google sheets api stuff).
source /mnt/chromeos/removable/JimmyMovies_1/DrewFTCAPI/ftcapivenv/bin/activate #sklearn-venv/bin/activate



iteration=1
status="\033[0;32mOK\033[0m"
lastupdate="0000-00-00 00:00:00"
delayseconds=120
testmode=false
onecycle=false
updateTeams=true
dryRun=false

authorizationheader="Authorization: Basic THE_TOKEN_GOES_HERE_FIX_THIS" #TODO: Remove this before sharing!

pathtoftcapi=$(pwd)
eventcode="FTCCMP1FRAN" # FTCCMP1 !!! REMEMBER TO ALSO CHANGE IT IN COMMONRESOURCES.PY !!! - "USTXCMPTESL" for testing


printstatus () {
    printf '\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F'
    printf ' ┌────────────────────────────────────┐\n'
    printf ' │ FTC API V47.1  -  Drew Wingfield   │\n'
    printf ' ├────────────────────────────────────┤\n'
    printf " │ Iteration:\033[0;35m %03d                     \033[0m│\n" $iteration
    printf " │ Last Update:\033[0;34m  $lastupdate  \033[0m│\n"
    printf ' │ Current Time:\033[0;34m %(%Y-%m-%d %H:%M:%S)T  \033[0m│\n'
    printf " │ Status:  $status                        │\n"
    printf " │ EventCode:\033[0;35m $eventcode             \033[0m│\n"
    printf ' │                            ┌───────┘\n'
    printf '\n\n'
    
    printf "\033[F\033[F"
    printf   " ├────────────────────────────┤"
    printf "\n │ $1 "
    printf "\n"
    printf   " └────────────────────────────┘"
    printf '\n'
}



countdown () {
    for (( i = $delayseconds; i>=0; i-- ))
    
    do
        printstatus "Counting down...   $(printf "%02d" $i)      │"
        sleep 1
    done

    #printf '\n'

}


getmatches () {
    # Gets the list of matches and teams for the event and puts it in eventdata

    # Get the matches for the event
    curl -S -s -o "$pathtoftcapi/eventdata/eventmatches.json" -X GET "https://ftc-api.firstinspires.org/v2.0/2023/matches/$eventcode" -H  "accept: application/json" -H  "$authorizationheader"
    
    # Get the teams for the event
    curl -S -s -o "$pathtoftcapi/eventdata/eventteams.json" -X GET "https://ftc-api.firstinspires.org/v2.0/2023/teams?eventCode=$eventcode" -H  "accept: application/json" -H  "$authorizationheader"

    # Get the event as a whole and put it into opr/all-events/EVENTCODE (needed for event-only OPR calculation)
    curl -s -S -o "$pathtoftcapi/opr/all-events/$eventcode.json" -X GET "https://ftc-api.firstinspires.org/v2.0/2023/matches/$eventcode?" -H  "accept: application/json" -H  "$authorizationheader"
}


getscores () {
    # get the event scores
    # this is still a work in progress (unimplemented for now)
    curl -S -s -X GET "https://ftc-api.firstinspires.org/v2.0/2023/scores/$eventcode/qual" -H  "accept: application/json" -H  "$authorizationheader"
    
    curl -S -s -X GET "https://ftc-api.firstinspires.org/v2.0/2023/scores/$eventcode/playoff" -H  "accept: application/json" -H  "$authorizationheader"
}



getrankings () {
    # Gets the event rankings and saves it in eventdata
    curl -S -s -o "$pathtoftcapi/eventdata/eventrankings.json" -X GET "https://ftc-api.firstinspires.org/v2.0/2023/rankings/$eventcode" -H  "accept: application/json" -H "$authorizationheader"
}



#curl -X GET "https://ftc-api.firstinspires.org/v2.0/2023/matches/$eventcode?" -H  "accept: application/json" -H  "$authorizationheader"



getschedule () {
    # Gets the event match schedule and saves it in eventdata
    curl -S -s -o "$pathtoftcapi/eventdata/eventschedule-qual.json" -X GET "https://ftc-api.firstinspires.org/v2.0/2023/schedule/$eventcode?tournamentLevel=qual" -H  "accept: application/json" -H  "$authorizationheader"
    curl -S -s -o "$pathtoftcapi/eventdata/eventschedule-playoff.json" -X GET "https://ftc-api.firstinspires.org/v2.0/2023/schedule/$eventcode?tournamentLevel=playoff" -H  "accept: application/json" -H  "$authorizationheader"
}




cycle () {
    sleep 0.1
    printstatus "Getting FTC event data...  │"
    if [[ "$dryRun" = false ]] ; then
        getmatches
        printstatus "Getting FTC event data  2/3 │"
        getschedule
        printstatus "Getting FTC event data  3/3 │"
        getrankings
    
    fi
    
    sleep 0.5
    
    # If updating the team data, calculate and push the team OPR data
    if [[ "$updateTeams" = true ]] ; then
        # update teams here
        printstatus "Calculating OPRs...        │"
        python3 "$pathtoftcapi/OPRv4.py" quiet # NOTE: Needs to be done before pushing matches
        # Pushing matches includes calculating predictions, which relies on OPR and recentOPR stats
        printstatus "Pushing team data...       │"
        python3 "$pathtoftcapi/sheetsapi.py" teams quiet

    fi
    
    printstatus "Pushing match data...      │"

    if [[ "$dryRun" = false ]] ; then
    
    # Push the matches and rankings data to the google sheet
    python3 "$pathtoftcapi/sheetsapi.py" matches rankings quiet
    
    
    fi
    sleep 0.5
    printstatus "Done!                      │"

    # Add one to the iterations and reset the lastupdate timestamp
    iteration=$((iteration + 1))
    printf -v lastupdate "%(%Y-%m-%d %H:%M:%S)T"

    #sleep 1
    countdown
    
}



Help()
{
   # Display Help
   printf "ftcapiv4.sh\nby Drew Wingfield\n"
   printf "Make sure to see the documentation in the README.md file\n"
   printf "This program uses the official FIRST API for match info\nYou can find it here: https://frc-events.firstinspires.org/services/API\n\n"
   printf "Syntax: . ftcapifinal.sh [-e|h|o] \n"
   printf "options: \n"
   printf "  e [eventcode] Use a specific event code\n"
   #printf "g     Print the GPL license notification. \n"
   printf "  h     Print this Help. \n"
   printf "  T     Update the team stats. \n"
   printf "  o     Do only one cycle. \n"
   printf "  r     Get rankings data for event, then push rankings data to sheets. \n"
   printf "  d     Do a \"dry run,\" where nothing actually runs, just the visual output. \n"
   #printf "V     Print software version and exit. \n\n"
}





# Getting options was modified from https://stackoverflow.com/questions/7069682/how-to-get-arguments-with-flags-in-bash
#while getopts 'h' flag; do
while test $# -gt 0; do
  #case "${flag}" in
  case "$1" in
    h) Help
    return 0
    exit;;
    e) 
    shift
    eventcode=$1
    printf "  Using cusom event code $eventcode\n"
    ;;

    r) 
    printf "  Only getting and pushing rankings data."
    getrankings
    python3 "$pathtoftcapi/sheetsapi.py" rankings quiet
    return 0
    ;;
    
    t) 
    shift
    testmode=$1
    printf "  Testmode set to $testmode\n"
    ;;

    T) 
    shift
    updateTeams=true
    printf "  updateTeams set to true\n"
    ;;

    d) 
    shift
    dryRun=true
    printf "  dryRun set to true\n"
    ;;

    o) 
    shift
    onecycle=true
    printf "  Doing only one cycle\n"
    ;;
    #b) b_flag='true' ;;
    #f) files="${OPTARG}" ;;
    #v) verbose='true' ;;
    *) break ;;
  esac
done

#printf "eventcode: $eventcode\n"
#printf "one\n"
#return 1

printf ' REMEMBER TO CHECK THIS (should be latest version!!!):\n'
printf " pathtoftcapi = $pathtoftcapi"
printf '\n\n\n\n\n\n\n\n\n\n\n\n\n\n' # needs to be here to offset the "going up" of the cursor


if [[ "$onecycle" = true ]] ; then
    cycle
    
else
    while true ; do

        cycle
    done
fi



#deactivate the virtual environment
deactivate


printf "[ftcapiv4] Program complete!\n"