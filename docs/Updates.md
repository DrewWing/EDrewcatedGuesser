# Updates

Remember to check out the [README](README.md) file.

<!-- Copyright (C) 2024, Drew Wingfield

This document is part of EDrewcated Guesser by Drew Wingfield, found at https://github.com/DrewWing/EDrewcatedGuesser.
EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
the terms of the AGNU Affero General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the AGNU Affero General Public License for more details.

You should have received a copy of the AGNU Affero General Public License along with 
EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.

See the documentation in the README.md file. -->

## v50.0
June 30th, 2025.
#### Overview
First post-release update. Added and fixed lots of documentation, made configuration a *lot* easier, added much better logging, and created a more efficient statistics calculation system.

#### Known Bugs:
  - [#49](https://github.com/DrewWing/EDrewcatedGuesser/issues/49) In statistics ranking, Google Sheets template spreadsheet "ties" between two teams cuases it to show neither.
  - [#1](https://github.com/DrewWing/EDrewcatedGuesser/issues/1) "Recent OPR" calculations sometimes show up as 0 due to the way that statistic is calculated.


#### Bugs Fixed
  - [#2](https://github.com/DrewWing/EDrewcatedGuesser/issues/2) Tests failed due to argparse usage.
  - [#30](https://github.com/DrewWing/EDrewcatedGuesser/issues/30) Global data from two or more seasons interacted with one another, causing incorrect season statistics.
  - [2babbce](https://github.com/DrewWing/EDrewcatedGuesser/pull/34/commits/2babbceed24b52db140b0e30941586a95ecc4d8f) A FIRST API authentication bug.
  - [2737b9f](https://github.com/DrewWing/EDrewcatedGuesser/pull/34/commits/2737b9f58bcd7ab9a7e48c04ae1ba60281cfa3ec) A tests file filter bug.


#### Key changes
  - [#5](https://github.com/DrewWing/EDrewcatedGuesser/issues/5) Added configuration using environment variables!
    - Completely redid the flow of operation.
      - Added `app/__main__.py` as the main function (replaces BASH/PowerShell files)
    - Added `.env.template`
    - Removed old configuration (`app/init_settings.py`, `app/python_settings.py`).
  - [#20](https://github.com/DrewWing/EDrewcatedGuesser/issues/20) Scrapped the old manual logging system and replaced it with Python's builtin `logging` module.
    - Removed functions `log_error`, `green_check`, `info_i`, and `red_x`.
    - Added `create_logger`.
    - Added clearer debug logging levels (configurable).
    - Added `debug.log` log file.
    - Added logging tests.
    - `line_counter.py` now treats logging output lines as output lines.
  - [#23](https://github.com/DrewWing/EDrewcatedGuesser/issues/23) and [#33](https://github.com/DrewWing/EDrewcatedGuesser/issues/33) Renamed `PATH_TO_FTCAPI` to `PROJECT_PATH` and added automatic detection (`PROJECT_PATH` is no longer a required configuration variable).
    - Paths are now more resilient and can support both backslashes and forwardslashes (now using `os.path`).
    - Added function to automatically create required directories, solving many `FilepathNotFoundError`.
  - [#9](https://github.com/DrewWing/EDrewcatedGuesser/issues/9) Added option to disable Google Sheets api interaction.
  - [#29](https://github.com/DrewWing/EDrewcatedGuesser/issues/29) Reworked statistics calculation (what calculations happen when).
    - Added `CALCULATION_MODE` configuration variable.
    - Added a time counter since last global calculation
    - Added [documentation](StatsCalculation.md).
    - Reworked various functions in json_parse, specifically:
      -  prepare_opr_calculation, and
      -  SeasonEvents.filter.
   -  Separated caching heavy functions into its own function in opr.
  - [#39](https://github.com/DrewWing/EDrewcatedGuesser/issues/39) Main program now warns the user when API data doesn't exist.
  - Made [the GitHub Project](https://github.com/users/DrewWing/projects/1) management easier.
  - [#3](https://github.com/DrewWing/EDrewcatedGuesser/issues/3) Added Google Sheets spreadsheet version validation (user is warned if version is too old).
  - Updated the .gitignore (rearranged, added [Scalene](https://github.com/plasma-umass/scalene) profile output files)
  - Cleaned up a lot of comments.
  - Removed old code.

#### Docs
  - Documentation was updated to be more clear and useful.
  - Split Google Sheets setup into its own page.
  - Added [statistics calculation information page](StatsCalculation.md).
  - Added flowchart diagrams.


## 49.0 Beta
December 25th, 2024
#### Overview
First version released to public.

Many fixes, a license, revamped docs, and a better file system.

#### Fixed Bugs
  - Gitignore in all branches not ignoring .venv/ folder. Otherwise, VS Code says too many changes and won't show the git changes for any other branch.
  - Line counter bug where gitignore items were not being ignored due to Windows using backslashes in their paths.
  - Fixed a lot of bugs with bad pathing (now using `os.path.join` to navigate to specific folders)

#### Files
  - Renamed `ml-test.py` to `train_algorithm.py`
  - Put all docs in the `docs` folder
  - Add a generated files folder

#### Licensing and Attribution
  - Added the license
  - Referenced licenses for all parent packages used
  - Updated conventions, tests, and scripts to include license in header

#### Docs
  - Added instructions to creating secrets.txt to the ReadMe.
  - Updated ReadMe
    - Updated file instructions, file names, and directory names to match current ones.
    - Added link to contribution guidelines.
  - Added contribution guidelines
  - Added setup docs
  - Added running the project docs
  - Added FAQs
  - Added Conventions page
    - Create standard variable naming, file naming, and code conventions
  - Reorganized this `todos.md` page and sorted by category.

#### Tests
  - Added tests for new license headers in Python files
  - Added tests for correct files in correct places


#### Other
  - Removed references to heatmap stuff (unused)
  - Updated the `__all__` variable in `commonresources.py`
  - Made the season year an input variable
  - Uploaded to GitHub
    - Added name and description
    - Added issue and feature request templates
    - Added milestones
    - Added tags

## 48.0 Alpha
August 24th, 2024
#### Overview
Wow, this update took awhile. here's the overview:

 - Redid the file system
 - Added tests
 - Fixed numerous bugs
 - Added diagram to files (soon to be in docs)
 - Updated ReadMe (still needs work)

#### Bugs
Fixed a lot of bugs:

 - Joblib Cachewarning due to oversized path (only on Windows machines)
 - global OPR calculation running during events, causing rediculously slow cycle times
 - OPR was "really wrong for some reason."
 - Version number wasn't correctly displayed
 - *Lots more that I forgot about or don't care to mention*

#### Other changes
 - Renamed files to remove versions in their names. Ex: `ftcapiv4.ps1` -> `ftcapi.ps1`
 - Updated version number
 - Added a virtual environment directory option to the main powershell script
 - Retrained the algorithms
 - Added tests to make sure files in `app` were scripts and files in `app/generatedfiles` were not scripts.
 - Added a couple debug/stats tools (probably temporary)
   - `flushGeneratedFiles.ps1`
   - `linecounter.py`
 - Updated the `LICENSE.txt`
 - Updated the ReadMe
 - Redid the file system
   - Most scripts are in the `apps` folder
   - Generated files are in the `apps/generatedfiles` folder
   - Tests are in the `tests` folder
   - Gitignore now properly works

That's all for now!


## 47.1
#### General
Fixed a bunch of bugs. \
Made the ReadMe more readable. \
Added `FieldMode`, a variable when true will disable global OPR calculation (saves cpu time not needed) \
Reduced size of certain matrices (lower RAM and faster overall!). \
Now rounding stats to 14 places instead of 10 for greater accuracy and precision. \
Various code quality-of-life and clarity updates. \
Added a python script [`init_settings.py`](init_settings.py) to keep track of all global settings. \
**Added git** (version control yay!). \
Deleted archive files.

#### Windows Support!
Added support for windows (added ``ftcapiv4.ps1``). \
Added a new virtual environment (outside of working directory for now), `ftcapivenvwindows` for windows, 
because apparently the other one just didn't work at all on windows for whatever reason.

## 46.1
Lots of machine learning stuff and some bug fixes.

The biggest thing is better organization of data;
Machine learning training set now calculates OPR and recent OPR more accurate to time period of the match,  calculated using only the matches before the given match.

Some optimizations were made (thanks to [Scalene](https://github.com/plasma-umass/scalene) for allowing me to pinpoint the most troublesome lines of code)


## 45.1
Mostly backend stuff, renamed `OPRv4-event.py` to `OPRv4.py` for importability and made it more modular.
Various changes for code readability.

In addition, the flow of the machine learning prep stuff is being redone and being made a *lot* easier to use.

### Features
#### New Machine Learning Prep
The machine learning preparation in `prepare-machinelearning.py` has been redone and now calculates the team stats relative to the time period in which the match was played, allowing for a better trained machine learning algorithm.

## 44.1
Various bugfixes, no real new features since 43-1.

### Features
#### An Error Log!
Whether an error is printed to the terminal or not, the common ones will be added to error.log with a datestamp and timestamp.

### Fixes
 - No rankings bug (malformed authentication headers in curl request)