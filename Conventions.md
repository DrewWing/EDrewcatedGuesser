# Conventions
All of the informal rules for naming, whitespace, etc. for the entire project.
Most of this is reminders for myself.

## Directories and Files
### Naming Directories
Directory names should be lowercase, without spaces, underscores, or dashes.
Honestly, this should be changed later but that's the way it is right now.

### Naming Files
Category | Naming | Example |
-|-|-
Python, CSV, Json | No uppercase. Underscores separate words if needed. | `python_settings.py`<br>`team_list_filtered.csv`
Powershell | Camel Case, but first letter is lowercase. No word separators | `flushGeneratedFiles.ps1`
Markdown | Camel Case | `StablePackageVersions.md`
Trained ML Models | If using Grid Search, start with `gs`. Then an abbreviated version of the model type (first letter capitalized). | `gsNeigh.pkl` or `gsSVC.pkl`

Notable eceptions are the `README.md`, `LICENSE.txt`, and `todos.md` files.

## Python Code

### Layout

#### Header
All python files should start with the following:
```python
#
# -*- coding: utf-8 -*-
# Name of the File (Title Case)
# Started MM-DD-YYYY
# by Drew Wingfield
#
"""
A short description of what this script is and provides.

This file is a part of Drew Wingfield's FTCAPI program (EDrewcated Guesser).
See the documentation in the README.md file.
See the license in the LICENSE.txt file.

A longer description of the script goes here, if necessary.
"""
```
Notice that this header does not contain a shebang, as all Python scripts should be run under the Virtual Environment (usually `.venv`).

I'm working on learning the [docstrings](https://peps.python.org/pep-0257/) and will update this when I finish.

#### Imports
All imports should be within a region defined by `#region <region name>` and `#endregion <region name>`. They should further be categorized by builtins, files from this project, then external modules. \
As per [PEP 8](https://peps.python.org/pep-0008), you should only import one module for each line.

#### Constants
Constants should be next, in their own region. See below for naming conventions.

#### Functions
Functions should come next. They may be in their own region, or split up into sub-regions. A `utils` region classifies utility functions/classes that could be in `commonresources.py` but are only used in this one script (for instance, `build_credentials` and `add_timestamp`).

#### Classes
Classes can be before or after functions, they just have to be organized and in their own region.

#### Procedural Code
Code that is procedural in the script should be under the `Procedural` region. Code should be made as object-oriented as possible. Calling code via an `if __name__ == "__main__"` conditional is reccomended, allowing for other scripts to import parts of the given script without tons of code run every time.

---

### General
Generally just please adhere to [PEP 8](https://peps.python.org/pep-0008).

Use double quotes `"` except for certain situations where Python can't handle it (strings within f-strings).

Lines should be no longer than 5 billion characters long (haha TODO: decide this).

Don't ever use `from some_package import *`.

#### Indentation
As per [PEP 8](https://peps.python.org/pep-0008/#indentation), there will be 4 spaces per indentation level. Resistance will not be tolerated.


#### Comments
Comments should be capitalized properly and have a space between the # and the comment.\
Example:
```python
# Add the timestamp to the begining of the data
data_to_push = add_timestamp(data_to_push)
```
Exceptions are TODOs. Comments that are to-do should start with ```TODO: ``` immediately after the # sign.


## PowerShell Code

### Layout

#### Header
All PowerShell files should start with the following:
```powershell
<#
.SYNOPSIS
    A brief description of what the script does.

.DESCRIPTION
    A more detailed explanation of the script's functionality, including its purpose and how it works.
    
    Created/Forked from <other script> on MM-DD-YYYY

    AUTHOR: Drew Wingfield
    VERSION: <The current version of the program>
    COPYRIGHT: 
        This script is a part of Drew Wingfield's FTCAPI program (EDrewcated Guesser).
        Please see the license in the LICENSE.txt and documentation in the README.md file.


.PARAMETER <ParameterName>
    Description of each parameter used by the script.

.EXAMPLE
    Example usage of script.

.EXAMPLE
    Another example usage.

.NOTES
    Additional info.

#>
```

#### Setup
Everything relating to a set-up of the script, including: parameters, variable declarations and virtual environment activation.
These should all be in a region titled `setup` or `Setup`.

#### Functions
All functions should be placed in a region titled `functions` or `Functions`.

#### Procedural
Everything else should be placed under a region titled `procedural` or `Procedural`.

## BASH Code
Insert text here.

