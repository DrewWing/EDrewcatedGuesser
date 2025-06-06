# Stats Calculation

<!-- Copyright (C) 2025, Drew Wingfield

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

Documentation on how statistics (OPR, AutoOPR, CCWM, etc.) calculation works, so I'm not forced
to reverse-engineer my old code every time I make changes.

> [!Warning]
> This document is a draft and may contain incorrect, incomplete, or outdated information.

## Files and Directories
Each season's data is separated into separate directories by season year (ex: `generatedfiles/2024`, `generatedfiles/2023`, etc.).
It's assumed in the rest of this document that all files and directories are within the current season year directory.

### Eventdata
The `eventdata` folder contains only <u>raw</u> data from the FIRST API.
  - `event_matches.json`, `event_rankings.json`, `eventschedule_qual.json`, `eventschedule_playoff.json`, and `event_teams.json` are all queries of the CURRENT event with code `EVENT_CODE`.
  - `event_rankings.csv` is a processed file, but no data is really changed. It's just the .csv version of `event_rankings.json`, created by the `rankings_dataframe` func (in `json_parse`) called by the `push_rankings` func in `sheets_api`.

<br>

### Team List Filtered
The file `team_list_filtered.csv` file is <u>generated</u> by the `prepare_opr_calculation` function in `json_parse.py`.
The content of this file is simply the team numbers of all unique teams in the matches filtered by the function.

<br>

### Results
Places that OPR results are stored:
`opr_result_sorted.csv` - Season-long data for the teams in the event. \
`opr_global_result_sorted.csv` - Season-long, all-teams data. No restrictions, all events used. \
`opr_recent_result_sorted.csv` - Recent (last 30 days) stats for teams in current event. \
`opr_event_result_sorted.csv` - Event-only matches


## Stats Calculation Terms:
The following table describes the types of statistics we can calculate. Each type calculates OPR, AutoOPR, and CCWM for their given filters, and is fed into the ML algorithm for accurate match outcome prediction.
| Name                 | Date Range                                                 | Teams                                                   | Output file |
| :------------------  | :--------------------------------------------------------- | :------------------------------------------------------ | :---------- |
| UniversalSeasonStats | All-Season                                                 | **All** active teams in the world. **No** restrictions. | `opr_global_result_sorted.csv` |
| RegularSeasonStats   | All-Season                                                 | Only teams in current event.                            | `opr_result_sorted.csv` |
| RecentStats          | The last `NUMBER_OF_DAYS_FOR_RECENT_OPR` (default 30) days | Only teams in current event.                            | `opr_recent_result_sorted.csv` |
| EventStats           | Current event only.                                        | Only teams in current event.                            | `opr_event_result_sorted.csv` |



## Process

1. `__main__.py` calls `master_function` in `OPR.py`.
2. `master_function`:
   1. Cache heavy functions (`calculate_opr`, `build_m`, `build_scores`, and `create_and_sort_stats`).
   2. Calculate the time since global calculations were last run.
   3. For each type of calculation (UniversalSeasonStats, RegularSeasonStats, RecentStats, EventStats):
      1. Check the conditions to run the calculation type. If fail, skip to next calculation type.
      2. Call `json_parse.prepare_opr_calculation` with appropriate arguments to filter teams and matches (based on calculation type)
         1. Load all events in opr/all_events (raw FIRST API data), unless specific_event != None.
         2. Gather all matches from all loaded events.
         3. Filter matches by teams.
         4. Organize dictionary of matches per team.
         5. Save all teams involved in matches to `team_list_filtered.csv`.
         6. Save all matches to `all_matches.csv`.
      3. Load teams from `loadTeamNumbers` function (list of team numbers from `team_list_filtered.csv`).
      4. Load matches using `loadMatches` function (Pandas object from `all_matches.csv`).
      5. Calculate and save statistics to appropriate file using `do_all_opr_stuff` function.
            > [!Note]
            > The matrices form the pattern `Mx = s`, with `M` being the sparse matrix of team participation,
            `x` being the statistics (`OPR`), and `s` being the scores[^1].
         1. Build the `M` matrix using the `build_m` function (sparse matrix of ones and zeroes).
         2. Build the scores (`s`) matrices using the `build_scores` function.
         3. Calculate the statistics (`OPR`, `AUTOOPR`, `CCWM`, aka `x` in the equation) using the `calculate_opr` function.
            1. For each statistics type, use the numpy's linear algebra library to solve the least squares solution.
         4. If any statistics are of size `0`, replace the stats with a matrix of zeroes of the appropriate size.
         5. Round statistics matrices to 14 places.
         6. Combine and sort the statistics into one pandas dataframe using the function `create_and_sort_stats`.
         7. Save the aggregated statistics to the correct .csv file.
      6. If applicable, save the current timestamp to a file.


<!-- Note: VS Code doesn't like Markdown footnotes for some reason. They should work in 
most other viewers, including GitHub. -->
[^1]: See https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/
