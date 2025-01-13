# To-Dos
This is the `todos.md` file. For more information, please read the [Readme](README.md).

Items labeled `Critical` need to be fixed/completed before the next release, and should be listed before non-critical items.

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


## Upcoming Timeline
<!-- ### November 2024
Finish features for release, flesh out docs, possibly get ML algorithm training bugfree.

#### Priorities During November
1. Fixing Critical Bugs
2. Adding Critical Features
3. Documentation
   1. Project Setup
   2. Running the Project
   3. Training a New Algorithm (if implemented)
4. Licensing -->

<!-- ### December 2024

#### Priorities
1. Licensing
2. Documentation
   1. Project Setup
   2. Running the Project
   3. ~~Training a New Algorithm~~ (did not meet feature deadline, pushed back to post-release)
3. Minor bugfixing
4. polish

#### Deadlines
**December 1st:** Hard deadline for new features. Any feature not functional is put on pause until post-release updates.

**December 18th:** Train algorithm for current season.

**December 19th:** Soft deadline of no more commits. Upload project to GitHub and start setting up issue templates, etc.

**December 22nd:** Hard deadline of no commits (except to fix critical bugs). Attempt a fresh install, setup, and run.

**December 24th:** Hard deadline of release. -->


### Release items
  - [ ] Set up GitHub stuff
  - [ ] Clone repo to new folder, run setup from scratch and verify it works
  - [X] ~~Reread all documentation~~
  - [ ] Release


### Post-Release
1. Re-evaluate priorities
2. Make algorithm training usable
3. Fix bugs


## To-Do Items

### GitHub
  - [X] ~~Add name and description~~
  - [X] ~~Add issue templates~~
  - [ ] Transfer to-do list?
    - [X] ~~Create Milestones~~
    - [X] ~~Create and assign tags~~
    - [ ] Create Issues
  - [ ] Set up PR template
  - [ ] Set up public permissions (PR permissions)
  - [X] Create release (December 24th)
    - [X] Switch all version references to new version
    - [X] Add to changelog
    - [X] Commit using new version tag
  - [X] Publication (December 25th)
    - [X] Make repo public
    - [ ] Update my website
    - [ ] Announce release on all channels


### Bugs
  - [ ] `[PowerShell]` `[FTC API]` `[REST]` All teams in opr/all-teams are invalid API request messagees, due to the team # being put in as the event code.
    - [ ] Figure out where in the world these files keep coming from! (unused)
  - [ ] `[OPR]` `[Accuracy]` Weird bug with some teams' recent OPR calculated as 0 for lower amounts of days (30)
    - Probably due to the team not playing matches within the last 30 days - fix and just replace with their respective all-time OPRs insted (requires re-training of machine learning algorithms)
  - [ ] `[Tests]` `[Argparse]` Import tests fail due to argparse.
  - [ ] `[Sheets]` Implement version checking in Google Sheet (make sure sheet template is compatible with current software version)



### Tests
  - [ ] `[Code]` `[Tests]` Create script to update test pass/fail status in the `README.md` file.
  - [ ] `[Code]` `[Tests]` Add tests
    - [ ] Machine learning is recent to the correct season  year
    - [ ] Conventions
      - [ ] Proper header for all scripts
        - [X] ~~Python~~
        - [ ] Powershell
        - [ ] BASH


### Config
  - [ ] `[Config]` Revamp the configuration and multiscript variable situation
    - [ ] `[Code]` `[Config]` Add an easily editable configuration file (yaml?)
  - [ ] `[Config]` Add Spreadsheet ID and api key json file location to secrets.txt


### Files
  - [ ] ~~`[Files]` `[WontFix]` Remove these files before release (dev tools or generally not needed)~~
    - [ ] ~~all packages.txt~~
    - [ ] ~~flushGeneratedFiles.ps1~~
    - [ ] ~~line_counter.py~~
    - [ ] ~~view_data.py?~~
  - [ ] `[Files]` Rename scripts to match their function better and update all references to those scripts.


### Optimizations
  - [ ] `[Speed]` Convert more things to use numpy matrices instead of pandas dataframes (much faster)
    - prepare-machinelearningpy training_data_matches
  - [ ] `[Speed]` Maybe add GPU/NPU support?
    - [ ] Switch to Pytorch?
    - [ ] Use CUDA?
  - [ ] `[Speed]` Convert project to C++ so it runs faster.


### Other
  - [ ] `[Code]` Make Google Sheets pushing optional, and add option for local spreadsheet
  - [ ] `[Code]` Add markdown support for line  counter
  - [ ] `[Code]` Convert all Python scripts to be completely object-oriented, make master Python script replacing PowerShell/BASH scripts.
  - [ ] `[Code]` Add feature of ftcapi.ps1 to detect if .venv was selected but no .venv exists, and asks the user whether they would like the script to automatically create the venv for them using the venv creation script.
  - [ ] `[OS Support]` `[Future]` Linux support
    - [ ] Fix Linux BASH scripts
    - [ ] Make sure everything works on Linux
  - [ ] `[Code]` In the PowerShell script, warn user if `secrets.txt` does not exist.
  - [ ] `[Git]` Perhaps ignore all `.log` files in `.gitignore`?
  - [ ] `[Code]` `[DeadCode]` Remove the `rankings_dataframe` function in jsonparse, it seems to not be called anywhere
  - [ ] `[Code]` `[Feature]` Add a write_json function in commonresources? (make write_needed_events in jsonparse less complex?)
  - [ ] `[General]` Get a better Todo system (use a bug-tracking system?)
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