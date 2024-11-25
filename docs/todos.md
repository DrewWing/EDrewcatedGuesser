# To-Dos
This is the `todos.md` file. For more information, please read the [Readme](README.md).

Items labeled `Critical` need to be fixed/completed before release, and should be listed before non-critical items.

## Upcoming Timeline
### November 2024
Finish features for release, flesh out docs, possibly get ML algorithm training bugfree.

#### Priorities During November
1. Fixing Critical Bugs
2. Adding Critical Features
3. Documentation
   1. Project Setup
   2. Running the Project
   3. Training a New Algorithm (if implemented)
4. Licensing

### December 2024

#### Priorities During December
1. Licensing
2. Documentation
   1. Project Setup
   2. Running the Project
   3. Training a New Algorithm (if implemented)
3. Minor bugfixing
4. polish

**December 1st:** Hard deadline for new features. Any feature not functional is put on pause until post-release updates.
**December 18th:** Train algorithm for current season. \
**December 19th:** Soft deadline of no more commits. Upload project to GitHub and start setting up issue templates, etc. \
**December 22nd:** Hard deadline of no commits (except to fix critical bugs). Attempt a fresh install, setup, and run. \
**December 24th:** Hard deadline of release.

## To-Do Items

### GitHub
  - [ ] Add name and description
  - [ ] Add issue templates
  - [ ] Transfer to-do list?
    - [ ] Create Milestones
    - [ ] Create and assign tags
    - [ ] Create Issues
  - [ ] Set up PR templates
  - [ ] Set up public permissions (PR permissions)
  - [ ] Create release (December 23rd)
  - [ ] Publication (December 24th)
    - [ ] Make repo public
    - [ ] Update my website
    - [ ] Announce release on all channels


### Bugs
  - [X] ~~`[Critical]` `[Git]` `[External]` Fix the gitignore in all branches to ignore .venv/ folder. Otherwise, VS Code says too many changes and won't show the git changes for any other branch.~~
  - [ ] `[PowerShell]` `[FTC API]` `[REST]` All teams in opr/all-teams are invalid API request messagees, due to the team # being put in as the event code.
    - [ ] Figure out where in the world these files keep coming from! (unused)
  - [ ] `[OPR]` `[Accuracy]` Weird bug with some teams' recent OPR calculated as 0 for lower amounts of days (30)
    - Probably due to the team not playing matches within the last 30 days - fix and just replace with their respective all-time OPRs insted (requires re-training of machine learning algorithms)
  - [ ] `[Tests]` `[Argparse]` Import tests fail due to argparse.
  - [ ] `[Sheets]` Implement version checking in Google Sheet (make sure sheet template is compatible with current software version)

### Docs
  - [ ] `[Critical]` `[Readme]` Add instructions to creating secrets.txt to the readme (authorizationheader needs to be no spaces or quotes)
  - [ ] `[Critical]` `[Readme]` `[Docs]` Update Readme file instructions, file names, and directory names to match current ones.
  - [ ] `[Critical]` `[ReadMe]` Add documentation about `venvSetup.ps1` script.
  - [X] ~~`[Docs]` Reorganize this `todos.md` page and sort by category.~~


### Tests
  - [ ] `[Code]` `[Tests]` Create script to update test pass/fail status in the `README.md` file.
  - [ ] `[Code]` `[Tests]` Add tests
    - [X] ~~Correct files in correct places~~
    - [ ] Machine learning is recent to the correct season  year


### Config
  - [ ] `[Config]` Revamp the configuration and multiscript variable situation
    - [ ] `[Code]` `[Config]` Add an easily editable configuration file (yaml?)
  - [ ] `[Config]` Add Spreadsheet ID and api key json file location to secrets.txt


### Files
  - [ ] `[Files]` `[Critical]` Remove these files before release (dev tools or generally not needed)
    - [ ] all packages.txt
    - [ ] flushGeneratedFiles.ps1
    - [ ] line_counter.py
    - [ ] view_data.py?
  - [ ] `[Files]` Rename scripts to match their function better and update all references to those scripts.
  - [X] ~~`[Files]` Rename ml-test.py to something else more descriptive (and excluding the - symbol)~~
  - [X] ~~`[Files]` `[Docs]` Put all doc files (readme and updates) into a docs folder?~~
  - [X] ~~`[QOL]` `[Files]` Organize generated files into a single folder and update the .gitignore~~
  - [X] ~~Remove all references to heatmap stuff.~~


### Optimizations
  - [ ] `[Speed]` Convert more things to use numpy matrices instead of pandas dataframes (much faster)
    - prepare-machinelearningpy training_data_matches
  - [ ] `[Speed]` Maybe add GPU/NPU support?
    - [ ] `[Code]` Switch to Pytorch?


### Other
  - [ ] `[Code]` Make Google Sheets pushing optional, and add option for local spreadsheet
  - [ ] `[Code]` Add markdown support for line  counter
  - [ ] `[Code]` Convert all Python scripts to be completely object-oriented, make master Python script replacing PowerShell/BASH scripts.
  - [ ] `[Code]` Add feature of ftcapi.ps1 to detect if .venv was selected but no .venv exists, and asks the user whether they would like the script to automatically create the venv for them using the venv creation script.
  - [ ] `[License]` `[Critical]` Update all files to include a reference to the license and this file
    - [ ] Scripts in `app` folder
    - [ ] `tests` folder
    - [ ] `__init__.py`
  - [ ] `[OS Support]` `[Critical]` Linux support
    - [ ] Fix Linux BASH scripts
    - [ ] Make sure everything works on Linux
  - [X] ~~`[Code]` Update the `__all__` variable in `commonresources.py`.~~
  - [ ] `[Code]` In the PowerShell script, warn user if `secrets.txt` does not exist.
  - [ ] `[Git]` Perhaps ignore all `.log` files in `.gitignore`?
  - [ ] `[Code]` `[DeadCode]` Remove the `rankings_dataframe` function in jsonparse, it seems to not be called anywhere
  - [ ] `[Code]` `[Feature]` Add a write_json function in commonresources? (make write_needed_events in jsonparse less complex?)
  - [X] ~~`[Code]` Have a standard variable, class, and function naming system (camel case vs underscores vs etc.)~~
  - [ ] `[General]` Get a better Todo system (use a bug-tracking system?)
  - [X] ~~`[Code]` `[QOL]` Redo all the path things to make them better lol~~
  - [X] ~~`[QOL]` `[variables]` In ftcapiv4.ps1, make the season year an input variable~~ (or automatic?)
  - [ ] `[QOL]` `[Code]` `[Arguments]` Make all Python files use argparse
  - [ ] `[Sheets]` `[Readme]` Add instruction for how to use the Google Sheets
  - [ ] `[Sheets]` `[QOL]` `[Feature]` It would be nice to add the team name to the number when pushing to sheets
  - [ ] `[QOL]` `[Readme]` Redo the README.
  - [ ] `[QOL]` `[DeadCode]` Remove all unneccessary files
    - [ ] `[DeadCode]` Figure out what to do with view_data.py
    - [X] ~~Figure out where in the world OPR-m.npy comes from~~
    - [X] ~~Figure out if anything in the world uses OPR-m.npy~~
    - [X] ~~All opr/teamstats stuff~~
    - [X] ~~All references to opr/teamstats stuff~~
  - [ ] `[Code QOL]` Making predictions work with both the EventMatches and EventSchedule classes (jsonparse)
    - and the implementation of the predictions in sheetsapi
    - and the processing of the data (getting recent OPRs, etc etc.)
  - [ ] `[QOL]` Adding a user interface?
  - [ ] `[Code QOL]` Make all Python files consistent with PEP 8 and PEP 257