
# venvSetup.ps1
# by Drew Wingfield
# created on September 20th, 2024
# by Drew Wingfield

# Please see the README.txt and LICENSE.txt files for more info.

param (
    [switch]$help = $false, #TODO: add this feature
    [switch]$h = $false,
    [switch]$replace = $false,
    [switch]$DryRun = $false,
    [int]$DebugLevel = 0, # Debug level of python scripts
    [string]$VenvName = ".venv" # The directory of virtual environment to use
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
Write-Output "`n`n Installing required packages... `n" >> $logPath
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


