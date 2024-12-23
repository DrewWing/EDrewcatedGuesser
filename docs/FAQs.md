# Frequently Asked Questions

## Why the name EDrewcated Guesser?
This project started out as a simple scouting spreadsheet for team #12928, the LightSaders. It originally attempted to "guess" the outcome of matches based on the collective OPR of each team. Since my name is Drew, "EDrewcated Guesser" came pretty naturally.

Of course this program is much more advanced. It calculates several timelines of each team's OPR, AutoOPR, and CCWM, and uses two separate machine learning algorithms (some might call this AI, but I don't) to predict matches with great accuracy.

It also takes care of fetching and filling out the match schedule for you, which is an absolute pain to enter manually.


## I'm a noob and don't know what any of this means!
A basic understanding of the command line is required to set up and run this project (PowerShell if on Windows, and BASH if on most Linux distros).


## Does this have a GUI?
Currently this project is CLI only, but I'm considering adding a GUI in some later update.


## I'm having trouble setting up and/or am getting errors while running.
Please make sure you followed the documentation for each, and their respective troubleshooting sections.
Most errors will be logged in the `app/generatedfiles/errors.log` file. You may also increase the debug level for more verbosity in the terminal.
> Note: You may set the debug level by using the `DebugLevel` parameter. 0 produces no debug output, and each additional integer adds more debug print statements.


## I followed all documentation and have troubleshooted, but still found a bug
Please check the GitHub Issues page to see if a relevant issue already exists. If not, please create an issue and follow the template.


## I want X feature!
Try searching the [todos page](todos.md) and all existing GitHub issues. 
If you still haven't found the feature you want, create an issue and follow the template.


## Packages are all messed up!
Try running the `venvSetup` script with the `-replace` flag, which removes the current Virtual Environment and performs a fresh install of the required packages. 

If that doesn't work, you may have to install the packages yourself. Installing from `requirements.txt` should work, but if it doesn't, try installing the specific versions found in [StablePackageVersions](StablePackageVersions.md).

## Can I repurpose this project and use it commercially?
Absolutely not. See the project license at [`license.txt`](../LICENSE.txt).
In addition, this project relies on the FIRST API (ruled by their [terms of service](https://frc-events.firstinspires.org/services/api/terms)), which clearly states:
> You shall not do any of the following:
> - make any commercial use (i.e. use that generates revenue) of the APIs, API Documentation or Events Data. This means that You may not:
>   - sell the Events Data, or
>   - sell access to the Events Data, or
>   - include any of the Events Data in an any product or service that You sell, or
>   - make any of the Events Data available to any other person or entity for that other person or entity to sell access to, or include, any of the Events Data in any product or service that is sold;
> >
> ...

(The Terms of Service was referenced December 16th, 2024, using the February 1, 2021 version of the Terms)

