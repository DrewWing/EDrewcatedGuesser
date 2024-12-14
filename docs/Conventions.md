# Conventions
All of the informal rules for naming, whitespace, etc. for the entire project.
Most of this is reminders for myself.

## Git
### Branches
Branches should be named starting with `feat/`, `fix/`, or `dev/` (for features, hotfixes, and general development, respectively). They should then contain the brief description separated by dashes `-`. No capital letters. References to files should replace underscores with dashes.

Ex: `feat/linecounter-language-support` \
Ex: `fix/json-parse-encoding-syntax-bug`


## Directories and Files
### Naming Directories
Directory names should be lowercase, without spaces, underscores, or dashes.
Honestly, this should be changed later but that's the way it is right now.

### Naming Files
Category | Naming | Example |
-|-|-
Python, CSV, Json | No uppercase. Underscores separate words if needed. | `python_settings.py`<br>`team_list_filtered.csv`
Powershell | Camel Case, but first letter is lowercase. No word separators | `flushGeneratedFiles.ps1`
Markdown* | Camel Case | `StablePackageVersions.md`
Trained ML Models | If using Grid Search, start with `gs`. Then an abbreviated version of the model type (first letter capitalized). | `gsNeigh.pkl` or `gsSVC.pkl`

*Notable eceptions are the `README.md`, `COPYING`, `LICENSE.txt`, and `todos.md` files.


## Markdown Files
All Markdown files and other documentation media should be in the `docs` folder (except `README.md` and licensing stuff).
Images relating to markdown files should be in `docs/images`.

## Python Code

### Layout

#### Header
All python files should use the UTF-8 encoding and start with the following:
```python
#
# -*- coding: utf-8 -*-
# Name of the File (Regular title case with spaces)
# Started MM-DD-YYYY
# by Drew Wingfield
#
# Copyright (C) 2024, Drew Wingfield
#
# This script is part of EDrewcated Guesser by Drew Wingfield.
# EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
# the terms of the AGNU Affero General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the AGNU Affero General Public License for more details.
#
# You should have received a copy of the AGNU Affero General Public License along with 
# EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.
#
# See the documentation in the README.md file.
#
"""
A short description of what this script is and provides.

See the documentation in the README.md file.

Copyright (C) 2024, Drew Wingfield

This script is part of EDrewcated Guesser by Drew Wingfield.
EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
the terms of the AGNU Affero General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the AGNU Affero General Public License for more details.

You should have received a copy of the AGNU Affero General Public License along with 
EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.


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
        Copyright (C) 2024, Drew Wingfield

        This script is part of EDrewcated Guesser by Drew Wingfield.
        EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
        the terms of the AGNU Affero General Public License as published by the Free Software 
        Foundation, either version 3 of the License, or (at your option) any later version.

        EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
        WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
        PURPOSE. See the AGNU Affero General Public License for more details.

        You should have received a copy of the AGNU Affero General Public License along with 
        EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.


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

#### Header
All bash files should start with the following. Note the lack of a shebang as usually the Virtual Environment should already be activated.
```bash
#
# -*- coding: utf-8 -*-
# Name of the script (title case, with spaces)
#
# Copyright (C) 2024, Drew Wingfield
#
# This script is part of EDrewcated Guesser by Drew Wingfield.
# EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
# the terms of the AGNU Affero General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
# PURPOSE. See the AGNU Affero General Public License for more details.
#
# You should have received a copy of the AGNU Affero General Public License along with 
# EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.
#
# See the documentation in the README.md file.
#
# Description:
# A description of the script
#
```


## Other Code/resources
All other code, resources, or other files must contain at the top (or close to the top) of the file the following:
```
Copyright (C) 2024, Drew Wingfield

This [script/document/file] is part of EDrewcated Guesser by Drew Wingfield.
EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
the terms of the AGNU Affero General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the AGNU Affero General Public License for more details.

You should have received a copy of the AGNU Affero General Public License along with 
EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.

See the documentation in the README.md file.
```

