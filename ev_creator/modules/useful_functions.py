import numpy as np
import pandas as pd
from numpy import NaN
import math

first_season = '2019-20'

#wrong its actually first name + _ + second_name
def convert(name):
  n = ''
  for c in name:
    if c == ' ':
      c = '_'
    n += c
  return n

def convert_date(date):
  n = ''
  for c in date:
    if c == 'T':
      c = ' '
    if c == 'Z':
      c = ''
    n += c
  return n 

def next_spi(pl_matches, team, date):
    try:
        i = 0
        df = pl_matches[(pl_matches['team1']==team) | (pl_matches['team2']==team)]
        while df['date'].iloc[i] < date:
            i = i+1
        i = i+1
        if df['team1'].iloc[i] == team:
            return df['spi1'].iloc[i]
        else:
            return df['spi2'].iloc[i]
    except:
        return np.NaN
    
def previous(season):
  if season ==first_season:
    return season
  season1 = season[:4]
  season2 = season[5:7]
  season1 = int(season1) - 1
  season2 = int(season2) - 1
  return str(season1) + season[4] + str(season2)


def last4npxGAp90(team, kickoff_time, season, team_stats_dict, gw_no_lim):
  x = 0
  for x in range(team_stats_dict[season][team].shape[0]):
    if team_stats_dict[season][team]['date'][x] >= convert_date(kickoff_time):
      break
  if x < gw_no_lim:
    if season != first_season:
      try:
        return float(team_stats_dict[previous(season)][team][['npxGA']].mean())
      except:
        return 1.8
    return float(team_stats_dict[season][team].iloc[:x][['npxGA']].mean())
  return float(team_stats_dict[season][team].iloc[x-gw_no_lim:x][['npxGA']].mean())


def npxGAp90(team, kickoff_time, season, team_stats_dict, gw_no_lim):
  x = 0
  for x in range(team_stats_dict[season][team].shape[0]):
    if team_stats_dict[season][team]['date'][x] >= convert_date(kickoff_time):
      break

  if x < gw_no_lim:
    if season != first_season:
      try:
        return float(team_stats_dict[previous(season)][team][['npxGA']].mean())
      except:
        return 1.8
    return float(team_stats_dict[season][team].iloc[:x][['npxGA']].mean())
  return float(team_stats_dict[season][team].iloc[:x][['npxGA']].mean())


def opp_npxGp90(team, kickoff_time, season, team_stats_dict, gw_no_lim):
  x = 0
  for x in range(team_stats_dict[season][team].shape[0]):
    if team_stats_dict[season][team]['date'][x] >= convert_date(kickoff_time):
      break

  if x < gw_no_lim:
    if season != first_season:
      try:
        return float(team_stats_dict[previous(season)][team][['npxG']].mean())
      except:
        return 0.8
    return float(team_stats_dict[season][team].iloc[:x][['npxG']].mean())
  return float(team_stats_dict[season][team].iloc[:x][['npxG']].mean())


def opp_last4npxGp90(team, kickoff_time, season, team_stats_dict, gw_no_lim):
  x = 0
  for x in range(team_stats_dict[season][team].shape[0]):
    if team_stats_dict[season][team]['date'][x] >= convert_date(kickoff_time):
      break
  if x < gw_no_lim:
    if season != first_season:
      try:
        return float(team_stats_dict[previous(season)][team][['npxG']].mean())
      except:
        return 0.6
    return float(team_stats_dict[season][team].iloc[:x][['npxG']].mean())
  return float(team_stats_dict[season][team].iloc[x-gw_no_lim:x][['npxG']].mean())


def last4npxGp90(df, season, kickoff_time, gw_no_lim):
  x = 0
  try:
    for x in range(df[df['season']==season].shape[0]):
      if df[df['season']==season][::-1]['date'].iloc[x] >= convert_date(kickoff_time):
        x=x-1
        break
    if x < gw_no_lim:
      #get last season's data
      return float(90*df[df['season']==season-1][['npxG']].sum()/float(df[df['season']==season-1][['time']].sum()))
    return float(90*df[df['season']==season][::-1].iloc[x-gw_no_lim:x][['npxG']].sum()/float(df[df['season']==season][::-1].iloc[x-gw_no_lim:x][['time']].sum()))
  except:
    return np.nan


def last4xAp90(df, season, kickoff_time, gw_no_lim):
  x = 0
  try:
    for x in range(df[df['season']==season].shape[0]):
      if df[df['season']==season][::-1]['date'].iloc[x] >= convert_date(kickoff_time):
        x=x-1
        break
    if x < gw_no_lim:
      #get last season's data
      return float(90*df[df['season']==season-1][['xA']].sum()/float(df[df['season']==season-1][['time']].sum()))
    return float(90*df[df['season']==season][::-1].iloc[x-gw_no_lim:x][['xA']].sum()/float(df[df['season']==season][::-1].iloc[x-gw_no_lim:x][['time']].sum()))
  except:
    return np.nan


def npxGp90(df, season, kickoff_time, gw_no_lim):
  x = 0
  try:
    for x in range(df[df['season']==season].shape[0]):
      if df[df['season']==season][::-1]['date'].iloc[x] >= convert_date(kickoff_time):
        x=x-1
        break

    if x < gw_no_lim:
      #get last season's data
      return float(90*df[df['season']==season-1][['npxG']].sum()/float(df[df['season']==season-1][['time']].sum()))
    return float(90*df[df['season']==season][::-1].iloc[:x][['npxG']].sum()/float(df[df['season']==season][::-1].iloc[:x][['time']].sum()))
  except:
    return np.nan


def xAp90(df, season, kickoff_time, gw_no_lim):
  x = 0
  try:
    for x in range(df[df['season']==season].shape[0]):
      if df[df['season']==season][::-1]['date'].iloc[x] >= convert_date(kickoff_time):
        x=x-1
        break

    if x < gw_no_lim:
      #get last season's data
      return float(90*df[df['season']==season-1][['xA']].sum()/float(df[df['season']==season-1][['time']].sum()))
    return float(90*df[df['season']==season][::-1].iloc[:x][['xA']].sum()/float(df[df['season']==season][::-1].iloc[:x][['time']].sum()))
  except:
    return np.nan


def shp90(df, season, kickoff_time, gw_no_lim):
  x = 0
  try:
    for x in range(df[df['season']==season].shape[0]):
      if df[df['season']==season][::-1]['date'].iloc[x] >= convert_date(kickoff_time):
        x=x-1
        break

    if x < gw_no_lim:
      #get last season's data
      return float(90*df[df['season']==season-1][['shots']].sum()/float(df[df['season']==season-1][['time']].sum()))
    return float(90*df[df['season']==season][::-1].iloc[:x][['shots']].sum()/float(df[df['season']==season][::-1].iloc[:x][['time']].sum()))
  except:
    return np.nan


def kpp90(df, season, kickoff_time, gw_no_lim):
  x = 0
  try:
    for x in range(df[df['season']==season].shape[0]):
      if df[df['season']==season][::-1]['date'].iloc[x] >= convert_date(kickoff_time):
        x=x-1
        break

    if x < gw_no_lim:
      #get last season's data
      return float(90*df[df['season']==season-1][['key_passes']].sum()/float(df[df['season']==season-1][['time']].sum()))
    return float(90*df[df['season']==season][::-1].iloc[:x][['key_passes']].sum()/float(df[df['season']==season][::-1].iloc[:x][['time']].sum()))
  except:
    return np.nan


def npg (main_df, understat_df, season):
  try:
    i=0
    while understat_df[understat_df['season']==season][::-1]['date'].iloc[i] < convert_date(main_df['kickoff_time'][0]):
      i=i+1
    i=i-1
  except:
    i=0
  npgoals=[]
  df = understat_df[understat_df['season']==season][::-1]
  try:
    for x in range(main_df.shape[0]):
      if main_df['minutes'][x] != 0:
        npgoals.append(df['npg'].iloc[i])
        i=i+1
      else:
        npgoals.append(0)
  except:
    npgoals = [np.nan]*main_df.shape[0]
  return npgoals


def team(fixture_id, was_home, season, teams, fixtures):
  if was_home:
    return teams[season].iloc[int(fixtures[season][fixtures[season]['id'] == fixture_id]['team_h'])-1, 5]
  else:
    return teams[season].iloc[int(fixtures[season][fixtures[season]['id'] == fixture_id]['team_a'])-1, 5]


def clean_sheets(exp_goals):
  return math.e**-exp_goals


def xAppPoints(xmins):
  sum=0
  for x in range(60):
    sum += float((xmins**x)*(math.e**(-xmins))/math.factorial(x))
  chance60 = 1-float(sum)
  if xmins == 0:
    return (0,0)
  elif xmins < 30:
    return (0.033*xmins, chance60)
  else:
    return (2*chance60 + 1 - chance60, chance60)


def minus_points_def(xgoals):
  return -((xgoals**2)*(math.e**-xgoals)/math.factorial(2) + (xgoals**3)*(math.e**-xgoals)/math.factorial(3)) - 2*((xgoals**4)*(math.e**-xgoals)/math.factorial(4) + (xgoals**5)*(math.e**-xgoals)/math.factorial(5))

def save_points(xsaves):
  save1 = (xsaves**3)*(math.e**-xsaves)/math.factorial(3) + (xsaves**4)*(math.e**-xsaves)/math.factorial(4) + (xsaves**5)*(math.e**-xsaves)/math.factorial(5)
  save2 = (xsaves**6)*(math.e**-xsaves)/math.factorial(6) + (xsaves**7)*(math.e**-xsaves)/math.factorial(7) + (xsaves**8)*(math.e**-xsaves)/math.factorial(8)
  save3 = (xsaves**9)*(math.e**-xsaves)/math.factorial(9) + (xsaves**10)*(math.e**-xsaves)/math.factorial(10) + (xsaves**11)*(math.e**-xsaves)/math.factorial(11)
  return  save1 + 2*save2 + 3*save3

def team_id(player_id, season, players_raw):
  return players_raw[season][players_raw[season]['id']==player_id]['team'].iloc[0]
  
def previous_team_id(team_id, season, teams):
  t = teams[season] 
  team_name = t[t['id']==team_id]['name'].iloc[0]
  t_prev = teams[previous(season)]
  return t_prev[t_prev['name']==team_name]['id'].iloc[0]

def fixture_info(player_id, season, gw, fixtures, teams, players_raw):
  team = team_id(player_id, season, players_raw)
  df = fixtures[season][fixtures[season]['event']==gw]
  fix = []
  filtered_df = df[(df['team_a']==team) | (df['team_h']==team)]
  for i in range(filtered_df.shape[0]):
    if filtered_df['team_a'].iloc[i] == team:
      fix.append((teams[season].iloc[filtered_df['team_h'].iloc[i]-1, 5], False, filtered_df['kickoff_time'].iloc[i], filtered_df['fix_prob'].iloc[i]))
    else:
      fix.append((teams[season].iloc[filtered_df['team_a'].iloc[i]-1, 5], True, filtered_df['kickoff_time'].iloc[i], filtered_df['fix_prob'].iloc[i]))
  return fix


def fixture_info2(team, season, gw, fixtures, teams):
  df = fixtures[season][fixtures[season]['event']==gw]
  fix = []
  filtered_df = df[(df['team_a']==team) | (df['team_h']==team)]
  for i in range(filtered_df.shape[0]):
    if filtered_df['team_a'].iloc[i] == team:
      fix.append((teams[season].iloc[filtered_df['team_h'].iloc[i]-1, 5], False, filtered_df['kickoff_time'].iloc[i], filtered_df['team_a_score'].iloc[i], filtered_df['team_h_score'].iloc[i]))
    else:
      fix.append((teams[season].iloc[filtered_df['team_a'].iloc[i]-1, 5], True, filtered_df['kickoff_time'].iloc[i], filtered_df['team_h_score'].iloc[i], filtered_df['team_a_score'].iloc[i]))
  return fix


def finishing_rate(understat_df):
  return (understat_df['npg'].sum()+55)/(understat_df['npxG'].sum()+55)

def penalty_finishing_rate(understat_df):
  return (understat_df['goals'].sum() - understat_df['npg'].sum()+15)/(understat_df['xG'].sum()-understat_df['npxG'].sum()+15)

def sh (main_df, understat_df, season):
  try:
    i=0
    while understat_df[understat_df['season']==season][::-1]['date'].iloc[i] < convert_date(main_df['kickoff_time'][0]):
      i=i+1
    i=i-1
  except:
    i=0
  s=[]
  df = understat_df[understat_df['season']==season][::-1]
  for x in range(main_df.shape[0]):
    if main_df['minutes'][x] != 0:
      s.append(df['shots'].iloc[i])
      i=i+1
    else:
      s.append(0)
  return s

def el_per_app(df, gw, el):
  if el == 'bonus':
    return df['bonus'].iloc[:gw].mean()
  elif el == 'yc':
    return df['yellow_cards'].iloc[:gw].mean()

def assist_to_goal_ratio(seasons, PATH):
    total = []
    for season in seasons:
        df = pd.read_csv(PATH + season + '/players_raw.csv')
        total.append(df)
    total_df = pd.concat(total)
    return sum(total_df['assists'].to_list())/sum(total_df['goals_scored'].to_list())

def avg(l):
    if len(l)==0:
        return 0
    else:
        return sum(l)/len(l)

def rates100(df, kickoff_time, el):
    try:
        i = 0
        while df['date'].iloc[i] >= convert_date(kickoff_time):
            i=i+1
        c = i + 1
        return 90*sum(df[el].to_list()[c:100+c])/sum(df['time'].to_list()[c:100+c])
    except:
        return 0  # np.nan while creating the dataset and training, 0 for prediction

def npg_rate_season(df, kickoff_time, season):
    try:
        new_df = df[df['season']==season]
        if new_df.shape[0] < 4:
          new_df = df[df['season']==season-1]
          return 90*sum(new_df['npg'].to_list())/sum(new_df['time'].to_list())
        i = 0
        while new_df['date'].iloc[i] >= convert_date(kickoff_time):
            i=i+1
        c = i + 1
        return 90*sum(new_df['npg'].to_list()[c:])/sum(new_df['time'].to_list()[c:])
    except:
        return rates100(df, kickoff_time, 'npg')

def assist_rate_season(df, kickoff_time, season):
    try:
        new_df = df[df['season']==season]
        if new_df.shape[0] < 4:
          new_df = df[df['season']==season-1]
          return 90*sum(new_df['assists'].to_list())/sum(new_df['time'].to_list())
        i = 0
        while new_df['date'].iloc[i] >= convert_date(kickoff_time):
            i=i+1
        c = i + 1
        return 90*sum(new_df['assists'].to_list()[c:])/sum(new_df['time'].to_list()[c:])
    except:
        return rates100(df, kickoff_time, 'assists')
'''
xpens_2022 = {
      'Arsenal': [(13, 1)], #saka
      'Aston Villa': [(40, 1)], #watkins
      'Brentford': [(80, 1), (95, 0)], #toney, mbeumo
      'Brighton': [(116, 1), (104, 0)], #mac allister, gross
      'Bournemouth':[(105, 1)], #solanke                                                        
      'Chelsea':  [(145, 0.95), (146, 0.05)], # havertz, james
      'Crystal Palace': [(160, 1), (169, 0)], #zaha, eze
      'Everton': [(191, 1), (189, 0)], #dcl, gray
      'Leeds':  [(227, 0.2), (225, 0.8)], #bamford, rodrigo
      'Leicester':  [(255, 0), (259, 0), (261, 0.4), (262, 0.6)], #vardy, tielemans, maddison, IHEANACHO
      'Liverpool': [(283, 1), (282, 0)], #salah, fabinho
      'Man City':  [(318,1), (303, 0.4)], #haaland, mahrez
      'Man Utd': [(335, 0.15), (333, 0.85)], #rashford, bruno
      'Newcastle': [(356, 0.5), (594, 0.5)], #wilson, isak
      'Nott\'m Forest':[(315, 1)], #johnson                                                     
      'Southampton':  [(407, 1)], #jwp
      'Spurs': [(427, 1), (428, 0)], #kane, son
      'Fulham': [(210, 0), (346, 0), (618, 0.9)], #mitro, andreas, vinicious                                                   
      'West Ham': [(464, 0.7), (465, 0.15), (458, 0.15)], #benrahma, bowen, antonio
      'Wolves': [(476, 0.4), (480, 0.6)], #jimenez, neves
  }
'''
xpens_2022 = {
      'Arsenal': [(19, 0), (14, 0), (12, 0)], #saka, odegaard, martinelli
      'Aston Villa': [(43, 0), (60, 0), (34, 0)], #luiz, watkins, bailey
      'Brentford': [(117, 0), (108, 0), (119, 0)], #toney, mbeumo, wissa
      'Brighton': [(135, 0), (134, 0), (154, 0)], # pedro, gross, welbeck
      'Bournemouth':[(85, 0), (63, 0), (86, 0)], #solanke, billing, tavernier                                                       
      'Chelsea':  [(212, 0), (199, 0), (216, 0)], # nkunku, enzo, sterling       
      'Crystal Palace': [(226, 0), (225, 0), (232, 0)], #eze, edouard, mateta         
      'Everton': [(246, 0), (258, 0), (601, 0)], #dcl, maupay, danjuma
      'Luton':  [(326, 0), (314, 0), (340, 0)], #Morris, Adebayo, Woodrow           
      'Burnley':  [(177, 0), (170, 0), (594, 0)], #rodriguez, gudmundsson, amdouni
      'Liverpool': [(308, 0), (304, 0), (296, 0)], #salah, mac allister, fabinho
      'Man City':  [(355, 0), (359, 0), (343, 0)], #haaland, mahrez, alvarez
      'Man Utd': [(373, 0), (396, 0), (390, 0)], #bruno, rashford, martial
      'Newcastle': [(433, 0), (415, 0), (416, 0)], #wilson, isak, joelinton
      'Nott\'m Forest':[(447, 0), (437, 0), (378, 0)], #gibbs-white, awoniyi, elanga                                                     
      'Sheffield Utd':  [(477, 0), (488, 0), (481, 0)], #brewster, norwood, fleck
      'Spurs': [(516, 0), (509, 0), (504, 0)], #son, richarlison, maddison
      'Fulham': [(278, 0), (267, 0), (288, 0)], #mitro, andreas, wilson                                                   
      'West Ham': [(525, 0), (539, 0), (664, 0)], #benrahma, paqueta, ward-prowse
      'Wolves': [(558, 0), (557, 0), (567, 0)], #jimenez, hwang, neto
  }
  
def pens_per_game(fixtures, season, team_stats_dict, teams, team_id, gw_no_lim):
    fix = fixtures[season]
    team_fixtures = fix[(fix['team_h']==team_id) | (fix['team_a']==team_id)]
    team = teams[season].iloc[team_id-1, 5]
    cnt = 0
    pens = []
    team_df = team_stats_dict[season][team]
    if team_df.shape[0] < gw_no_lim:
      try:
        if not team_stats_dict[previous(season)][team].empty:
            prev_id = previous_team_id(team_id, season, teams)
            return pens_per_game(fixtures, previous(season), team_stats_dict, teams, prev_id, gw_no_lim)
      except:
          return [0.1, 0.1, 0.1, 0.1], 0
    while team_fixtures['kickoff_time'].iloc[cnt] == None:
        cnt+=1
    for i in range(team_df.shape[0]):
        if convert_date(team_fixtures['kickoff_time'].iloc[i+cnt]) == team_df['date'].iloc[i]:
            if team_df['xG'].iloc[i] - team_df['npxG'].iloc[i] < 0.5:
                pens.append(0)
            elif team_df['xG'].iloc[i] - team_df['npxG'].iloc[i] < 1:
                pens.append(1)
            elif team_df['xG'].iloc[i] - team_df['npxG'].iloc[i] < 2:
                pens.append(2)
            else:
                pens.append(3)
        else:
            # understat and fpl kickoff times don't match for some reason
            pens.append(0)
    return pens, cnt

def p90_main_df(main_df, el, x):
  l = []
  mins = []
  for i in range(main_df.shape[0]):
    if main_df['minutes'].iloc[i] != 0:
      l.append(main_df[el].iloc[i])
      mins.append(main_df['minutes'].iloc[i])
  if sum(mins[:x]) == 0:
    return np.nan
  return 90*sum(l[:x])/sum(mins[:x])

from statistics import mode

teams_map = {
        'Arsenal': 'Arsenal',
        'Aston Villa': 'Aston_Villa',
        'Brentford': 'Brentford',
        'Brighton': 'Brighton',
        'Burnley': 'Burnley',
        'Bournemouth': 'Bournemouth',
        'Chelsea': 'Chelsea',
        'Crystal Palace': 'Crystal Palace',
        'Everton': 'Everton',
        'Leeds': 'Leeds',
        'Leicester': 'Leicester',
        'Liverpool': 'Liverpool',
        'Man City': 'Manchester City',
        'Man Utd': 'Manchester United',
        'Newcastle': 'Newcastle United',
        'Norwich': 'Norwich',
        'Southampton': 'Southampton',
        'Spurs': 'Tottenham',
        'Watford': 'Watford',
        'West Ham': 'West_Ham',
        'Wolves': 'Wolverhampton_Wanderers',
        'Stoke': 'Stoke',
        'Watford': 'Watford',
        'Sunderland': 'Sunderland',
        'Hull': 'Hull',
        'West Brom': 'West Bromwich Albion',
        'Middlesbrough': 'Middlesbrough',
        'Swansea': 'Swansea',
        'Huddersfield': 'Huddersfield',
        'Cardiff':'Cardiff',
        'Sheffield Utd': 'Sheffield United'
    }

inv_teams_map = {v: k for k, v in teams_map.items()}

def players_team(udf, season):
  try:
    udf = udf[udf['season']==season]
    return inv_teams_map[mode(udf['h_team'].to_list() + udf['a_team'].to_list())]
  except:
    return np.nan