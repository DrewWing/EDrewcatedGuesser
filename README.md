# FTCAPI V47.1 (Alpha)
## by Drew Wingfield
This is the README file.

You can find the license [here](LICENSE.txt).
Also see the [Updates](Updates.md) page.

## Things to work on:

### Bugs
  - `[OPR]` `[Speed]` `[Urgent!!!]` Right Now global OPRs are calculated (because CRAPPY_LAPTOP is False) all the time, using up a rediculous amount of CPU time every time the matches change. Somehow fix that. (maybe only do it every time the event changes?)
  - `[Speed]` Maybe add GPU/NPU support?
  - `[OPR]` `[Accuracy]` `[fixed]` Fix bug where event opr is really wrong for whatever reason.
  - `[OPR]` `[Accuracy]` Weird bug with some teams' recent OPR calculated as 0 for lower amounts of days (30)
    - Probably due to the team not playing matches within the last 30 days - fix and just replace with their respective all-time OPRs insted (requires re-training of machine learning algorithms)

### Other
  - `[QOL]` Remove all unneccessary files
  - `[Accuracy]` Retrain the algorithms
  - `[Code QOL]` Making predictions work with both the EventMatches and EventSchedule classes (jsonparse)
    - and the implementation of the predictions in sheetsapi
    - and the processing of the data (getting recent OPRs, etc etc.)
  - `[Speed]` Convert more things to use numpy matrices instead of pandas dataframes (much faster)
    - prepare-machinelearningpy training_data_matches
  - `[QOL]` Adding a user interface?
  - `[Code QOL]` Make all files consistent with PEP 8 and PEP 257


## Running the Program
To run the program after setting up the correct variables (see below), run the `ftcapiv4.sh` program, which kind of calls everything else. If you want to do anything other than the basics, you're going to have to dig a little deeper into the code. Use the `h` modifier to get the help menu.

## Setting Up
Please note that this software needs to be set up correctly to work.

### Common Resources
Certain variables in commonresources.py need to be set up correctly;
 - `PATH_TO_FTCAPI` (string) is the absolute path to the parent folder of the program, including a trailing forwardslash. Ex: `/home/wingfield/ftcapi-branch44-1/`

 - `DO_JOBLIB_MEMORY` (boolean) describes whether or not certain functions are cached using the joblib library to speed up processing. <br> *Note that you may encounter UserWarnings about long processing times due to large inputs. It's your decision whether to enable or disable this setting.*

 - `PATH_TO_JOBLIB_CACHE` (string) is the absolute path to a folder where you want the joblib library to cache the functions. Only used if `DO_JOBLIB_MEMORY` is `True`. Ex: `/mnt/chromeos/removable/DrewsUSBDrive/DrewRAMExtension`

 - `EVENTCODE` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`

 - `SERVICE_ACCOUNT_FILE` (string) is the path to the .json file where your service account authentication key is stored.

 - `SPREADSHEET_ID` (string) is the ID of the google spreadsheet you want to push data to, found in the URL of the spreadsheet; https://docs.google.com/spreadsheets/d/spreadsheet_id_goes_here/edit. Ex: `1MoOvAGpCF_dbo-verZvakOPCE2XJQi5IMG24vWRL64o`


### The FTCAPI BASH Program
In ftcapiv4.sh there are several necessary variables to configure;
 - `authorizationheader` (string) should be set to your authorization token for the FTC API. Ex: `"Authorization: Basic <your_token_goes_here>"`

 - `pathtoftcapi` should be similarly configured as in commonresources.py, except **without the trailing forwardslash.** Ex: `/home/wingfield/ftcapi-branch44-1`

 - `eventcode` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`

## Files, their Purpose, and their Interactions
### FTCAPI BASH Shell Script (`ftcapiv4.sh`)
Documentation goes here!

### Commmon Resources (`commonresources.py`)
The place where most constants and commonly used functions are stored. Pretty much every other python file draws from this. \
Some examples are `red_x`, `green_check`, `PATH_TO_FTCAPI`, `PATH_TO_JOBLIB_CACHE`, and `get_json`.

### Json Parse (`jsonparse.py`)
Documentation goes here!

### Sheets API (`sheetsapi.py`)
Documentation goes here!

### OPR Event (`OPRv4-event.py`)
Documentation goes here!


### Archive (`Archive.zip`)
Never go here... It's filled with bugs, messy code, and things I removed for good reason. This exists mostly just as a backup in case I accidentally ***really*** mess up one of my files and need to pull from an older version.


## Machine Learning program.
First run `update-dataset-global.sh` to gather the data (uses `opr/all-events`).
Then run `prepare-machinelearning.py` to process the data (creates `machinefile.csv`).
To run, run the `ml-test.py` program (uses `machinefile.csv`) to actually train the algorithm.


## Credits/Honorable Mentions
This program uses the official FIRST API to get information on matches, schedules, and scores.
You can find it [here](https://frc-events.firstinspires.org/services/API).

Thanks to The [Blue Alliance](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/) for an overview of OPR.

Thanks to [this article](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/) for ideas on matrix calculation.

Printing in BASH with help from some people on [this StackOverflow post](https://stackoverflow.com/questions/1898712/make-sure-int-variable-is-2-digits-long-else-add-0-in-front-to-make-it-2-digits).

Python printing in colors (Colors class) was taken from [Rene-d](https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007).

## More documentation goes here!
As always, this is a work in progress and has some bugs. Errors should be both printed to the terminal and appended to `error.log` with a timestamp.

Good luck debugging!

<br><br>
All documentation and code is (c) 2024 Drew Wingfield unless otherwise mentioned. All rights reserved.
