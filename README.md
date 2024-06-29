# FTCAPI V47.1 (Alpha)
## by Drew Wingfield
This is the README file.

DO NOT DISTRIBUTE!
You may **not** earn money from this program. It's not just my terms, it's the terms of using the official FTC API.

**NOTE** that this is an alpha version still in "stealth," so please ignore any references to licenses, in code or on any documentation. I'll get all that ironed out before I release this. \
Everything that I'm doing right now is unpublished, so you **may not** use it under any of these unpublished licenses. \
I'm doing my best, just use whatever version is most current under its own license and ignore this. It has many bugs and is not worth it.

You can find the license [here](LICENSE.txt).
Also see the [Updates](Updates.md) page.

## Things to work on:

### Bugs
  - [ ] `[Powershell]` `[FTC API]` `[REST]` All teams in opr/all-teams are invalid API request messagees, due to the team # being put in as the event code.
    - [ ] Figure out where in the world these files keep coming from! (unused)
  - [X] ~~`[OPR]` `[Speed]` `[Urgent!!!]` Right Now global OPRs are calculated (because CRAPPY_LAPTOP is False) all the time, using up a rediculous amount of CPU time every time the matches change. Somehow fix that. (maybe only do it every time the event changes?)~~
  - [ ] `[Speed]` Maybe add GPU/NPU support?
  - [X] ~~`[OPR]` `[Accuracy]` Fix bug where event opr is really wrong for whatever reason.~~
  - [ ] `[OPR]` `[Accuracy]` Weird bug with some teams' recent OPR calculated as 0 for lower amounts of days (30)
    - Probably due to the team not playing matches within the last 30 days - fix and just replace with their respective all-time OPRs insted (requires re-training of machine learning algorithms)

### Other
  - [ ] `[speed]` `[packages]` Maybe install CuPy?
  - [ ] `[QOL]` `[Code]` `[Arguments]` Make all python files use argparse
  - [ ] `[Sheets]` `[Readme]` Add instruction for how to use the Google Sheets
  - [ ] `[Sheets]` `[QOL]` It would be nice to add the team name to the number when pushing to sheets
  - [ ] `[NEEDED]` `[Readme]` Add instructions to creating secrets.txt to the readme (authorizationheader needs to be no spaces or quotes)
  - [ ] `[QOL]` `[Readme]` Redo the README.
  - [ ] `[QOL]` Remove all unneccessary files
    - [X] ~~Figure out where in the world OPR-m.npy comes from~~
    - [X] ~~Figure out if anything in the world uses OPR-m.npy~~
    - [ ] All opr/teamstats stuff
    - [ ] All references to opr/teamstats stuff
  - [X] ~~`[Accuracy]` Retrain the algorithms~~
  - [ ] `[Code QOL]` Making predictions work with both the EventMatches and EventSchedule classes (jsonparse)
    - and the implementation of the predictions in sheetsapi
    - and the processing of the data (getting recent OPRs, etc etc.)
  - [ ] `[Speed]` Convert more things to use numpy matrices instead of pandas dataframes (much faster)
    - prepare-machinelearningpy training_data_matches
  - [ ] `[QOL]` Adding a user interface?
  - [ ] `[Code QOL]` Make all python files consistent with PEP 8 and PEP 257


## Running the Program
### Windows
Most of the time, you should be running the program `ftcapiv4.ps1`. \
It is reccomended to use the `-h` argument to get familiar with the arguments.


#### During Events
During events, there are two really important parameters:
   - `FieldMode`, a boolean which should be set to `True` during an event. See the below section for more info on what it does.
   - `EventCode`, an alphanumeric code that FTC uses to keep track of their events. It is usually found in the URL of the ftc-events or ftc-scout website.

Your typical configuration during an event with an event code of `FTCCMPFRAN1` is going to look something like this:
```powershell
. 'your_path_to_the_directory\ftcapiv4.ps1' -FieldMode $True -EventCode "FTCCMPFRAN1"
```

#### Between Events
Between events, it's a good idea to rerun the program at least once with `FieldMode` set to `False`. This will enable updating the *global calculations* (more CPU taxing), which will be saved and used during the next event. It is reccomended to do this soon before the event (the `EventCode` doesn't matter for global statistics) to get the most up-to-date statistics on the teams.

You can also add the flag `-OneCycle` to only perform one cycle and then terminate.

A configuration between events might look something like this:
```powershell
. 'your_path_to_the_directory\ftcapiv4.ps1' -OneCycle -Fieldmode $False
```

### Linux
To run the program after setting up the correct variables (see below), run the `ftcapiv4.sh` program, which kind of calls everything else. If you want to do anything other than the basics, you're going to have to dig a little deeper into the code. Use the `h` modifier to get the help menu.

### MacOS
Good luck haha. I've had enough trouble adding support for both Linux and Windows, so there's no way I'm going to spend another 2,000 hours attempting to add MacOS support.

## Setting Up
Please note that this software needs to be set up correctly to work. This should be configured automatically by `ftcapiv4.ps1` or `ftcapiv4.sh`.

### Common Resources
Certain variables in commonresources.py need to be set up correctly;
 - `EVENTCODE` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`

 - `SERVICE_ACCOUNT_FILE` (string) is the path to the .json file where your service account authentication key is stored.

 - `SPREADSHEET_ID` (string) is the ID of the google spreadsheet you want to push data to, found in the URL of the spreadsheet; https://docs.google.com/spreadsheets/d/spreadsheet_id_goes_here/edit. Ex: `1MoOvAGpCF_dbo-verZvakOPCE2XJQi5IMG24vWRL64o`


### The FTCAPI BASH Program
In ftcapiv4.sh there are several necessary variables to configure;
 - `authorizationheader` (string) should be set to your authorization token for the FTC API. Ex: `"Authorization: Basic <your_token_goes_here>"`

 - `pathtoftcapi` should be similarly configured as in commonresources.py, except **without the trailing forwardslash.** Ex: `/home/wingfield/ftcapi-branch44-1`

 - `eventcode` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`

## Files, their Purpose, and their Interactions
### Commmon Resources (`commonresources.py`)
The place where most constants and commonly used functions are stored. Pretty much every other python file draws from this. \
Some examples are `red_x`, `green_check`, `PATH_TO_FTCAPI`, `PATH_TO_JOBLIB_CACHE`, and `get_json`.

### Json Parse (`jsonparse.py`)
Documentation goes here!

### Sheets API (`sheetsapi.py`)
Documentation goes here!

### OPR Event (`OPRv4.py`)
Documentation goes here!


## Machine Learning program.
The machine learning algorithm is just fine on its own, and you should not retrain it unless you know what you are doing. \
If you *are* retraining the algorithm, follow these steps.
1. Run `update-dataset-global.sh` to gather the data (uses `opr/all-events`).
2. Run `prepare-machinelearning.py` to process the data (creates `machinefile.csv`).
3. Actually train the algorithm by running the `ml-test.py` program (uses `machinefile.csv`).


## Credits/Honorable Mentions
This program uses the official FIRST API to get information on matches, schedules, and scores.
You can find it [here](https://frc-events.firstinspires.org/services/API).

Thanks to The [Blue Alliance](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/) for an overview of OPR.

Thanks to [this article](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/) for ideas on matrix calculation.

Printing in BASH with help from some people on [this StackOverflow post](https://stackoverflow.com/questions/1898712/make-sure-int-variable-is-2-digits-long-else-add-0-in-front-to-make-it-2-digits).

Python printing in colors (Colors class) was taken from [Rene-d](https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007).

Google sheets api was implemented with lots of help from [their sample program](https://github.com/googleapis/google-api-python-client/blob/main/samples/service_account/tasks.py) and [quickstart](https://developers.google.com/sheets/api/quickstart/python).

## More documentation goes here!
As always, this is a work in progress and has some bugs. Errors should be both printed to the terminal and appended to `error.log` with a timestamp.

Good luck debugging!

<br><br>
All documentation and code is (c) 2024 Drew Wingfield unless otherwise mentioned. All rights reserved.
