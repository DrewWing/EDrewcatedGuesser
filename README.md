# EDrewcated Guesser V48.0 (Alpha)
## by Drew Wingfield

You may **not** earn money or monetize in any way from this program. It's not just my terms, it's also a part of the terms of using the official FTC API.

**NOTE** that this is an alpha version still in "stealth," so please ignore any other references to licensing, in code or on any documentation, except this paragraph. I'll get all that ironed out before I release this.  \
All versions of this software (and all of their code, documentation, assets, and any other intellectual property they contain) before publication (TODO: insert range of versions here) are hereby licensed under the first published version (TODO: state here). The current version of this software is **unpublished**.

I'm doing my best but am not a lawyer, please just use the latest published version under its own license.

You can find the license [here](LICENSE.txt).
The todo list is [here](docs/todos.md).
Also see the [Updates](docs/Updates.md) page.


---
## Language Stats:
<img src="./languages.png" alt="A graph describing the current language composition." width="512"/> 
<!-- Created by linecounter.py -->
<br>


## Helpful Documentation Links
 - [How to Set Up the Project (Start Here!)](docs/Setup.md)
 - [Running the program](docs/RunningTheProject.md)
   - During an event
   - Outside of an event
 - [Machine Learning Guide (advanced)](docs/MachineLearningGuide.md)


## Contributing
Add some text here mentioning conventions, PR templates, etc etc. TODO.


## More documentation goes here!
As always, this is a work in progress and has some bugs. Errors should be both printed to the terminal and appended to `app/generatedfiles/error.log` with a timestamp.

Good luck debugging!


## Credits/Honorable Mentions
Though I wrote almost the entirety of the project by myself, I had some help. Below are some resources that I used (whether for copypasting code, general reference, or other research).

This program uses the official FIRST Tech Challenge API to get information on matches, schedules, and scores.
You can find it [here](https://ftc-events.firstinspires.org/services/API).

Thanks to [The Blue Alliance](https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/) for an overview of OPR and the math behind it.

Thanks to [this article](https://www.johndcook.com/blog/2010/01/19/dont-invert-that-matrix/) for ideas on matrix calculation.

Printing in BASH with help from some people on [this StackOverflow post](https://stackoverflow.com/questions/1898712/make-sure-int-variable-is-2-digits-long-else-add-0-in-front-to-make-it-2-digits).

Python printing in colors (the `Colors` class in `commonresources.py`) was taken from [Rene-d](https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007).

The Google Sheets API was implemented with lots of help from [their sample program](https://github.com/googleapis/google-api-python-client/blob/main/samples/service_account/tasks.py) and [quickstart](https://developers.google.com/sheets/api/quickstart/python).

Thanks to viniciusarrud on GitHub in [this Joblib issue](https://github.com/joblib/joblib/issues/1496#issuecomment-1788968714) for a solution to a particular bug involving pathing on Windows.

The diagram `FTCAPI file diagram.drawio` (soon to be exported into an image and put in the docs) was generated using [Drawio](https://app.diagrams.net/) [24.7.7], made by JGraph, https://github.com/jgraph/drawio. \
I am not JGraph, this project is not by JGraph, and JGraph neither endorses me nor this project.

### External libraries

This software uses the following external libraries:

 - Google API Python Client Framework: Copyright Google APIs. Licensed under Apache 2.0 license, see [LICENSES/APACHE2.txt](LICENSES/APACHE2.txt) for details. \
Website: https://github.com/googleapis/google-api-python-client

 - Matplotlib Framework: Copyright (c)
2012- Matplotlib Development Team; All Rights Reserved. Licensed similar to the PSF license, see [LICENSES/MATPLOTLIB.txt](LICENSES/MATPLOTLIB.txt) for details. \
Website: https://matplotlib.org/stable/

 - Pandas Framework: Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team. Licensed under a BSD 3-Clause license, see [LICENSES/PANDAS.txt](LICENSES/PANDAS.txt) for details. \
Website: https://github.com/pandas-dev/pandas

 - Scikit-Learn Framework: Copyright (c) 2011, Pedregosa et al. Licensed under a BSD 3-Clause license, see [LICENSES/SCIKIT-LEARN.txt](LICENSES/SCIKIT-LEARN.txt) for details. \
Website: https://github.com/scikit-learn/scikit-learn

 - PyArrow Framework: Copyright (c) 2024, Richardson N, Cook I, Crane N, Dunnington D, François R, Keane J, Moldovan-Grünfeld D, Ooms J, Wujciak-Jens J, Apache Arrow (2024). arrow: Integration to 'Apache' 'Arrow'. Licensed under Apache 2.0 license, see [LICENSES/APACHE2.txt](LICENSES/APACHE2.txt) for details. \
Websites: https://github.com/apache/arrow/, https://arrow.apache.org/docs/r/.


### EDrewcated Guesser License
<img src="Docs/images/agplv3-with-text-162x68.png" alt="AGPL3 logo, Free as in Freedom." width="100"/> 

Copyright (C) 2024, Drew Wingfield

EDrewcated Guesser is licenced under the GNU Affero General Public License 
as published by the Free Software Foundation, version 3.

EDrewcated Guesser is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

EDrewcated Guesser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program (in the COPPYING file). If not, see https://www.gnu.org/licenses/.