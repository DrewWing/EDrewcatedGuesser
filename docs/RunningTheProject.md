# How to Run the Project


> [!Tip]
> It is recommended to `cd` into the project folder before running scripts.


## Running the Main Program
To run the main program, call `__main__.py` while the virtual environment is activated. The workflow should look something similar to this:

```powershell
$ .\.venv\Scripts\activate # Activate the virtual environment.
$ python3 .\app\__main__.py # Run the main script.
```

The program will initialize, gather some data, then run cycles until it is stopped (unless `ONE_CYCLE_ONLY` is `True`), as seen in the below flowcharts:


<table>
    <tr>
        <td> <img src="images/Flowchart_Main_Overview.svg" /> </td>
        <td> <img src="images/Flowchart_Main_Cycle.svg" /> </td>
    </tr>
</table>
<br>

## Configuring the Program
<!-- TODO: Should this be put in it's own page? -->
The program may be configured using variables in the `.env` file. Other than those in the [setup instructions](Setup.md), the only recommended modification is of `SEASON_YEAR`.

### General Configuration Variables
| Variable Name | Default Value | Description |
| :------------ | :------------ | :---------- |
| `SEASON_YEAR` | 2023          | A string or integer describing the first year of the season. For instance, the 2023-2024 season is "`2023`." |
| `EVENT_CODE`  | FTCCMP1FRAN   | The alphanumeric event code FIRST uses to keep track of their events, as a string. |
| `CALCULATION_MODE` | AUTO     | Controls which types of calculations are run and when. See [Stats Calculation](StatsCalculation.md) for more details.


### `__main__`-Specific Configuration Variables
| Variable Name | Default Value | Description |
| :------------ | :------------ | :---------- |
| `DELAY_SECONDS` | 120 | Positive integer. Seconds to wait between each cycle. Does not include the time taken for the cycle itself. |
| `ONE_CYCLE_ONLY` | False | Boolean. If True, `__main__.py` performs one cycle then exits. |


### API Configuration Variables
| Variable Name | Default Value | Description |
| :----------------------- | :----- | :---------- |
| `DISABLE_API_CALLS`      | False  | If True, disables all FIRST API and Google Sheets API calls. |
|`DISABLE_GOOGLE_API_CALLS`| False  | If True, disables all Google Sheets API calls. |
| `DISABLE_FTC_API_CALLS`  | False  | If True, disables all FIRST API calls. |
| `GOOGLE_SPREADSHEET_ID` | \<placeholder Google Sheets Spreadsheet ID\> | The Google Sheets spreadsheet ID. |
| `PERSONAL_ACCESS_TOKEN` | \<placeholder personal access token\> | Your FIRST API access token. |
| `SERVICE_ACCOUNT_KEY_PATH` | PROJECT_PATH/ServiceAccountKey.json | The path to your Google Cloud Service Worker account key. |


### Advanced/Debug Configuration Variables
| Variable Name | Default Value | Description |
| :----------------------- | :----- | :---------- |
| `LOG_LEVEL`   | INFO          | The log level for logger to use. May be `DEBUG`, `INFO`, `WARN`, `ERROR`, or `CRITICAL`. |
| `DEBUG_LEVEL` | 0             | A positive integer starting at zero. Higher values print more info and make execution slightly slower. Only applicable if `LOG_LEVEL`=`DEBUG`. |
| `FLUSH_DEBUG_LOG` | True      | Boolean. If True, flushes the file `debug.log` on initialization. Otherwise, only appends to the file. **Caution:** may lead to very large debug files. |
| `DO_JOBLIB_MEMORY` | True     | If True, enables caching of heavy functions. In general, you should leave this on unless joblib starts to throw errors. |
| `PROJECT_PATH` | *(autodetected)* | The absolute path to the project directory. You shouldn't need to use this. |
| `JOBLIB_PATH` | PROJECT_PATH/generatedfiles/joblibcache/joblib | The absolute path to the joblib cache, as a string. You shouldn't need to change this. |
| `DRY_RUN` | False | Boolean. If true, `__main__.py` does no operations, and just prints info. |


## Training Your Own Algorithm
Training your own algorithm is not officially supported at this time and will be addressed in a future update.

