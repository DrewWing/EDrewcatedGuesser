# Updates

Remember to check out the [README](README.md) file

## 47.1
Reduced size of certain matrices (lower RAM and faster overall!). \
Now rounding stats to 14 places instead of 10 for greater accuracy and precision. \
Various code quality-of-life and clarity updates. \
Added support for windows (added a powershell file). \
Added a new virtual environment (outside of working directory for now), `ftcapivenvwindows` for windows, 
because apparently the other one just didn't work at all on windows for whatever reason.
Added a python script [`init_settings.py`](init_settings.py) to keep track of all global settings. \
**Added git** (version control yay!). \
Deleted archive files.

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