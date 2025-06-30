# How to Set Up the Project

<!-- Copyright (C) 2024, Drew Wingfield

This document is part of EDrewcated Guesser by Drew Wingfield, found at https://github.com/DrewWing/EDrewcatedGuesser.
EDrewcated Guesser is free software: you can redistribute it and/or modify it under 
the terms of the AGNU Affero General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later version.

EDrewcated Guesser is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the AGNU Affero General Public License for more details.

You should have received a copy of the AGNU Affero General Public License along with 
EDrewcated Guesser. If not, see <https://www.gnu.org/licenses/>.

See the documentation in the README.md file. -->

> [!Tip]
> It is recommended to `cd` into the project folder before running scripts.

## Setting Up
Please note that this software needs to be set up correctly to work. If any of the steps are followed incorrectly, this software may fail. If you run into any trouble, see the [FAQs](FAQs.md) and the [Troubleshooting section](#Troubleshooting) below.

- - -
<br>

### Venv
First of all, you must set up a Virtual Environment and install the required packages. If you are running Windows, the script `venvSetup.ps1` will automatically do this for you.

- - -
<br>

### Creating the `.env` File
Copy `.env.template` into a new file called `.env`. This is where you will set the project configuration variables. Each variable is explained in the [running the project](RunningTheProject.md) page.


#### FIRST API Token
You will need to get an API token from FIRST.
Go to [their website](https://ftc-events.firstinspires.org/services/API) and click `Register for API Access`. Fill out the form, and you should recieve a token in your email.

Replace `YOUR_PERSONAL_ACCESS_TOKEN_HERE` with that token in the `.env` file.

- - - 
<br>


### Google Sheets
Now is the time to make a decision. You can either
 1) Set up the project to push its data to a Google Sheets spreadsheet. This requires creating a Google Cloud Service Worker using [these instructions](SetupGoogleSheets.md). Or, you could
 2) Set up the project to **not** push its data anywhere. You do this by setting `DISABLE_GOOGLE_API_CALLS=True` in the `.env` file you created.

In the very near future, an option will be available to have a **local** spreadsheet (similar to the Google Sheets but without the Google Cloud mess, running locally on your computer). For now, you most likely want to choose option 1. I apologize in advance, it's kind of a pain.

- - -
<br>

## Run the program
By this point, the project should be correctly set up. For instructions on how to use the software, go to [running the project](RunningTheProject.md).


## Extra Info

You may look at [Stats Calculation](StatsCalculation.md) for more info on how statistics are calculated and what the `CALCULATION_MODE` configuration variable does.
