import pandas as pd
import requests
import asyncio
import json
import pandas as pd
import aiohttp
import nest_asyncio
nest_asyncio.apply()
from understat import Understat

'''
async def main(team, season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        teams = await understat.get_teams(
            "epl",
            season,
            title=team
        )
        return pd.DataFrame(teams[0]['history'])
'''

def dataset_initialization(PATH):
    '''
    # Team Stats 2016/17
    season = '2016-17'
    loop = asyncio.get_event_loop()
    Arsenal_stats_df = loop.run_until_complete(main('Arsenal',int(season[:4])))
    Bournemouth_stats_df = loop.run_until_complete(main('Bournemouth',int(season[:4])))
    Burnley_stats_df = loop.run_until_complete(main('Burnley',int(season[:4])))
    Chelsea_stats_df = loop.run_until_complete(main('Chelsea',int(season[:4])))
    Crystal_Palace_stats_df = loop.run_until_complete(main('Crystal Palace',int(season[:4])))
    Everton_stats_df = loop.run_until_complete(main('Everton',int(season[:4])))
    Hull_stats_df = loop.run_until_complete(main('Hull',int(season[:4])))
    Leicester_stats_df = loop.run_until_complete(main('Leicester',int(season[:4])))
    Liverpool_stats_df = loop.run_until_complete(main('Liverpool',int(season[:4])))
    Manchester_City_stats_df = loop.run_until_complete(main('Manchester City',int(season[:4])))
    Manchester_United_stats_df = loop.run_until_complete(main('Manchester United',int(season[:4])))
    Middlesbrough_stats_df = loop.run_until_complete(main('Middlesbrough',int(season[:4])))
    Stoke_stats_df = loop.run_until_complete(main('Stoke',int(season[:4])))
    Southampton_stats_df = loop.run_until_complete(main('Southampton',int(season[:4])))
    Tottenham_stats_df = loop.run_until_complete(main('Tottenham',int(season[:4])))
    Swansea_stats_df = loop.run_until_complete(main('Swansea',int(season[:4])))
    Sunderland_stats_df = loop.run_until_complete(main('Sunderland',int(season[:4])))
    Watford_stats_df = loop.run_until_complete(main('Watford',int(season[:4])))
    West_Ham_stats_df = loop.run_until_complete(main('West Ham',int(season[:4])))
    West_Bromwich_Albion_stats_df = loop.run_until_complete(main('West Bromwich Albion',int(season[:4])))

    team_stats_dict_2016 = {
        'Arsenal': Arsenal_stats_df,
        'Hull': Hull_stats_df,
        'Swansea': Swansea_stats_df,
        'Sunderland': Sunderland_stats_df,
        'Burnley': Burnley_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Bournemouth': Bournemouth_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Middlesbrough': Middlesbrough_stats_df,
        'Stoke': Stoke_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'Watford': Watford_stats_df,
        'West Ham': West_Ham_stats_df,
        'West Brom': West_Bromwich_Albion_stats_df
    }

    # Team Stats 2017/18
    season = '2017-18'
    loop = asyncio.get_event_loop()
    Arsenal_stats_df = loop.run_until_complete(main('Arsenal',int(season[:4])))
    Bournemouth_stats_df = loop.run_until_complete(main('Bournemouth',int(season[:4])))
    Burnley_stats_df = loop.run_until_complete(main('Burnley',int(season[:4])))
    Chelsea_stats_df = loop.run_until_complete(main('Chelsea',int(season[:4])))
    Crystal_Palace_stats_df = loop.run_until_complete(main('Crystal Palace',int(season[:4])))
    Everton_stats_df = loop.run_until_complete(main('Everton',int(season[:4])))
    Newcastle_United_stats_df = loop.run_until_complete(main('Newcastle United',int(season[:4])))
    Leicester_stats_df = loop.run_until_complete(main('Leicester',int(season[:4])))
    Liverpool_stats_df = loop.run_until_complete(main('Liverpool',int(season[:4])))
    Manchester_City_stats_df = loop.run_until_complete(main('Manchester City',int(season[:4])))
    Manchester_United_stats_df = loop.run_until_complete(main('Manchester United',int(season[:4])))
    Brighton_stats_df = loop.run_until_complete(main('Brighton',int(season[:4])))
    Stoke_stats_df = loop.run_until_complete(main('Stoke',int(season[:4])))
    Southampton_stats_df = loop.run_until_complete(main('Southampton',int(season[:4])))
    Tottenham_stats_df = loop.run_until_complete(main('Tottenham',int(season[:4])))
    Swansea_stats_df = loop.run_until_complete(main('Swansea',int(season[:4])))
    Huddersfield_stats_df = loop.run_until_complete(main('Huddersfield',int(season[:4])))
    Watford_stats_df = loop.run_until_complete(main('Watford',int(season[:4])))
    West_Ham_stats_df = loop.run_until_complete(main('West Ham',int(season[:4])))
    West_Bromwich_Albion_stats_df = loop.run_until_complete(main('West Bromwich Albion',int(season[:4])))

    team_stats_dict_2017 = {
        'Arsenal': Arsenal_stats_df,
        'Newcastle': Newcastle_United_stats_df,
        'Swansea': Swansea_stats_df,
        'Brighton': Brighton_stats_df,
        'Burnley': Burnley_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Bournemouth': Bournemouth_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Huddersfield': Huddersfield_stats_df,
        'Stoke': Stoke_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'Watford': Watford_stats_df,
        'West Ham': West_Ham_stats_df,
        'West Brom': West_Bromwich_Albion_stats_df
    }

    # Team Stats 2018/19
    season = '2018-19'
    loop = asyncio.get_event_loop()
    Arsenal_stats_df = loop.run_until_complete(main('Arsenal',int(season[:4])))
    Bournemouth_stats_df = loop.run_until_complete(main('Bournemouth',int(season[:4])))
    Burnley_stats_df = loop.run_until_complete(main('Burnley',int(season[:4])))
    Chelsea_stats_df = loop.run_until_complete(main('Chelsea',int(season[:4])))
    Crystal_Palace_stats_df = loop.run_until_complete(main('Crystal Palace',int(season[:4])))
    Everton_stats_df = loop.run_until_complete(main('Everton',int(season[:4])))
    Newcastle_United_stats_df = loop.run_until_complete(main('Newcastle United',int(season[:4])))
    Leicester_stats_df = loop.run_until_complete(main('Leicester',int(season[:4])))
    Liverpool_stats_df = loop.run_until_complete(main('Liverpool',int(season[:4])))
    Manchester_City_stats_df = loop.run_until_complete(main('Manchester City',int(season[:4])))
    Manchester_United_stats_df = loop.run_until_complete(main('Manchester United',int(season[:4])))
    Brighton_stats_df = loop.run_until_complete(main('Brighton',int(season[:4])))
    Fulham_stats_df = loop.run_until_complete(main('Fulham',int(season[:4])))
    Southampton_stats_df = loop.run_until_complete(main('Southampton',int(season[:4])))
    Tottenham_stats_df = loop.run_until_complete(main('Tottenham',int(season[:4])))
    Cardiff_stats_df = loop.run_until_complete(main('Cardiff',int(season[:4])))
    Huddersfield_stats_df = loop.run_until_complete(main('Huddersfield',int(season[:4])))
    Watford_stats_df = loop.run_until_complete(main('Watford',int(season[:4])))
    West_Ham_stats_df = loop.run_until_complete(main('West Ham',int(season[:4])))
    Wolverhampton_Wanderers_stats_df = loop.run_until_complete(main('Wolverhampton Wanderers',int(season[:4])))

    team_stats_dict_2018 = {
        'Arsenal': Arsenal_stats_df,
        'Newcastle': Newcastle_United_stats_df,
        'Fulham': Fulham_stats_df,
        'Brighton': Brighton_stats_df,
        'Burnley': Burnley_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Bournemouth': Bournemouth_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Huddersfield': Huddersfield_stats_df,
        'Cardiff': Cardiff_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'Watford': Watford_stats_df,
        'West Ham': West_Ham_stats_df,
        'Wolves': Wolverhampton_Wanderers_stats_df
    }
    '''
    # Team Stats 2019/20
    season = '2019-20'

    Arsenal_stats_df = pd.read_csv(PATH + season + '/understat/understat_Arsenal.csv')
    Aston_Villa_stats_df = pd.read_csv(PATH + season + '/understat/understat_Aston_Villa.csv')
    Sheffield_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Sheffield_United.csv')
    Brighton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Brighton.csv')
    Burnley_stats_df = pd.read_csv(PATH + season + '/understat/understat_Burnley.csv')
    Chelsea_stats_df = pd.read_csv(PATH + season + '/understat/understat_Chelsea.csv')
    Crystal_Palace_stats_df = pd.read_csv(PATH + season + '/understat/understat_Crystal_Palace.csv')
    Everton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Everton.csv')
    Bournemouth_stats_df = pd.read_csv(PATH + season + '/understat/understat_Bournemouth.csv')
    Leicester_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leicester.csv')
    Liverpool_stats_df = pd.read_csv(PATH + season + '/understat/understat_Liverpool.csv')
    Manchester_City_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_City.csv')
    Manchester_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_United.csv')
    Newcastle_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Newcastle_United.csv')
    Norwich_stats_df = pd.read_csv(PATH + season + '/understat/understat_Norwich.csv')
    Southampton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Southampton.csv')
    Tottenham_stats_df = pd.read_csv(PATH + season + '/understat/understat_Tottenham.csv')
    Watford_stats_df = pd.read_csv(PATH + season + '/understat/understat_Watford.csv')
    West_Ham_stats_df = pd.read_csv(PATH + season + '/understat/understat_West_Ham.csv')
    Wolverhampton_Wanderers_stats_df = pd.read_csv(PATH + season + '/understat/understat_Wolverhampton_Wanderers.csv')

    team_stats_dict_2019 = {
        'Arsenal': Arsenal_stats_df,
        'Aston Villa': Aston_Villa_stats_df,
        'Sheffield Utd': Sheffield_United_stats_df,
        'Brighton': Brighton_stats_df,
        'Burnley': Burnley_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Bournemouth': Bournemouth_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Newcastle': Newcastle_United_stats_df,
        'Norwich': Norwich_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'Watford': Watford_stats_df,
        'West Ham': West_Ham_stats_df,
        'Wolves': Wolverhampton_Wanderers_stats_df
    }


    # Team Stats 2020/21
    season = '2020-21'

    Arsenal_stats_df = pd.read_csv(PATH + season + '/understat/understat_Arsenal.csv')
    Aston_Villa_stats_df = pd.read_csv(PATH + season + '/understat/understat_Aston_Villa.csv')
    Sheffield_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Sheffield_United.csv')
    Brighton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Brighton.csv')
    Burnley_stats_df = pd.read_csv(PATH + season + '/understat/understat_Burnley.csv')
    Chelsea_stats_df = pd.read_csv(PATH + season + '/understat/understat_Chelsea.csv')
    Crystal_Palace_stats_df = pd.read_csv(PATH + season + '/understat/understat_Crystal_Palace.csv')
    Everton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Everton.csv')
    Leeds_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leeds.csv')
    Leicester_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leicester.csv')
    Liverpool_stats_df = pd.read_csv(PATH + season + '/understat/understat_Liverpool.csv')
    Manchester_City_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_City.csv')
    Manchester_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_United.csv')
    Newcastle_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Newcastle_United.csv')
    Fulham_stats_df = pd.read_csv(PATH + season + '/understat/understat_Fulham.csv')
    Southampton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Southampton.csv')
    Tottenham_stats_df = pd.read_csv(PATH + season + '/understat/understat_Tottenham.csv')
    West_Bromwich_Albion_stats_df = pd.read_csv(PATH + season + '/understat/understat_West_Bromwich_Albion.csv')
    West_Ham_stats_df = pd.read_csv(PATH + season + '/understat/understat_West_Ham.csv')
    Wolverhampton_Wanderers_stats_df = pd.read_csv(PATH + season + '/understat/understat_Wolverhampton_Wanderers.csv')

    team_stats_dict_2020 = {
        'Arsenal': Arsenal_stats_df,
        'Aston Villa': Aston_Villa_stats_df,
        'Sheffield Utd': Sheffield_United_stats_df,
        'Brighton': Brighton_stats_df,
        'Burnley': Burnley_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Leeds': Leeds_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Newcastle': Newcastle_United_stats_df,
        'Fulham': Fulham_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'West Brom': West_Bromwich_Albion_stats_df,
        'West Ham': West_Ham_stats_df,
        'Wolves': Wolverhampton_Wanderers_stats_df
    }


    # Team Stats 2021/22
    season = '2021-22'

    Arsenal_stats_df = pd.read_csv(PATH + season + '/understat/understat_Arsenal.csv')
    Aston_Villa_stats_df = pd.read_csv(PATH + season + '/understat/understat_Aston_Villa.csv')
    Brentford_stats_df = pd.read_csv(PATH + season + '/understat/understat_Brentford.csv')
    Brighton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Brighton.csv')
    Burnley_stats_df = pd.read_csv(PATH + season + '/understat/understat_Burnley.csv')
    Chelsea_stats_df = pd.read_csv(PATH + season + '/understat/understat_Chelsea.csv')
    Crystal_Palace_stats_df = pd.read_csv(PATH + season + '/understat/understat_Crystal_Palace.csv')
    Everton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Everton.csv')
    Leeds_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leeds.csv')
    Leicester_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leicester.csv')
    Liverpool_stats_df = pd.read_csv(PATH + season + '/understat/understat_Liverpool.csv')
    Manchester_City_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_City.csv')
    Manchester_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_United.csv')
    Newcastle_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Newcastle_United.csv')
    Norwich_stats_df = pd.read_csv(PATH + season + '/understat/understat_Norwich.csv')
    Southampton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Southampton.csv')
    Tottenham_stats_df = pd.read_csv(PATH + season + '/understat/understat_Tottenham.csv')
    Watford_stats_df = pd.read_csv(PATH + season + '/understat/understat_Watford.csv')
    West_Ham_stats_df = pd.read_csv(PATH + season + '/understat/understat_West_Ham.csv')
    Wolverhampton_Wanderers_stats_df = pd.read_csv(PATH + season + '/understat/understat_Wolverhampton_Wanderers.csv')

    team_stats_dict_2021 = {
        'Arsenal': Arsenal_stats_df,
        'Aston Villa': Aston_Villa_stats_df,
        'Brentford': Brentford_stats_df,
        'Brighton': Brighton_stats_df,
        'Burnley': Burnley_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Leeds': Leeds_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Newcastle': Newcastle_United_stats_df,
        'Norwich': Norwich_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'Watford': Watford_stats_df,
        'West Ham': West_Ham_stats_df,
        'Wolves': Wolverhampton_Wanderers_stats_df
    }


    # Team Stats 2022/23
    season = '2022-23'

    Arsenal_stats_df = pd.read_csv(PATH + season + '/understat/understat_Arsenal.csv')
    Aston_Villa_stats_df = pd.read_csv(PATH + season + '/understat/understat_Aston_Villa.csv')
    Brentford_stats_df = pd.read_csv(PATH + season + '/understat/understat_Brentford.csv')
    Brighton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Brighton.csv')
    Bournemouth_stats_df = pd.read_csv(PATH + season + '/understat/understat_Bournemouth.csv')
    Chelsea_stats_df = pd.read_csv(PATH + season + '/understat/understat_Chelsea.csv')
    Crystal_Palace_stats_df = pd.read_csv(PATH + season + '/understat/understat_Crystal_Palace.csv')
    Everton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Everton.csv')
    Leeds_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leeds.csv')
    Leicester_stats_df = pd.read_csv(PATH + season + '/understat/understat_Leicester.csv')
    Liverpool_stats_df = pd.read_csv(PATH + season + '/understat/understat_Liverpool.csv')
    Manchester_City_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_City.csv')
    Manchester_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Manchester_United.csv')
    Newcastle_United_stats_df = pd.read_csv(PATH + season + '/understat/understat_Newcastle_United.csv')
    Fulham_stats_df = pd.read_csv(PATH + season + '/understat/understat_Fulham.csv')
    Southampton_stats_df = pd.read_csv(PATH + season + '/understat/understat_Southampton.csv')
    Tottenham_stats_df = pd.read_csv(PATH + season + '/understat/understat_Tottenham.csv')
    Nottingham_Forest_stats_df = pd.read_csv(PATH + season + '/understat/understat_Nottingham_Forest.csv')
    West_Ham_stats_df = pd.read_csv(PATH + season + '/understat/understat_West_Ham.csv')
    Wolverhampton_Wanderers_stats_df = pd.read_csv(PATH + season + '/understat/understat_Wolverhampton_Wanderers.csv')

    team_stats_dict_2022 = {
        'Arsenal': Arsenal_stats_df,
        'Aston Villa': Aston_Villa_stats_df,
        'Brentford': Brentford_stats_df,
        'Brighton': Brighton_stats_df,
        'Bournemouth': Bournemouth_stats_df,
        'Chelsea': Chelsea_stats_df,
        'Crystal Palace': Crystal_Palace_stats_df,
        'Everton': Everton_stats_df,
        'Leeds': Leeds_stats_df,
        'Leicester': Leicester_stats_df,
        'Liverpool':Liverpool_stats_df,
        'Man City': Manchester_City_stats_df,
        'Man Utd': Manchester_United_stats_df,
        'Newcastle': Newcastle_United_stats_df,
        'Fulham': Fulham_stats_df,
        'Southampton': Southampton_stats_df,
        'Spurs': Tottenham_stats_df,
        'Nott\'m Forest': Nottingham_Forest_stats_df,
        'West Ham': West_Ham_stats_df,
        'Wolves': Wolverhampton_Wanderers_stats_df
    }


    team_stats_dict = {
        '2019-20': team_stats_dict_2019,
        '2020-21': team_stats_dict_2020,
        '2021-22': team_stats_dict_2021,
        '2022-23': team_stats_dict_2022
    }

    url = 'https://fantasy.premierleague.com/api/fixtures/'
    fixtures = {
        '2019-20': pd.read_csv(PATH + '2019-20/fixtures.csv'),
        '2020-21': pd.read_csv(PATH + '2020-21/fixtures.csv'),
        '2021-22': pd.read_csv(PATH + '2021-22/fixtures.csv'),
        '2022-23': pd.json_normalize(requests.get(url).json())
    }


    players_raw = {
        '2019-20': pd.read_csv(PATH + '2019-20/players_raw.csv'),
        '2020-21': pd.read_csv(PATH + '2020-21/players_raw.csv'),
        '2021-22': pd.read_csv(PATH + '2021-22/players_raw.csv'),
        '2022-23': pd.read_csv(PATH + '2022-23/players_raw.csv')
    }

    teams = {
        '2019-20': pd.read_csv(PATH + '2019-20/teams.csv'),
        '2020-21': pd.read_csv(PATH + '2020-21/teams.csv'),
        '2021-22': pd.read_csv(PATH + '2021-22/teams.csv'),
        '2022-23': pd.read_csv(PATH + '2022-23/teams.csv')
    }

    ids = {
        '2019-20': 'FPL_ID_2019',
        '2020-21': 'FPL_ID_2020',
        '2021-22': 'FPL_ID_2021',
        '2022-23': 'FPL_ID_2022'
    }

    seasons = ['2019-20', '2020-21', '2021-22', '2022-23']

    return team_stats_dict, fixtures, players_raw, teams, ids, seasons