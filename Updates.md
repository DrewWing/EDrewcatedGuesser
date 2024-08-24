# Updates

Remember to check out the [README](README.md) file

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