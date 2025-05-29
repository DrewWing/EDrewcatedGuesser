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
Each season's data is separated into separate directories by season year (ex: `generatedfiles/2024`, `generatedfiles/2023`, etc.). \
The `eventdata` folder contains only <u>raw</u> data from the FIRST API.
  - `event_matches.json`, `event_rankings.json`, `eventschedule_qual.json`, `eventschedule_playoff.json`, and `event_teams.json` are all queries of the CURRENT event with code `EVENT_CODE`.
  - `event_rankings.csv` is a processed file, but no data is really changed. It's just the .csv version of `event_rankings.json`, created by the `rankings_dataframe` func (in `json_parse`) called by the `push_rankings` func in `sheets_api`.


Now, for the interesting stuff:
`team_list_filtered.csv` 


Places that OPR results are stored:
`opr_result_sorted.csv` - Season-long data for the teams in the event.
`opr_global_result_sorted.csv` - Season-long, all-teams data. No restrictions, all events used.
`opr_recent_result_sorted.csv` - Recent (last 30 days) stats for teams in current event.
`opr_event_result_sorted.csv` - Event-only matches

## Process
(TODO) put text here describing the process of calculating statistics. Perhaps add a diagram.

