# Conventions
All of the informal rules for naming, whitespace, etc. for the entire project.

## Directories and Files
### Naming Directories
Directory names should be lowercase, without spaces, underscores, or dashes.
Honestly, this should be changed later but that's the way it is right now.

### Naming Files
Category | Naming | Example |
-|-|-
Python | No uppercase. Underscores separate words if needed. | `python_settings.py`
Powershell | Camel Case, but first letter is lowercase. No word separators | `flushGeneratedFiles.ps1`
Markdown | Camel Case | `StablePackageVersions.md`
Trained ML Models | If using Grid Search, start with `gs`. Then an abbreviated version of the model type (first letter capitalized). | `gsNeigh.pkl` or `gsSVC.pkl`


## Python Code

### Layout
All python files should start with the following:
```
#
# -*- coding: utf-8 -*-
# Name of the File (Title Case)
# Started MM-DD-YYYY
# by Drew Wingfield

# Description:
# Enter the description here (what this file does/provides).

# This file is a part of Drew Wingfield's FTCAPI program.
# See the documentation in the README.md file.
# See the license in the LICENSE.txt file.
```


All imports should be within a region defined by `#region <region name>` and `#endregion <region name>`.



### General
Lines should be no longer than 5 billion characters long (haha TODO decide this).




## Powershell Code
Insert text here.

