#
# -*- coding: utf-8 -*-
# jsonparse
# by Drew Wingfield
# started 2024-01-29
# (c) 2024 Drew Wingfield, All Rights Reserved

# This was initially started as a program to parse json data, but now mostly serves as another library
# of functions, the most used being preparing for OPR calculation.
# Make sure to read the README.txt and the LICENSE.txt



#region Imports
import sys
import os

from common_resources import log_error, green_check, info_i, red_x, get_json, PATH_TO_FTCAPI, accepted_match_types

from python_settings import PythonSettings
settings = PythonSettings()


try:
    import pandas as pd

except ImportError as e:
    log_error('[jsonparse.py][imports] ImportError while importing pandas. Are you using a virtual environment with pandas installed?')
    print('\n\n[jsonparse.py][imports] !!! ERROR !!!\n  Something went wrong during importing pandas. Are you using the correct venv?\n\n')
    raise e

#endregion Imports


def get_team_stats(team_number) -> dict:
    """ 
    Returns a dictionary containing the stats of the team. 
    Uses: 
      - opr/opr-recent-result-sorted.csv
      - opr/opr-result-sorted.csv 
    """
    team_stats = {}
    if settings.debug_level>1:
        print(info_i()+f'         [jsonparse.py][get_team_stats] Getting team stats for team #{team_number}')
    
    all_oprs = pd.read_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','opr-result-sorted.csv'), index_col=False)

    try:
        team_stats['OPR']     = all_oprs[all_oprs["Team"]==team_number]['OPR'].values[0]
        team_stats['AutoOPR'] = all_oprs.loc[all_oprs["Team"]==team_number]['AutoOPR'].values[0]
        team_stats['CCWM']    = all_oprs.loc[all_oprs["Team"]==team_number]['CCWM'].values[0]
    
    except IndexError as e:
        #log_error(f'[jsonparse.py][get_team_stats] IndexError. team_number={team_number}, all_oprs["Team"]={all_oprs["Team"]} all_oprs={all_oprs}, additional info:{e}')
        #try:
        #    log_error(f'[jsonparse.py][get_team_stats] all_oprs.loc[all_oprs["Team"]==team_number]={all_oprs.loc[all_oprs["Team"]==team_number]}')
        #except:
        #    pass
        #print(red_x()+' Index error! See the error log for more details.')
        #raise e
        team_stats['OPR']     = 1
        team_stats['AutoOPR'] = 1
        team_stats['CCWM']    = 1
    #Team,OPR,AutoOPR,CCWM

    all_oprs_recent = pd.read_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','opr-recent-result-sorted.csv'), index_col=False)

    try:
        team_stats['recentOPR']     = all_oprs_recent.loc[all_oprs_recent["Team"]==team_number]['OPR'].values[0]
        team_stats['recentAutoOPR'] = all_oprs_recent.loc[all_oprs_recent["Team"]==team_number]['AutoOPR'].values[0]
        team_stats['recentCCWM']    = all_oprs_recent.loc[all_oprs_recent["Team"]==team_number]['CCWM'].values[0]
    
    except IndexError:
        team_stats['recentOPR']     = 1
        team_stats['recentAutoOPR'] = 1
        team_stats['recentCCWM']    = 1
    
    return team_stats


#region classes
"""
{
  "matches": [
    {
      "actualStartTime": "2024-02-06T01:42:57.183Z",
      "description": "string",
      "tournamentLevel": "string",
      "series": 0,
      "matchNumber": 0,
      "scoreRedFinal": 0,
      "scoreRedFoul": 0,
      "scoreRedAuto": 0,
      "scoreBlueFinal": 0,
      "scoreBlueFoul": 0,
      "scoreBlueAuto": 0,
      "postResultTime": "2024-02-06T01:42:57.183Z",
      "teams": [
        {
          "teamNumber": 0,
          "station": "string",
          "dq": true,
          "onField": true
        }
      ],
      "modifiedOn": "2024-02-06T01:42:57.183Z"
    }
  ]
}
"""

# somehow this is still used in sheetsapi.py, though I should remove it sometime
class EventMatches():
    def __init__(self, raw_json):
        """
        Event.
        """
        self.raw_json = raw_json
        self.matches  = raw_json['matches']
        self.number_of_matches = len(raw_json['matches'])

        self.matches_split = []

        for match in raw_json['matches']:
            try:

                teamsdic = {'Red1':1,'Red2':1,'Blue1':1,'Blue2':1}

                for i in match['teams']:
                    teamsdic[i['station']] = i['teamNumber']
                    
                
                appendlist = [
                    match['tournamentLevel'],
                    match['scoreRedFinal'],
                    match['scoreRedFoul'],
                    match['scoreRedAuto'],
                    match['scoreBlueFinal'],
                    match['scoreBlueFoul'],
                    match['scoreBlueAuto'],
                    # rearranging so it's Red1 Red2 Blue1 Blue2
                    teamsdic['Red1'],
                    teamsdic['Red2'],
                    teamsdic['Blue1'],
                    teamsdic['Blue2'],
                        ]
                
                self.matches_split.append(appendlist)
            except IndexError as e:
                log_error(f'[jsonparse.py][EventMatches][__init__] An index error occured. Teams {match['teams']}')
                log_error(f'    touornamentLevel: {match['tournamentLevel']}')
                log_error(f'    actualStartTime: {match['actualStartTime']}')
                log_error(f'    Error info: {e}')
                print(red_x()+'\n\n  An index error was detected! Some useful info:')
                print(red_x()+'    Teams:'+str(match['teams']))
                print(red_x()+'    tournamentLevel:'+str(match['tournamentLevel']))
                print(red_x()+'    actualStartTime:'+str(match['actualStartTime']))
                print('\n\n')
                raise e


    def __str__(self) -> str:
        return f"<EventMatches class with {self.number_of_matches} matches>"
    
    def make_dataframe(self) -> pd.DataFrame:
        
        if settings.debug_level>1:
            print(info_i()+'         [jsonparse.py][EventMatches][make_dataframe] Making the dataframe with proper format (for the predictors)')
        # we need a dataframe with columns
        #redOPR,redAutoOPR,redCCWM,blueOPR,blueAutoOPR,blueCCWM,recentredOPR,recentredAutoOPR,recentredCCWM,recentblueOPR,recentblueAutoOPR,recentblueCCWM
        # and each of the matches as rows.
        dic_thing = {
            'redOPR':[],'redAutoOPR':[],'redCCWM':[],
            'blueOPR':[],'blueAutoOPR':[],'blueCCWM':[], 
            'recentredOPR':[],'recentredAutoOPR':[],'recentredCCWM':[], 
            'recentblueOPR':[], 'recentblueAutoOPR':[], 'recentblueCCWM':[]
        }
        
        for match in self.matches_split:
            red1  = get_team_stats(match[7])
            red2  = get_team_stats(match[8])
            blue1 = get_team_stats(match[9])
            blue2 = get_team_stats(match[10])

            dic_thing['redOPR'].append(     red1['OPR']  + red2['OPR'])
            dic_thing['redAutoOPR'].append( red1['AutoOPR'] + red2['AutoOPR'])
            dic_thing['redCCWM'].append(    red1['CCWM'] + red2['CCWM'])
            dic_thing['recentredOPR'].append(     red1['recentOPR']  + red2['recentOPR'])
            dic_thing['recentredAutoOPR'].append( red1['AutoOPR'] + red2['recentAutoOPR'])
            dic_thing['recentredCCWM'].append(    red1['recentCCWM'] + red2['recentCCWM'])

            dic_thing['blueOPR'].append(     blue1['OPR']  + blue2['OPR'])
            dic_thing['blueAutoOPR'].append( blue1['AutoOPR'] + blue2['AutoOPR'])
            dic_thing['blueCCWM'].append(    blue1['CCWM'] + blue2['CCWM'])
            dic_thing['recentblueOPR'].append(     blue1['recentOPR']  + blue2['recentOPR'])
            dic_thing['recentblueAutoOPR'].append( blue1['AutoOPR'] + blue2['recentAutoOPR'])
            dic_thing['recentblueCCWM'].append(    blue1['recentCCWM'] + blue2['recentCCWM'])
        
        return pd.DataFrame(dic_thing)

    def predict_outcomes(self, predictors: list, inplace: bool) -> list:
        """
        Using a given list of predictors, predicts the outcomes of matches.
        If inplace is false, returns just the predictions.
        Otherwise, appends the predictions to self.matches_split
        """

        # Matchdata needs to be some kind of dataframe containing all matches in the given EventMatches object, 
        # and their respective calculated OPR, CCWM, AutoOPR, recentOPR, recentCCWM, and recentAutoOPR for each team
        if settings.debug_level>1:
            print(info_i()+'     [jsonparse.py][EventMatches][predict_outcomes] Predicting outcomes of matches for this EventMatches object.')
        
        matchdata = self.make_dataframe() # TODO: create a dataframe out of the matches
        # Somehow get the input matches, then calculate the "input data" for the predictor
        # for each of the matches, then transform it, then precit it and return the predictions.
        #[['redOPR','redAutoOPR','redCCWM','blueOPR','blueAutoOPR','blueCCWM', 'recentredOPR','recentredAutoOPR','recentredCCWM', 'recentblueOPR', 'recentblueAutoOPR', 'recentblueCCWM']]
        

        if settings.debug_level>1:
            print(info_i()+'     [jsonparse.py][EventMatches][predict_outcomes] Match data formatted. Now doing the actual predictions')

        predictions_per_predictor = []

        # Actually predict the things
        for predictor in predictors:
            try:
                predictions_per_predictor.append(predictor.predict(matchdata))
            
            except ValueError as e:
                log_error('[jsonparse.py][EventMatches][predict_outcomes] Match data is probably empty. This is NORMAL if no matches have been played. Full error info:'+str(e), level='WARN')
                if settings.debug_level>0:
                    print(info_i()+' [jsonparse.py][EventMatches][predict_outcomes] Value error - This is NORMAL and fine if no matches played.')

        if settings.debug_level>1:
            print(info_i()+'     [jsonparse.py][EventMatches][predict_outcomes] Outcomes predicted. Returning results.')

        if inplace:
            index=0
            try:
                for index in range(0,len(predictions_per_predictor[0])):
                    for match_prediction_list in predictions_per_predictor:
                        self.matches_split[index].append(match_prediction_list[index])
                    index+=1
            
            except IndexError as e:
                log_error(f'[jsonparse.py][EventMatches][predict_outcomes] Index error. This is completely NORMAL if no matches have been played. {e}', level='WARN')
        
        else:
            # Return predictions in the match order
            return predictions_per_predictor



"""
{
  "schedule": [
    {
      "description": "string",
      "field": "string",
      "tournamentLevel": "string",
      "startTime": "2024-02-10T20:15:45.887Z",
      "series": 0,
      "matchNumber": 0,
      "teams": [
        {
          "teamNumber": 0,
          "displayTeamNumber": "string",
          "station": "string",
          "team": "string",
          "teamName": "string",
          "surrogate": true,
          "noShow": true
        }
      ],
      "modifiedOn": "2024-02-10T20:15:45.887Z"
    }
  ]
}
"""
class EventSchedule():
    def __init__(self, raw_json):
        """
        Event schedule.
        """
        self.raw_json = raw_json
        self.matches  = raw_json['schedule']
        self.number_of_matches = len(raw_json['schedule'])
        self.matches_split = []

        for match in raw_json['schedule']:
            try:
                teamsdic = {'Red1':1,'Red2':1,'Blue1':1,'Blue2':1}

                for i in match['teams']:
                    teamsdic[i['station']] = i
                    
                appendlist = [
                    match['tournamentLevel'],
                    None, # None in place of all scores
                    None,
                    None,
                    None,
                    None,
                    None,
                    # rearranging so it's Red1 Red2 Blue1 Blue2
                    teamsdic['Red1' ]['teamNumber'],
                    teamsdic['Red2' ]['teamNumber'],
                    teamsdic['Blue1']['teamNumber'],
                    teamsdic['Blue2']['teamNumber'],
                        ]
                
                self.matches_split.append(appendlist)
            except IndexError as e:
                print(red_x()+'\n\n  An index error was detected! Some useful info:')
                print(red_x()+'    Teams:'+str(match['teams']))
                print(red_x()+'    tournamentLevel:'+str(match['tournamentLevel']))
                print(red_x()+'    actualStartTime:'+str(match['actualStartTime']))
                print('\n\n')
                raise e

    def make_dataframe(self):
        
        if settings.debug_level>1:
            print(info_i()+'         [jsonparse.py][EventSchedule][make_dataframe] Making the dataframe with proper format (for the predictors)')
        # we need a dataframe with columns
        #redOPR,redAutoOPR,redCCWM,blueOPR,blueAutoOPR,blueCCWM,recentredOPR,recentredAutoOPR,recentredCCWM,recentblueOPR,recentblueAutoOPR,recentblueCCWM
        # and each of the matches as rows.
        dic_thing = {
            'redOPR':[],'redAutoOPR':[],'redCCWM':[],
            'blueOPR':[],'blueAutoOPR':[],'blueCCWM':[], 
            'recentredOPR':[],'recentredAutoOPR':[],'recentredCCWM':[], 
            'recentblueOPR':[], 'recentblueAutoOPR':[], 'recentblueCCWM':[]
        }
        counter = 0
        for match in self.matches_split:
            if settings.debug_level > 3:
                print(f'counter: {counter}') #TODO remove
                counter += 1

            red1  = get_team_stats(match[7])
            red2  = get_team_stats(match[8])
            blue1 = get_team_stats(match[9])
            blue2 = get_team_stats(match[10])

            dic_thing['redOPR'].append(     red1['OPR']  + red2['OPR'])
            dic_thing['redAutoOPR'].append( red1['AutoOPR'] + red2['AutoOPR'])
            dic_thing['redCCWM'].append(    red1['CCWM'] + red2['CCWM'])
            dic_thing['recentredOPR'].append(     red1['recentOPR']  + red2['recentOPR'])
            dic_thing['recentredAutoOPR'].append( red1['AutoOPR'] + red2['recentAutoOPR'])
            dic_thing['recentredCCWM'].append(    red1['recentCCWM'] + red2['recentCCWM'])

            dic_thing['blueOPR'].append(     blue1['OPR']  + blue2['OPR'])
            dic_thing['blueAutoOPR'].append( blue1['AutoOPR'] + blue2['AutoOPR'])
            dic_thing['blueCCWM'].append(    blue1['CCWM'] + blue2['CCWM'])
            dic_thing['recentblueOPR'].append(     blue1['recentOPR']  + blue2['recentOPR'])
            dic_thing['recentblueAutoOPR'].append( blue1['AutoOPR'] + blue2['recentAutoOPR'])
            dic_thing['recentblueCCWM'].append(    blue1['recentCCWM'] + blue2['recentCCWM'])

        if settings.debug_level>3:
            print(info_i()+' dic_thing:')
            print(pd.DataFrame(dic_thing))
        
        return pd.DataFrame(dic_thing)

    def predict_outcomes(self, predictors: list, inplace: bool, level: str=None) -> list:
        """
        Using a given list of predictors, predicts the outcomes of matches.
        If inplace is false, returns just the predictions.
        Otherwise, appends the predictions to self.matches_split
        If level is "playoff," the warning due to Value Errors logged to errors.log will be supressed.
        """

        # matchdata needs to be some kind of dataframe containing all matches in the given EventMatches object, and their respective calculated OPR, CCWM, AutoOPR, recentOPR, recentCCWM, and recentAutoOPR for each team
        if settings.debug_level>1:
            print(info_i()+'     [jsonparse.py][EventSchedule][predict_outcomes] Predicting outcomes of matches for this EventMatches object.')
        
        matchdata = self.make_dataframe()

        if settings.debug_level>1:
            print(info_i()+'     [jsonparse.py][EventSchedule][predict_outcomes] Match data formatted. Now doing the actual predictions')

        predictions_per_predictor = []

        # Actually predict the things
        for predictor in predictors:
            try:
                predictions_per_predictor.append(predictor.predict(matchdata))

            except ValueError as e:
                if level!='playoff':
                    log_error('[jsonparse.py][EventSchedule][predict_outcomes] ValueError - Match data is probably empty. This is normal if no matches have been played. Full error info:'+str(e), level='WARN')
                    if settings.debug_level>0:
                        print(info_i()+' [jsonparse.py][EventSchedule][predict_outcomes] Value error - This is normal and fine if no matches played.')

        if settings.debug_level>1:
            print(info_i()+'     [jsonparse.py][EventSchedule][predict_outcomes] Outcomes predicted. Returning results.')

        if inplace:
            index=0
            try:
                for index in range(0,len(predictions_per_predictor[0])):
                    for match_prediction_list in predictions_per_predictor:
                        self.matches_split[index].append(match_prediction_list[index])
                    index+=1
            
            except IndexError as e:
                if level!='playoff':
                    log_error(f'[jsonparse.py][EventSchedule][predict_outcomes] Index error. This is completely normal if no matches have been played. {e}', level='WARN')
        
        else:
            # return predictions in the match order
            return predictions_per_predictor




#Season Events
"""
{
  "events": [
    {
      "eventId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "code": "string",
      "divisionCode": "string",
      "name": "string",
      "remote": true,
      "hybrid": true,
      "fieldCount": 0,
      "published": true,
      "type": "string",
      "typeName": "string",
      "regionCode": "string",
      "leagueCode": "string",
      "districtCode": "string",
      "venue": "string",
      "address": "string",
      "city": "string",
      "stateprov": "string",
      "country": "string",
      "website": "string",
      "liveStreamUrl": "string",
      "coordinates": {
        <stuff>
      "webcasts": [
        "string"
      ],
      "timezone": "string",
      "dateStart": "2024-02-08T16:20:08.012Z",
      "dateEnd": "2024-02-08T16:20:08.012Z"
    }
  ],
  "eventCount": 0
}
"""
class SeasonEvents():
    def __init__(self, raw_json):
        """
        SeasonEvents.
        """
        self.raw_json   = raw_json
        self.eventcount = raw_json['eventCount']

        self.events_split = []
        self.events_list  = raw_json['events']
        
        for event in raw_json['events']:
            self.events_split.append(
                [
                    event['eventId'],
                    event['code'],
                    event['divisionCode'],
                    event['name'],
                    event['remote'],
                    event['hybrid'],
                    event['type'],
                    event['typeName'],
                    event['regionCode'],
                    event['leagueCode'],
                    event['districtCode'],
                    event['venue'],
                    event['city'],
                    event['stateprov'],
                    event['country'],
                    event['website'],
                    event['timezone'],
                    event['dateStart'],
                    event['dateEnd'],
                ]
            )

    def filter(self, region=None,type=[], nottype=[], state=None) -> list:
        """
        Returns a list of non-remote events in the raw json filtered by stuff 
        """
        #print(info_i()+' parameters: region={}   type={}   nottype={}   state={}'.format(region,type,nottype,state))
        rtn = []
        for event in self.raw_json['events']:
            # debug info
            #print('\n\n'+info_i()+'      '+event['regionCode'])
            #print(info_i()+str(event))
            #print(info_i()+' eventcode: '+str(event['code']))
            #print(info_i()+'      If statements: region {}, type {}, nottype {}, state {}, remote {}'.format(
            #    ((region==None) or (event['regionCode'].lower()==region.lower()) ),
            #    ((len(type)==0) or (event['typeName'] in type) ),
            #    ((len(nottype)==0) or (event['typeName'] not in nottype) ),
            #    ((state==None) or (event['stateprov']==state) ),
            #    (True != event['remote'])
            #))
            #exit()
            if (
                #all types: ['Qualifier', 'Championship', 'Scrimmage', 'Kickoff', 'League Tournament', 'League Meet', 'Super Qualifier', 'Volunteer Signup', 'Practice Day', 'Workshop', 'FIRST Championship', 'Demo / Exhibition', 'Off-Season']
                ((region==None) or (event['regionCode'].lower()==region.lower()) ) and
                ((len(type)==0) or (event['typeName'] in type) ) and
                ((len(nottype)==0) or (event['typeName'] not in nottype) ) and
                ((state==None) or (event['stateprov']==state) ) and
                (True != event['remote'])
            ):
                rtn.append(event)

            
        return rtn




#season
"""
{
  "eventCount": 0,
  "gameName": "string",
  "kickoff": "2024-02-08T16:15:25.517Z",
  "rookieStart": 0,
  "teamCount": 0,
  "frcChampionships": [
    {
      "name": "string",
      "startDate": "2024-02-08T16:15:25.517Z",
      "location": "string"
    }
  ]
}
"""

class Season():
    def __init__(self, raw_json):
        """
        Season.
        """
        self.raw_json   = raw_json
        self.eventcount = raw_json['eventCount']
        self.gamename   = raw_json['gameName']
        self.teamcount  = raw_json['teamCount']
        

        self.championships_split = []

        for champ in raw_json['fRCChampionships']:
            self.championships_split.append(
                [
                    champ['name'],
                    champ['startDate'],
                    champ['location']
                ]
            )
#endregion classes


"""
{
  "Rankings": [
    {
      "rank": 0,
      "teamNumber": 0,
      "displayTeamNumber": "string",
      "teamName": "string",
      "sortOrder1": 0,
      "sortOrder2": 0,
      "sortOrder3": 0,
      "sortOrder4": 0,
      "sortOrder5": 0,
      "sortOrder6": 0,
      "wins": 0,
      "losses": 0,
      "ties": 0,
      "qualAverage": 0,
      "dq": 0,
      "matchesPlayed": 0,
      "matchesCounted": 0
    }
  ]
}
"""
def rankings_dataframe(json_filepath: str, csv_filepath: str):
    """
    returns a pandas dataframe containing the rankings
    based on the given filepath json file.
    """
    try:
        ranking_json = get_json(json_filepath)
    
    except Exception as e:
        ranking_json = {'rankings':[]}

    try:
        ranking_pd = pd.DataFrame(ranking_json['rankings'])

    except IndexError as e:
        log_error('[jsonparse.py][rankings_dataframe] IndexError parsing ranking_json in rankings_dataframe. Incorrect/malformed json. Full error message: '+str(e))
        print('\n\n !!!!! ERROR parsing ranking_json in rankings_dataframe (jsonpare.py). Incorrect json. !!!!!\n\n')
        raise e

    
    ranking_pd.to_csv(csv_filepath, index=False)




def write_needed_events(season_events, texasonly=False):
    """
    Using a given SeasonEvents object, gathers all the
    event IDs (for non-remote events) and writes them to a file
    """
    print(info_i()+' Writing needed events...')
    # All types: ['Qualifier', 'Championship', 'Scrimmage', 'Kickoff', 'League Tournament', 'League Meet', 'Super Qualifier', 'Volunteer Signup', 'Practice Day', 'Workshop', 'FIRST Championship', 'Demo / Exhibition', 'Off-Season']

    rawevents = open(os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','needed-events-raw.json'),'w+')
    rawevents.truncate()
    rawevents.write('{"matches":[\n')
    
    with open(os.path.join(PATH_TO_FTCAPI+f'generatedfiles','opr','needed-event-ids.txt'),'w+') as thefile:
        thefile.truncate() # Clear the file
        filtered_event_list = season_events.filter(type=accepted_match_types, state=("TX" if texasonly else None))
        # Iterate over every event
        for event in filtered_event_list:
            # If it's not remote and it's an accepted type
            thefile.write(str(event['code'])+'\n') #write to the file
            rawevents.write(str(event).replace("'",'"').replace('False','false').replace('True','true').replace('None','null')+', \n')

    rawevents.write(']}')
    #print('Done!')
    rawevents.close()




def write_needed_teams(use_opr=False):
    """
    Gathers all the team IDs from ftcapi/all-events
    and writes them to a file for later processing
    """
    allteams = []
    counter  = 0
    eventcounter = 0
    if (not use_opr):
        thepath = os.path.join(PATH_TO_FTCAPI,'generatedfiles','all-events')
    else:
        thepath = os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','all-events')
    
    l=len(os.listdir(thepath))

    print(info_i()+'    [write_needed_teams] Getting teams...')
    # Iterate through all match files
    for file in os.listdir(thepath):
        filename = os.fsdecode(file)

        eventcounter += 1

        print(green_check()+f'  Event {eventcounter}/{l} - {filename}',end='            \r')

        #open the file json & extract matches from the event
        a = get_json(thepath+'/'+filename)

        # Iterate over each match
        for match in a['matches']:
            counter += 1
            
            # Extract teams
            for team in match['teams']:
                #print('team '+str(team))
                if not (team['teamNumber'] in allteams):
                    allteams.append(team['teamNumber'])

    
    print(green_check()+'    Teams assembled. Writing all teams to file team-ids-to-get.txt...       ')
    
    with open(os.path.join(PATH_TO_FTCAPI,'generatedfiles',('opr','all-teamids-involved.txt' if use_opr else 'generatedfiles','team-ids-to-get.txt')),'w+') as thefile:
        thefile.truncate() # Clear the file
        for team in allteams:
            thefile.write(str(team)+'\n')

    print(green_check()+f'    Wrote {len(allteams)} teams for {counter} matches.')

    

def loadMatches(filter_by_teams=None) -> pd.DataFrame:
    """
    Returns a pandas object of the csv file containing all matches (reads from all-matches.csv, created by prepare_opr_calculation)
    """
    #TODO: update everything else that relies on this function's output to accomodate pandas
    all_matches = pd.read_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','all-matches.csv'))
    all_matches['actualStartTime'] = pd.to_datetime(all_matches['actualStartTime'], format='mixed')#format="%Y-%m-%"+"dT%H:%M:%S.%"+"f")

    # if filter_by_teams isn't none, filter the matches
    # by only the teams specified
    if filter_by_teams != None:
        all_matches = all_matches[
            all_matches['Red1'].isin(filter_by_teams) |
            all_matches['Red2'].isin(filter_by_teams) |
            all_matches['Blue1'].isin(filter_by_teams) |
            all_matches['Blue2'].isin(filter_by_teams)
        ]
    
    #print('All matches:')
    #print(all_matches)
    #print('\n\n')
    return all_matches



def prepare_opr_calculation(
    specific_event=None, specific_teams: list =None, specific_event_teams: str =None):
    """
    Prepares the OPR calculation and writes to all-matches.csv and matches-per-team.csv
    
    Draws from opr/all-events (created when curling in the BASH/Powershell script)
    
    Arguments:
      - specific_event (str) - returns only the data pertaining to the specified event code.
      - specific_teams (list) - filters all matches by the given teams
      - specific_event_teams (str) - returns data only for all teams in specified event code.
    """
    
    matchcounter  = 0
    eventcounter  = 0
    l=len(os.listdir(
        (
            os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','all-events'))
        ))

    matches_per_team_dic = {}
    all_matches_dic = {
        'actualStartTime':[],'description' :[],'tournamentLevel':[],
        'scoreRedFinal'  :[],'scoreRedAuto':[],'scoreBlueFinal' :[],'scoreBlueAuto':[],
        'Red1':[], 'Red2':[], 'Blue1':[], 'Blue2':[]}
    
    specific_event_teams_list = []


    if settings.debug_level>0:
        print(info_i()+' [jsonparse.py][prepare_opr_calculation] Starting to prepare opr calculation.')
        print(info_i()+'        specific_event='+str(specific_event))
        print(info_i()+'        specific_teams='+str(specific_teams))
        print(info_i()+'        specific_event_teams='+str(specific_event_teams))
        print(info_i()+'        settings.debug_level='+str(settings.debug_level))


    
    if specific_teams != None:
        specific_teams = [ str(i) for i in specific_teams]

    if settings.debug_level>0:
        print(info_i()+'    [prepare_opr_calculation] Getting teams...')
    
    if specific_event==None:
        path_list = [ os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','all-events', j) for j in [i for i in os.listdir(os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','all-events'))]]

    elif specific_event=='RECENT':
        if settings.debug_level>0:
            # eventmatches.json is updated in ftcapiv3.sh, during the getmatches
            print(info_i() + '    [prepare_opr_calculation] Iterating through only event in eventmatches.json')
        path_list = [os.path.join(PATH_TO_FTCAPI,'generatedfiles','eventdata','eventmatches.json')]
        l = 1
    
    else:
        if settings.debug_level>0:
            print(info_i() + '    [prepare_opr_calculation] Iterating through only one event with code '+str(specific_event))
        path_list = [os.path.join(PATH_TO_FTCAPI,'generatedfiles','opr','all-events',str(specific_event).upper()+'.json')]
        l = 1

    
    # Iterate through all events
    for eventfile in path_list:
        
        eventfilename = os.fsdecode(eventfile)

        eventcounter += 1

        if settings.debug_level>2:
            print(green_check()+f'    Event {eventcounter}/{l} - {eventfilename}',end='            \r')

        #open the file json & extract matches from the event
        event_raw_json = get_json(eventfilename)


        # Iterate over each match
        for match in event_raw_json['matches']:
            matchcounter += 1

            # do some opr stuff
            teamsdic = {'Red1':1,'Red2':1,'Blue1':1,'Blue2':1}

            for i in match['teams']:
                teamsdic[i['station']] = i['teamNumber']
            
            """
            red1, red2, redscore, redauto, blue1, blue2, bluescore, blueauto
            """
            # If the teams are in the valid list (or all teams are acceptable)
            if (
                (specific_teams==None) or 
                (str(teamsdic['Red1'])  in specific_teams) or
                (str(teamsdic['Red2'])  in specific_teams) or
                (str(teamsdic['Blue1']) in specific_teams) or
                (str(teamsdic['Blue2']) in specific_teams)
            ):
                # Add the match info to the all_matches_dic dictionary
                for i in ['actualStartTime','description','tournamentLevel', 'scoreRedAuto','scoreBlueAuto']:
                    all_matches_dic[i].append(match[i])

                all_matches_dic['scoreRedFinal'].append( match['scoreRedFinal'] -match['scoreBlueFoul'])
                all_matches_dic['scoreBlueFinal'].append(match['scoreBlueFinal']-match['scoreRedFoul'])
                # add the team numbers to the all_matches dictionary
                all_matches_dic['Red1' ].append(teamsdic['Red1'])
                all_matches_dic['Red2' ].append(teamsdic['Red2'])
                all_matches_dic['Blue1'].append(teamsdic['Blue1'])
                all_matches_dic['Blue2'].append(teamsdic['Blue2'])
            

            # Extract teams
            for team in match['teams']:
                # if team in specified teams (or no specified teams)
                if (specific_teams==None) or (str(team['teamNumber']) in specific_teams):
                    #print('team '+str(team))
                    # If team isn't already in the matches_per_team_dic
                    if not (team['teamNumber'] in matches_per_team_dic.keys()):
                        matches_per_team_dic[team['teamNumber']] = [match] # add the team

                    else:
                        matches_per_team_dic[team['teamNumber']].append(match)

    
    if (specific_event_teams != None):
        try:
            # If the current event is the specific event given, add all teams to list
            event_teams_raw_json = get_json(os.path.join(PATH_TO_FTCAPI,'generatedfiles','eventdata','eventteams.json')) # Created when FTC APIing

            #print('event_teams_raw_json[teams]'+str(event_teams_raw_json['teams']))
    
            # Iterate over each match and add teams to the list
            for team in event_teams_raw_json['teams']:

                #print(team['teamNumber'])
                if (team['teamNumber'] not in specific_event_teams_list):
                    specific_event_teams_list.append(team['teamNumber'])

                    if settings.debug_level>2:
                        print(info_i()+'    Adding team #'+str(team['teamNumber']))
        
        except Exception as e:
            print(e)
            print('\n\n\n\n\n\n\n\n\n')
            raise e
    

    
    if settings.debug_level>1:
        print('\n'+info_i()+'    Formatting matches_per_team_dic')
        print(info_i()+'    len(matches_per_team_dic.keys()): '+str(len(matches_per_team_dic.keys())))
    
    matches_per_team_for_pandas = {
        'teamNumber':[],
        'matches'   :[]
    }
    
    for team in matches_per_team_dic.keys():
        if (specific_event_teams == None) or (team in specific_event_teams_list):
            matches_per_team_for_pandas['teamNumber'].append(team)
            matches_per_team_for_pandas['matches'].append(matches_per_team_dic[team])

    
    if settings.debug_level>1:
        print(info_i()+'    Creating pandas dataframe from matches_per_team_dic')
        print(info_i()+'    len(matches_per_team_for_pandas[\'teamNumber\']): '+str(len(matches_per_team_for_pandas['teamNumber'])))
        print(info_i()+'      specific_event_teams: '+str(specific_event_teams))
        print(info_i()+'      specific_event_teams_list: '+str(specific_event_teams_list))
    
    matches_per_team = pd.DataFrame(matches_per_team_for_pandas)
    
    if (specific_event_teams != None):
        if settings.debug_level>1:
            print(info_i()+'    Filtering pandas dataframe matches_per_team for only the teams in specific_event_teams_list')
            print(info_i()+'    Start shape of matches_per_team: '+str(matches_per_team.shape))
        
        matches_per_team = matches_per_team[matches_per_team['teamNumber'].isin( specific_event_teams_list)]
    
    if settings.debug_level>1:
        print(info_i()+'    End shape of matches_per_team: '+str(matches_per_team.shape))
    
    #print(matches_per_team)
    if settings.debug_level>1:
        print(green_check()+'    Teams assembled. Writing all matches per team to file generatedfiles/matches-per-team.csv...       ')
    
    matches_per_team.to_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','matches-per-team.csv'), index=False)


    if settings.debug_level>1:
        print(green_check()+'    Teams assembled. Writing all team numbers to file generatedfiles/team-list-filtered.csv...       ')
    
    matches_per_team['teamNumber'].to_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','team-list-filtered.csv'), index=False)

    

    if settings.debug_level>1:
        print(info_i()+'    Creating pandas dataframe from all_matches_dic')
    
    all_matches_pd = pd.DataFrame(all_matches_dic)

    if specific_event_teams != None:
        if settings.debug_level>1:
            print(info_i()+'    Filtering pandas dataframe from all_matches_dic by teams in specific_event_teams_list')
            print(info_i()+'    Start shape of all_matches_pd: '+str(all_matches_pd.shape))
        
        all_matches_pd = all_matches_pd[
            all_matches_pd['Red1'].isin( specific_event_teams_list) |
            all_matches_pd['Red2'].isin( specific_event_teams_list) |
            all_matches_pd['Blue1'].isin(specific_event_teams_list) |
            all_matches_pd['Blue2'].isin(specific_event_teams_list)
        ]
        if settings.debug_level>1:
            print(info_i()+'    End shape of all_matches_pd: '+str(all_matches_pd.shape))
            print(info_i()+'    Sorting pandas dataframe by actualStartTime')
            
    all_matches_pd.sort_values(by='actualStartTime', inplace=True)
    #print(all_matches_pd)
    
    if settings.debug_level>0:
        print(green_check()+'    Matches assembled. Writing all teams to file generatedfiles/all-matches.csv...       ')
    
    all_matches_pd.to_csv(os.path.join(PATH_TO_FTCAPI,'generatedfiles','all-matches.csv'), index=False)

    if settings.debug_level>2:
        print(green_check()+f'    Wrote about {len(pd.unique(all_matches_pd["Red1"]))} (unique in Red1) of teams out of {matchcounter} matches (matchcounter).')
        print(info_i()+f' [jsonparse.py][prepare_opr_calculation] Size of the actual all_matches_pd written: {all_matches_pd.size}')
        print(info_i()+f' [jsonparse.py][prepare_opr_calculation] Shape of the actual all_matches_pd written: {all_matches_pd.shape}')
        print(green_check()+'    Info is now prepared for OPR calculation.')
        print(green_check()+'[jsonparse.py][prepare_opr_calculation] This is the end of prepare_opr_calculation.')



if __name__ == "__main__" and 'get-events-global' in sys.argv:
    print(info_i()+'  [jsonparse.py] This script was called as __main__')
    print(info_i()+'      Jsonparse getting global event ids that match')
    print(info_i()+'      Getting the season\'s data from seasondata at '+os.path.join(PATH_TO_FTCAPI,'generatedfiles','seasondata.json'))

    write_needed_events(SeasonEvents(get_json(os.path.join(PATH_TO_FTCAPI,'generatedfiles','seasondata.json'))), texasonly=False)


# -- End of file --