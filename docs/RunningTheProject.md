# How to Run the Project

# <p style="color:orange"><u>**This Documentation is currently a WORK IN PROGRESS**</u></p>

## Windows
Most of the time, you should be running the program `ftcapi.ps1`. \
It is reccomended to use the `-h` argument to get familiar with the arguments. You may alternatively use 
```powershell
Get-Help -Name 'YOUR_PATH_TO_THIS_PROJECT\app\ftcapi.ps1'
```


### During Events
During events, there are three really important parameters:
   - `FieldMode`, a boolean which should be set to `True` during an event. See the below section for more info on what it does.
   - `EventCode`, an alphanumeric code that FTC uses to keep track of their events. It is usually found in the URL of the ftc-events or ftc-scout website.
   - `SeasonYear`, a string or integer describing the first year of the season. For instance, the 2023-2024 season is just "`2023`." Defaults to "`2023`"

Your typical configuration during an event with an event code of `FTCCMPFRAN1` is going to look something like this:
```powershell
. 'your_path_to_the_directory\ftcapi.ps1' -FieldMode $True -EventCode "FTCCMPFRAN1" -SeasonYear 2023
```

### Between Events
Between events, it's a good idea to rerun the program at least once with `FieldMode` set to `False`. This will enable updating the *global calculations* (more CPU taxing), which will be saved and used during the next event. It is reccomended to do this soon before the event (the `EventCode` doesn't matter for global statistics) to get the most up-to-date statistics on the teams.
> Note that the `FieldMode` feature might be slightly broken, and will be addressed in post-release updates.

You can also add the flag `-OneCycle` to only perform one cycle and then terminate.

A configuration between events might look something like this:
```powershell
. 'your_path_to_the_directory\ftcapi.ps1' -OneCycle -Fieldmode $False
```

## Linux
**The current version of this program does not support Linux, don't use it right now. It will be fixed in a post-release update.**
To run the program after setting up the correct variables (see below), run the `ftcapi.sh` program, which kind of calls everything else. If you want to do anything other than the basics, you're going to have to dig a little deeper into the code. Use the `h` modifier to get the help menu.

### MacOS
**The current version of this software does not support MacOS. There are currently no plans to implement support.**
