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

### Licensing and Attribution 
Note that all tasks should be tagged `[license]` and `[critical]`.
  - [ ] `[License]` `[Critical]` Update all files to include a reference to the license and this file
    - [ ] Scripts in `app` folder
    - [ ] `tests` folder
    - [ ] `__init__.py`
  
  - [ ] `[License]` `[Critical]` Make sure licensing is correct for all packages used.
    - [ ] Update the `requirements.txt` to use only needed packages.
    - [ ] Here is the output of `pipdeptree -fl`. Thanks whoever you are for the package, it really helps!
      ```
      google-api-python-client==2.146.0
        google-api-core==2.20.0
          google-auth==2.35.0
            cachetools==5.5.0
            pyasn1_modules==0.4.1
              pyasn1==0.6.1
            rsa==4.9
              pyasn1==0.6.1
          googleapis-common-protos==1.65.0
            protobuf==5.28.2
          proto-plus==1.24.0
            protobuf==5.28.2
          protobuf==5.28.2
          requests==2.32.3
            certifi==2024.8.30
            charset-normalizer==3.3.2
            idna==3.10
            urllib3==2.2.3
        google-auth==2.35.0
          cachetools==5.5.0
          pyasn1_modules==0.4.1
            pyasn1==0.6.1
          rsa==4.9
            pyasn1==0.6.1
        google-auth-httplib2==0.2.0
          google-auth==2.35.0
            cachetools==5.5.0
            pyasn1_modules==0.4.1
              pyasn1==0.6.1
            rsa==4.9
              pyasn1==0.6.1
          httplib2==0.22.0
            pyparsing==3.1.4
        httplib2==0.22.0
          pyparsing==3.1.4
        uritemplate==4.1.1
      matplotlib==3.9.2
        contourpy==1.3.0
          numpy==2.1.1
        cycler==0.12.1
        fonttools==4.54.0
        kiwisolver==1.4.7
        numpy==2.1.1
        packaging==24.1
        pillow==10.4.0
        pyparsing==3.1.4
        python-dateutil==2.9.0.post0
          six==1.16.0
      pandas==2.2.3
        numpy==2.1.1
        python-dateutil==2.9.0.post0
          six==1.16.0
        pytz==2024.2
        tzdata==2024.2
      pipdeptree==2.23.4
        packaging==24.1
        pip==24.2
      pyarrow==17.0.0
        numpy==2.1.1
      scikit-learn==1.5.0
        joblib==1.4.2
        numpy==2.1.1
        scipy==1.14.1
          numpy==2.1.1
        threadpoolctl==3.5.0
      setuptools==65.5.0
      ```

      So overall, the packages that I need to explicitly cite are:
      ```
      google-api-python-client>=2.119.0
      matplotlib>=3.8.3
      numpy>=1.26.4 (explicitly imported)
      pandas>=2.2.0
      pyarrow>=15.0.0 (really not sure what this does but it's in requirements so idk)
      scikit-learn==1.5.0
      ```
    - [ ] Figure out what pyarrow does and if it's used or needed
    - [ ] Also figure out a way to cite/get license of the FTC API

### Other
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