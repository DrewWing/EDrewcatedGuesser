# How to Run the Project

# <p style="color:red"><u>**This Documentation is currently OUTDATED**</u></p>

## During Events
## Outside of Events
### Windows
Most of the time, you should be running the program `ftcapi.ps1`. \
It is reccomended to use the `-h` argument to get familiar with the arguments.


#### During Events
During events, there are two really important parameters:
   - `FieldMode`, a boolean which should be set to `True` during an event. See the below section for more info on what it does.
   - `EventCode`, an alphanumeric code that FTC uses to keep track of their events. It is usually found in the URL of the ftc-events or ftc-scout website.

Your typical configuration during an event with an event code of `FTCCMPFRAN1` is going to look something like this:
```powershell
. 'your_path_to_the_directory\ftcapi.ps1' -FieldMode $True -EventCode "FTCCMPFRAN1"
```

#### Between Events
Between events, it's a good idea to rerun the program at least once with `FieldMode` set to `False`. This will enable updating the *global calculations* (more CPU taxing), which will be saved and used during the next event. It is reccomended to do this soon before the event (the `EventCode` doesn't matter for global statistics) to get the most up-to-date statistics on the teams.

You can also add the flag `-OneCycle` to only perform one cycle and then terminate.

A configuration between events might look something like this:
```powershell
. 'your_path_to_the_directory\ftcapi.ps1' -OneCycle -Fieldmode $False
```

### Linux
**The current version of this program is broken, don't use it right now. It will be fixed... hopefully... sometime later...**
To run the program after setting up the correct variables (see below), run the `ftcapi.sh` program, which kind of calls everything else. If you want to do anything other than the basics, you're going to have to dig a little deeper into the code. Use the `h` modifier to get the help menu.

### MacOS
Good luck haha. I've had enough trouble adding support for both Linux and Windows, so there's no way I'm going to spend another 2,000 hours attempting to add MacOS support.