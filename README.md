# FTCAPI V48.0 (Alpha)
## by Drew Wingfield
This is the README file.

DO NOT DISTRIBUTE!
You may **not** earn money or monetize in any way from this program. It's not just my terms, it's also a part of the terms of using the official FTC API.

**NOTE** that this is an alpha version still in "stealth," so please ignore any references to licenses, in code or on any documentation, except this paragraph. I'll get all that ironed out before I release this.  \
Everything that I'm doing right now is unpublished, so you **may not** use it under any of these unpublished licenses. \
I'm doing my best, just use whatever version is most current under its own license. It has many bugs and is not worth it.

You can find the license [here](LICENSE.txt).
Also see the [Updates](Updates.md) page.

## Things to work on:

### Bugs
  - [ ] `[Powershell]` `[FTC API]` `[REST]` All teams in opr/all-teams are invalid API request messagees, due to the team # being put in as the event code.
    - [ ] Figure out where in the world these files keep coming from! (unused)
  - [ ] `[Speed]` Maybe add GPU/NPU support?
  - [ ] `[OPR]` `[Accuracy]` Weird bug with some teams' recent OPR calculated as 0 for lower amounts of days (30)
    - Probably due to the team not playing matches within the last 30 days - fix and just replace with their respective all-time OPRs insted (requires re-training of machine learning algorithms)

### Other
  - [ ] `[Files]` Rename ml-test.py to something else more descriptive (and excluding the - symbol)
  - [ ] `[General]` Get a better Todo system (usse a bug-tracking system?)
  - [ ] `[OS Support]` `[Critical]` Linux support
    - [ ] Fix Linux bash file
    - [ ] Make sure everything works on linux lol
  - [ ] `[License]` `[Critical]` Update all files to include a reference to the license and this file
    - [ ] Scripts in `app` folder
    - [ ] `tests` folder
    - [ ] `__init__.py`
  - [ ] `[Files]` Remove these files before release (dev tools or generally not needed)
    - [ ] all packages.txt
    - [ ] flushGeneratedFiles.ps1
    - [ ] linecounter.py
    - [ ] viewdata.py?
  - [ ] `[Files]` Put all doc files (readme and updates) into a docs folder?
  - [ ] `[Code]` `[QOL]` Redo all the path things to make them better lol
  - [ ] `[Code]` `[Tests]` Add tests
    - [X] ~~Correct files in correct places~~
    - [ ] Machine learning is recent to the correct season  year
  - [X] ~~`[QOL]` `[variables]` In ftcapiv4.ps1, make the season year an input variable~~ (or automatic?)
  - [X] ~~`[QOL]` `[Files]` Organize generated files into a single folder and update the .gitignore~~
    - [ ] `[Readme]` Update Readme file instructions, file names, and directory names to match current ones.
  - [X] ~~Remove all references to heatmap stuff.~~
  - [ ] `[speed]` `[packages]` Maybe install CuPy?
  - [ ] `[QOL]` `[Code]` `[Arguments]` Make all python files use argparse
  - [ ] `[Sheets]` `[Readme]` Add instruction for how to use the Google Sheets
  - [ ] `[Sheets]` `[QOL]` It would be nice to add the team name to the number when pushing to sheets
  - [ ] `[NEEDED]` `[Readme]` Add instructions to creating secrets.txt to the readme (authorizationheader needs to be no spaces or quotes)
  - [ ] `[QOL]` `[Readme]` Redo the README.
  - [ ] `[QOL]` Remove all unneccessary files
    - [ ] Figure out what to do with viewdata.py
    - [X] ~~Figure out where in the world OPR-m.npy comes from~~
    - [X] ~~Figure out if anything in the world uses OPR-m.npy~~
    - [ ] All opr/teamstats stuff
    - [ ] All references to opr/teamstats stuff
  - [ ] `[Code QOL]` Making predictions work with both the EventMatches and EventSchedule classes (jsonparse)
    - and the implementation of the predictions in sheetsapi
    - and the processing of the data (getting recent OPRs, etc etc.)
  - [ ] `[Speed]` Convert more things to use numpy matrices instead of pandas dataframes (much faster)
    - prepare-machinelearningpy training_data_matches
  - [ ] `[QOL]` Adding a user interface?
  - [ ] `[Code QOL]` Make all python files consistent with PEP 8 and PEP 257


## Running the Program
### Windows
Most of the time, you should be running the program `ftcapi.ps1`. \
It is reccomended to use the `-h` argument to get familiar with the arguments.


#### During Events
During events, there are two really important parameters:
   - `FieldMode`, a boolean which should be set to `True` during an event. See the below section for more info on what it does.
   - `EventCode`, an alphanumeric code that FTC uses to keep track of their events. It is usually found in the URL of the ftc-events or ftc-scout website.

Your typical configuration during an event with an event code of `FTCCMPFRAN1` is going to look something like this:
```powershell
. 'your_path_to_the_directory\ftcapi.ps1' -FieldMode $True -EventCode "FTCCMPFRAN1"
```

#### Between Events
Between events, it's a good idea to rerun the program at least once with `FieldMode` set to `False`. This will enable updating the *global calculations* (more CPU taxing), which will be saved and used during the next event. It is reccomended to do this soon before the event (the `EventCode` doesn't matter for global statistics) to get the most up-to-date statistics on the teams.

You can also add the flag `-OneCycle` to only perform one cycle and then terminate.

A configuration between events might look something like this:
```powershell
. 'your_path_to_the_directory\ftcapi.ps1' -OneCycle -Fieldmode $False
```

### Linux
**The current version of this program is broken, don't use it right now. It will be fixed... hopefully... sometime later...**
To run the program after setting up the correct variables (see below), run the `ftcapi.sh` program, which kind of calls everything else. If you want to do anything other than the basics, you're going to have to dig a little deeper into the code. Use the `h` modifier to get the help menu.

### MacOS
Good luck haha. I've had enough trouble adding support for both Linux and Windows, so there's no way I'm going to spend another 2,000 hours attempting to add MacOS support.

## Setting Up
Please note that this software needs to be set up correctly to work. This should be configured automatically by `ftcapi.ps1` or `ftcapi.sh`.

### Common Resources
Certain variables in commonresources.py need to be set up correctly;
 - `EVENTCODE` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`

 - `SERVICE_ACCOUNT_FILE` (string) is the path to the .json file where your service account authentication key is stored.

 - `SPREADSHEET_ID` (string) is the ID of the google spreadsheet you want to push data to, found in the URL of the spreadsheet; https://docs.google.com/spreadsheets/d/spreadsheet_id_goes_here/edit. Ex: `1MoOvAGpCF_dbo-verZvakOPCE2XJQi5IMG24vWRL64o`


### The FTCAPI BASH Program
In ftcapi.sh there are several necessary variables to configure;
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
Though I wrote almost the entirety of the project by myself, I had some help. Below are some resources that I used (whether for copypasting code, general reference, or other research).

This program uses the official FIRST API to get information on matches, schedules, and scores.
You can find it [here](https://frc-events.firstinspires.org/services/API).

Thanks to [The Blue Alliance](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/) for an overview of OPR and the math behind it.

Thanks to [this article](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/) for ideas on matrix calculation.

Printing in BASH with help from some people on [this StackOverflow post](https://stackoverflow.com/questions/1898712/make-sure-int-variable-is-2-digits-long-else-add-0-in-front-to-make-it-2-digits).

Python printing in colors (the `Colors` class in `commonresources.py`) was taken from [Rene-d](https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007).

The Google Sheets API was implemented with lots of help from [their sample program](https://github.com/googleapis/google-api-python-client/blob/main/samples/service_account/tasks.py) and [quickstart](https://developers.google.com/sheets/api/quickstart/python).

Thanks to viniciusarrud on GitHub in [this Joblib issue](https://github.com/joblib/joblib/issues/1496#issuecomment-1788968714) for a solution to a particular bug involving pathing on Windows.

The diagram `FTCAPI file diagram.drawio` (soon to be exported into an image and put in this doc) was generated using [Drawio](https://app.diagrams.net/) [24.7.7], made by JGraph, https://github.com/jgraph/drawio. \
I am not JGraph, this project is not by JGraph, and JGraph neither endorses me nor this project.

### External libraries

This software uses the following external libraries:

 - Google API Python Client Framework: Copyright Google APIs. Licensed under Apache 2.0 license, see LICENSES.apache for details. \
Website: https://github.com/googleapis/google-api-python-client?tab=readme-ov-file

 - Matplotlib Framework: Copyright (c)
2012- Matplotlib Development Team; All Rights Reserved. Licensed similar to the PSF license, see LICENSES.matplotlib for details. \
Website: https://matplotlib.org/stable/

 - Pandas Framework: Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team. Licensed under a BSD 3-Clause license, see LICENSES.pandas for details. \
Website: https://github.com/pandas-dev/pandas?tab=readme-ov-file




## More documentation goes here!
As always, this is a work in progress and has some bugs. Errors should be both printed to the terminal and appended to `app/generatedfiles/error.log` with a timestamp.

Good luck debugging!

<br><br>
All documentation and code is Copyright (c) 2024 Drew Wingfield unless otherwise mentioned. All rights reserved.
