# Frequently Asked Questions


## I'm a noob and don't know what any of this means!
A basic understanding of the command line is required for this project (PowerShell if on Windows, and BASH if on most Linux distros).
This project is a command line interface, and does not have a graphical user interface (GUI).

## I'm having trouble setting up/running
Please make sure you followed the documentation for each, and their respective troubleshooting sections.


## I followed all documentation but have found a bug
Please check the GitHub Issues page to see if a relevant issue already exists. If not, please create an issue and follow the template.


## I want X feature!
Try searching the [todos page](todos.md) and all existing GitHub issues. 
If you still haven't found the feature you want, create an issue and follow the template.


## Packages are all messed up!
Try removing and recloning the repository. If that doesn't work, run the `venvSetup` script with the `-replace` flag, which removes the current Virtual Environment and performs a fresh install of the required packages.

If that still doesn't work, you may have to install the packages yourself. Installing from `requirements.txt` should work, but if it doesn't, try installing the specific versions found in [StablePackageVersions](StablePackageVersions.md).

