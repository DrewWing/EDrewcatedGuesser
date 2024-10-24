# How to Set Up the Project

# <p style="color:orange"><u>**This Documentation is currently a WORK IN PROGRES**</u></p>

## Setting Up
Please note that this software needs to be set up correctly to work.

### Venv
First of all, you must set up a Virtual Environment and install the required packages. The script `venvSetup.ps1` automatically does this for you.

> *Advanced*: You may change the location of the Virtual Environment with the `VenvName` flag.


### Secrets
#### Basic
You will need to get an API token from FIRST.
Go to [this website](https://ftc-events.firstinspires.org/services/API) and click `Register for API Access`. Fill out the form, and you should recieve a token in your email.


Create a file called `secrets.txt` containing your FIRST API token. Format it as follows:
```
PersonalAccessToken=YOUR_TOKEN_GOES_HERE
```

> *Advanced*: Any variables in `secrets.txt` will be written into `ftcapi.ps1`, <u>after argument parsing</u> (will override arguments). 
> This is a great way to semi-permanently set some arguments without passing them into the script every time. 

### Common Resources
Certain variables in commonresources.py need to be set up correctly;
 - `SERVICE_ACCOUNT_FILE` (string) is the path to the .json file where your service account authentication key is stored.

 - `SPREADSHEET_ID` (string) is the ID of the google spreadsheet you want to push data to, found in the URL of the spreadsheet; https://docs.google.com/spreadsheets/d/spreadsheet_id_goes_here/edit. Ex: `1MoOvAGpCF_dbo-verZvakOPCE2XJQi5IMG24vWRL64o`
