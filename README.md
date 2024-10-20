# FTCAPI V48.0 (Alpha)
## by Drew Wingfield

DO NOT DISTRIBUTE!
You may **not** earn money or monetize in any way from this program. It's not just my terms, it's also a part of the terms of using the official FTC API.

**NOTE** that this is an alpha version still in "stealth," so please ignore any references to licenses, in code or on any documentation, except this paragraph. I'll get all that ironed out before I release this.  \
Everything that I'm doing right now is unpublished, so you **may not** use it under any of these unpublished licenses. \
I'm doing my best, just use whatever version is most current under its own license. It has many bugs and is not worth it.

You can find the license [here](LICENSE.txt).
The todo list is [here](docs/todos.md)
Also see the [Updates](docs/Updates.md) page.

## Helpful Documentation Links
 - [How to Set Up the Project (Start Here!)](docs/Setup.md)
 - [Running the program](docs/RunningTheProject.md)
   - During an event
   - Outside of an event
 - [Machine Learning Guide (advanced)](docs/MachineLearningGuide.md)


## Contributing
Add some text here mentioning conventions, PR templates, etc etc. TODO.

## Files, their Purpose, and their Interactions
### Commmon Resources (`commonresources.py`)
The place where most constants and commonly used functions are stored. Pretty much every other python file draws from this. \
Some examples are `red_x`, `green_check`, `PATH_TO_FTCAPI`, `PATH_TO_JOBLIB_CACHE`, and `get_json`.

### Json Parse (`jsonparse.py`)
Documentation goes here!

### Sheets API (`sheetsapi.py`)
Documentation goes here!

### OPR Event (`OPRv4.py`)
Documentation goes here!



## Credits/Honorable Mentions
Though I wrote almost the entirety of the project by myself, I had some help. Below are some resources that I used (whether for copypasting code, general reference, or other research).

This program uses the official FIRST API to get information on matches, schedules, and scores.
You can find it [here](https://frc-events.firstinspires.org/services/API).

Thanks to [The Blue Alliance](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/) for an overview of OPR and the math behind it.

Thanks to [this article](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/) for ideas on matrix calculation.

Printing in BASH with help from some people on [this StackOverflow post](https://stackoverflow.com/questions/1898712/make-sure-int-variable-is-2-digits-long-else-add-0-in-front-to-make-it-2-digits).

Python printing in colors (the `Colors` class in `commonresources.py`) was taken from [Rene-d](https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007).

The Google Sheets API was implemented with lots of help from [their sample program](https://github.com/googleapis/google-api-python-client/blob/main/samples/service_account/tasks.py) and [quickstart](https://developers.google.com/sheets/api/quickstart/python).

Thanks to viniciusarrud on GitHub in [this Joblib issue](https://github.com/joblib/joblib/issues/1496#issuecomment-1788968714) for a solution to a particular bug involving pathing on Windows.

The diagram `FTCAPI file diagram.drawio` (soon to be exported into an image and put in this doc) was generated using [Drawio](https://app.diagrams.net/) [24.7.7], made by JGraph, https://github.com/jgraph/drawio. \
I am not JGraph, this project is not by JGraph, and JGraph neither endorses me nor this project.

### External libraries

This software uses the following external libraries:

 - Google API Python Client Framework: Copyright Google APIs. Licensed under Apache 2.0 license, see LICENSES.apache for details. \
Website: https://github.com/googleapis/google-api-python-client?tab=readme-ov-file

 - Matplotlib Framework: Copyright (c)
2012- Matplotlib Development Team; All Rights Reserved. Licensed similar to the PSF license, see LICENSES.matplotlib for details. \
Website: https://matplotlib.org/stable/

 - Pandas Framework: Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team. Licensed under a BSD 3-Clause license, see LICENSES.pandas for details. \
Website: https://github.com/pandas-dev/pandas?tab=readme-ov-file




## More documentation goes here!
As always, this is a work in progress and has some bugs. Errors should be both printed to the terminal and appended to `app/generatedfiles/error.log` with a timestamp.

Good luck debugging!

<br><br>
All documentation and code is Copyright (c) 2024 Drew Wingfield unless otherwise mentioned. All rights reserved.
