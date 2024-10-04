# To-Dos
This is the `todos.md` file. For more information, please read the [Readme](README.md).

Items labeled `Critical` need to be fixed/completed before release.

### Bugs
  - [ ] `[Powershell]` `[FTC API]` `[REST]` All teams in opr/all-teams are invalid API request messagees, due to the team # being put in as the event code.
    - [ ] Figure out where in the world these files keep coming from! (unused)
  - [ ] `[Speed]` Maybe add GPU/NPU support?
    - [ ] `[Code]` Switch to Pytorch?
  - [ ] `[OPR]` `[Accuracy]` Weird bug with some teams' recent OPR calculated as 0 for lower amounts of days (30)
    - Probably due to the team not playing matches within the last 30 days - fix and just replace with their respective all-time OPRs insted (requires re-training of machine learning algorithms)
  - [ ] `[Tests]` `[Argparse]` Import tests fail due to argparse.
  - [X] ~~`[Critical]` `[Git]` `[External]` Fix the gitignore in all branches to ignore .venv/ folder. Otherwise, VS Code says too many changes and won't show the git changes for any other branch.~~

### Other
  - [ ] `[Code]` `[Tests]` Create script to update test pass/fail status in the `README.md` file.
  - [ ] `[Code]` Update the `__all__` variable in `commonresources.py`. Figure out if it's even needed.
  - [ ] `[Code]` In the powershell script, warn user if `secrets.txt` does not exist.
  - [ ] `[Git]` Perhaps ignore all `.log` files in `.gitignore`?
  - [ ] `[ReadMe]` Add documentation about `venvSetup.ps1` script.
  - [ ] `[Code]` `[DeadCode]` Remove the `rankings_dataframe` function in jsonparse, it seems to not be called anywhere
  - [ ] `[Code]` `[Feature]` Add a write_json function in commonresources? (make write_needed_events in jsonparse less complex?)
  - [ ] `[Code]` Have a standard variable, class, and function naming system (camel case vs underscores vs etc.)
  - [ ] `[Files]` Rename ml-test.py to something else more descriptive (and excluding the - symbol)
  - [ ] `[General]` Get a better Todo system (use a bug-tracking system?)
  - [ ] `[OS Support]` `[Critical]` Linux support
    - [ ] Fix Linux BASH scripts
    - [ ] Make sure everything works on linux
  - [ ] `[License]` `[Critical]` Update all files to include a reference to the license and this file
    - [ ] Scripts in `app` folder
    - [ ] `tests` folder
    - [ ] `__init__.py`
  - [ ] `[Files]` `[Critical]` Remove these files before release (dev tools or generally not needed)
    - [ ] all packages.txt
    - [ ] flushGeneratedFiles.ps1
    - [ ] linecounter.py
    - [ ] viewdata.py?
  - [ ] `[Files]` `[Docs]` Put all doc files (readme and updates) into a docs folder?
  - [ ] `[Code]` `[QOL]` Redo all the path things to make them better lol
  - [ ] `[Code]` `[Tests]` Add tests
    - [X] ~~Correct files in correct places~~
    - [ ] Machine learning is recent to the correct season  year
  - [X] ~~`[QOL]` `[variables]` In ftcapiv4.ps1, make the season year an input variable~~ (or automatic?)
  - [X] ~~`[QOL]` `[Files]` Organize generated files into a single folder and update the .gitignore~~
    - [ ] `[Readme]` Update Readme file instructions, file names, and directory names to match current ones.
  - [X] ~~Remove all references to heatmap stuff.~~
  - [ ] `[QOL]` `[Code]` `[Arguments]` Make all python files use argparse
  - [ ] `[Sheets]` `[Readme]` Add instruction for how to use the Google Sheets
  - [ ] `[Sheets]` `[QOL]` `[Feature]` It would be nice to add the team name to the number when pushing to sheets
  - [ ] `[Critical]` `[Readme]` Add instructions to creating secrets.txt to the readme (authorizationheader needs to be no spaces or quotes)
  - [ ] `[QOL]` `[Readme]` Redo the README.
  - [ ] `[QOL]` `[DeadCode]` Remove all unneccessary files
    - [ ] `[DeadCode]` Figure out what to do with viewdata.py
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