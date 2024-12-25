<#
.SYNOPSIS
    Adds and sets up a Virtual Environment for use with this program.

.DESCRIPTION
    Creates a Virtual Environment at the location specified and installs
    all required packages listed in "requirements.txt".
    Writes a log of packages to "venvSetup.log"
    
    Created on September 20th, 2024

    AUTHOR: Drew Wingfield
    VERSION: 49.0
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

.PARAMETER VenvName
            The (local) path to the directory of the Virtual Environment to use, as a string.
            Defaults to ".venv"
        
.PARAMETER replace
    If a Virtuual Environment currently exists with the path, replaces it.
    Otherwise creates the venv as normal.
    Defaults to false

.NOTES
    Ascii text with the help of https://patorjk.com/software/taag/#p=display&f=Slant&t=Setting%20up...

#>

param (
    [string]$VenvName = ".venv",
    [switch]$replace = $false
)

$currentLocation=Get-Location # The current location, should be the working directory

#Write-Output "current location $currentLocation"
# Ascii text with the help of https://patorjk.com/software/taag/#p=display&f=Slant&t=Setting%20up...
Write-Output " ############################################################ "
Write-Output " #    _____      __  __  _                                  # "
Write-Output " #   / ___/___  / /_/ /_(_)___  ____ _   __  ______         # "
Write-Output " #   \__ \/ _ \/ __/ __/ / __ \/ __ ``/  / / / / __ \        # "
Write-Output " #  ___/ /  __/ /_/ /_/ / / / / /_/ /  / /_/ / /_/ / _ _ _  # "
Write-Output " # /____/\___/\__/\__/_/_/ /_/\__, /   \__,_/ .___/ (_|_|_) # "
Write-Output " #                           /____/        /_/              # "
Write-Output " ############################################################ "

Write-Output " venvSetup.ps1"
Write-Output " Please see the README.txt for more details."
Write-Output " This program will add and set up a virtual environment for use with this program."

$venvPath = Join-Path -Path $currentLocation -ChildPath $venvName
$logPath = Join-Path -Path $currentLocation -ChildPath "venvSetup.log"

Write-Output " The virtual environment will be created on path $venvPath"

if ((Test-Path $venvPath) -and ( $replace -eq $false)){
    Write-Output "`n!! WARNING !!: The virtual environment path already exists!"
    Write-Output "To replace the current venv at this location, please run this script with the -replace flag."
    return 1
} elseif ($replace -eq $true){
    Write-Output "Replacing existing virtual environment (due to the -replace flag)"
    Remove-Item $venvPath -Recurse -Force -Confirm:$false
}

Write-Output " Creating environment... (this could take a minute)"

python -m venv $venvPath

Write-Output " Environment created."
Write-Output " Activating environment..."

$venvActivatePath = Join-Path -Path $venvPath -ChildPath "Scripts/activate.ps1"
Write-Output " Using activate path $venvActivatePath."

. $venvActivatePath  # Activate the new virtual environment

Write-Output " Installing required packages... (this could take up to 10 minutes)"

# Now install all required packages
Write-Output "`n`n $((Get-Date).ToString()) Installing required packages... `n" >> $logPath
python -m pip install -r .\requirements.txt >> $logPath

Write-Output " ############################################################ "
Write-Output " #        ______                      __     __             #"
Write-Output " #       / ____/___  ____ ___  ____  / /__  / /____         #"
Write-Output " #      / /   / __ \/ __ ``__ \/ __ \/ / _ \/ __/ _ \        #"
Write-Output " #     / /___/ /_/ / / / / / / /_/ / /  __/ /_/  __/        #"
Write-Output " #     \____/\____/_/ /_/ /_/ .___/_/\___/\__/\___(_)       #"
Write-Output " #                         /_/                              #"
Write-Output " ############################################################ "
Write-Output " Venv is correctly set up."
Write-Output " Wrote package install log to $logPath"


