# How to Set Up the Project

# <p style="color:red"><u>**This Documentation is currently OUTDATED**</u></p>

## Setting Up
Please note that this software needs to be set up correctly to work. This should be configured automatically by `ftcapi.ps1` or `ftcapi.sh`.

### Common Resources
Certain variables in commonresources.py need to be set up correctly;
 - `EVENTCODE` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`

 - `SERVICE_ACCOUNT_FILE` (string) is the path to the .json file where your service account authentication key is stored.

 - `SPREADSHEET_ID` (string) is the ID of the google spreadsheet you want to push data to, found in the URL of the spreadsheet; https://docs.google.com/spreadsheets/d/spreadsheet_id_goes_here/edit. Ex: `1MoOvAGpCF_dbo-verZvakOPCE2XJQi5IMG24vWRL64o`


### The FTCAPI BASH Program
In ftcapi.sh there are several necessary variables to configure;
 - `authorizationheader` (string) should be set to your authorization token for the FTC API. Ex: `"Authorization: Basic <your_token_goes_here>"`

 - `pathtoftcapi` should be similarly configured as in commonresources.py, except **without the trailing forwardslash.** Ex: `/home/wingfield/ftcapi-branch44-1`

 - `eventcode` (string) is configured before each event. It is the alphanumeric code that FTC uses to track their events. Ex: `USTXCMPTESL`