
# flushFilesForTransport
# by Drew Wingfield
# Copied from flushGeneratedFiles.ps1 on September 24th, 2024
# by Drew Wingfield

# COPYRIGHT: 
#         Copyright (C) 2024, Drew Wingfield

#         This script is part of EDrewcated Guesser by Drew Wingfield.
#         EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
#         the terms of the AGNU Affero General Public License as published by the Free Software 
#         Foundation, either version 3 of the License, or (at your option) any later version.

#         EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
#         WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
#         PURPOSE. See the AGNU Affero General Public License for more details.

#         You should have received a copy of the AGNU Affero General Public License along with 
#         EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.

# This script is to be used when transporting the project. It removes the virtual environment,
# cache files, and other unnecessary or large files/folders we can regenerate later.

Write-Output "Removing files..."

Remove-Item app/generatedfiles -Exclude *.log -Recurse
Remove-Item app/__pycache__ -Recurse
Remove-Item app/tests/__pycache__ -Recurse

Remove-Item .venv -Recurse

Write-Output "Done removing files."
