import pandas as pd
import numpy as np
from tqdm import tqdm
from modules.useful_functions import next_spi, team_id, p90_main_df, avg, rates100, npg_rate_season, assist_rate_season, convert_date, pens_per_game, npxGAp90, last4npxGp90, npxGp90, shp90, opp_npxGp90, npg, team, xAp90, kpp90, last4xAp90, opp_last4npxGp90, last4npxGAp90
import time
from modules.useful_functions2 import proj_scores, spis


def npg_dataset_creation(seasons, players_raw, player_info_dict, teams, team_stats_dict, fixtures, gw_no_limit):
    gframes = []
    proj_scores_df = pd.read_csv('soccer-spi/spi_matches.csv')
    proj_scores_df = proj_scores_df[proj_scores_df['league_id']==2411]

    for season in seasons:
        for row in tqdm(range(len(player_info_dict[season]))): 
            
            main_df = player_info_dict[season][row][0]
            understat_df = player_info_dict[season][row][1]
            player_id = main_df['element'].iloc[0]
            teamid = team_id(player_id, season, players_raw)
            team_name = teams[season].iloc[teamid-1, 5]

            # Change some things in the dataframe
            main_df = main_df.drop(['creativity', 'ict_index', 'goals_scored', 'influence', 'threat', 'saves', 'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards', 'yellow_cards', 'bonus', 'bps', 'assists', 'clean_sheets', 'goals_conceded', 'team_a_score', 'team_h_score', 'transfers_balance', 'transfers_in', 'transfers_out', 'selected'], axis=1)

            main_df['opponent_team'] = [teams[season].iloc[main_df['opponent_team'][x]-1, 5] for x in range(main_df.shape[0])]
            main_df.insert(0, 'spi_team', [spis(proj_scores_df, team_name, main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[0] for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_spi_team', [spis(proj_scores_df, team_name, main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[1] for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_npxGAp90', [npxGAp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGp90(L4)', [last4npxGp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGp90', [npxGp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'shp90', [shp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'teamnpxGp90', [opp_npxGp90(team(main_df['fixture'][x], main_df['was_home'][x], season, teams, fixtures), main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npg_ratel100', [rates100(understat_df, main_df['kickoff_time'][x], 'npg') for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGp90l100', [rates100(understat_df, main_df['kickoff_time'][x], 'npxG') for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'sh_ratel100', [rates100(understat_df, main_df['kickoff_time'][x], 'shots') for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npg_rate', [npg_rate_season(understat_df, main_df['kickoff_time'][x], int(season[:4])) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npg', npg(main_df, understat_df, int(season[:4])), True)
            main_df.insert(0, 'proj_goals', [proj_scores(proj_scores_df, team_name, main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[0] for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_proj_goals', [proj_scores(proj_scores_df, team_name, main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[1] for x in range(main_df.shape[0])], True)

            main_df = main_df.drop(['fixture', 'opponent_team'], axis=1)
            gframes.append(main_df)
    
    # some data cleaning
    data = pd.concat(gframes)
    data = data.drop(['round', 'value', 'element', 'kickoff_time', 'total_points'], axis=1)

    cols = data.columns.tolist()
    cols = [cols[6], cols[5], cols[4], cols[3], cols[9], cols[10], cols[8], cols[7], cols[11], cols[12], cols[13], cols[14], cols[15], cols[0], cols[1], cols[2]] 
    data = data[cols]

    data = data.dropna()
    data = data[data['spi_team'] > 0]
    print('Dataset size: ' ,data.shape)
    #data = data[data['minutes'] != 0]

    return data


def penalties_dataset_creation(seasons, fixtures, teams, team_stats_dict, gw_no_limit):
    frames = []
    proj_scores_df = pd.read_csv('soccer-spi/spi_matches.csv')
    proj_scores_df = proj_scores_df[proj_scores_df['league_id']==2411]
    for season in seasons:
        for team_id in tqdm(range(1,21)):
            fix = fixtures[season]
            team_fixtures = fix[(fix['team_h']==team_id) | (fix['team_a']==team_id)]
            team = teams[season].iloc[team_id-1, 5]
            team_df = team_stats_dict[season][team]
            pens, cnt = pens_per_game(fixtures, season, team_stats_dict, teams, team_id, gw_no_limit)
            for i in range(team_df.shape[0]):
                data = pd.DataFrame()
                kickoff_time = team_fixtures['kickoff_time'].iloc[i+cnt]
                if team_id == team_fixtures['team_h'].iloc[i+cnt]:
                    home = True
                    opp_team = teams[season].iloc[team_fixtures['team_a'].iloc[i+cnt]-1, 5]
                else:
                    home = False
                    opp_team = teams[season].iloc[team_fixtures['team_h'].iloc[i+cnt]-1, 5]

                data.insert(0, 'team_npxG', [opp_npxGp90(team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
                data.insert(1, 'oppteam_npxGA', [npxGAp90(opp_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
                data.insert(2, 'was_home', [home], True)
                data.insert(3, 'pen_rate', [avg(pens[:i])], True)
                data.insert(4, 'proj_goals', [proj_scores(team, opp_team, int(season[:4]), home)[0]], True)
                data.insert(5, 'spi_team', [spis(proj_scores_df, team, opp_team, int(season[:4]), home)[0]])
                data.insert(6, 'spi_opp_team', [spis(proj_scores_df, team, opp_team, int(season[:4]), home)[1]])
                data.insert(7, 'team_npxGp90(L4)', [opp_last4npxGp90(team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
                data.insert(8, 'oppteam_npxGAp90(L4)', [last4npxGAp90(opp_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
                data.insert(9, 'team_pens', [pens[i]], True)
                frames.append(data)
    data = pd.concat(frames)
    data = data.dropna()
    data = data[data['spi_team'] > 0]
    return data

 
def assists_dataset_creation(seasons, player_info_dict, teams, players_raw, team_stats_dict, fixtures, gw_no_limit):
    aframes = []
    proj_scores_df = pd.read_csv('soccer-spi/spi_matches.csv')
    proj_scores_df = proj_scores_df[proj_scores_df['league_id']==2411]
    for season in seasons:
        for row in tqdm(range(len(player_info_dict[season]))): 
            
            main_df = player_info_dict[season][row][0]
            understat_df = player_info_dict[season][row][1]
            player_id = main_df['element'].iloc[0]
            teamid = team_id(player_id, season, players_raw)
            team_name = teams[season].iloc[teamid-1, 5]
            main_df = main_df.drop(['creativity', 'ict_index', 'influence', 'threat', 'saves', 'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards', 'yellow_cards', 'bonus', 'bps', 'goals_scored', 'clean_sheets', 'goals_conceded', 'team_a_score', 'team_h_score', 'transfers_balance', 'transfers_in', 'transfers_out', 'selected'], axis=1)

            main_df['opponent_team'] = [teams[season].iloc[main_df['opponent_team'][x]-1, 5] for x in range(main_df.shape[0])]
            main_df.insert(0, 'opp_npxGAp90', [npxGAp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True) 
            main_df.insert(0, 'spi_team', [spis(proj_scores_df, team_name, main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[0] for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'spi_opp_team', [spis(proj_scores_df, team_name, main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[1] for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'xAp90(L4)', [last4xAp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'kpp90', [kpp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'teamnpxGp90', [opp_npxGp90(team(main_df['fixture'][x], main_df['was_home'][x], season, teams, fixtures), main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'xAp90', [xAp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_npxGp90', [opp_npxGp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'assist_rate', [assist_rate_season(understat_df, main_df['kickoff_time'][x], int(season[:4])) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'assist_ratel100', [rates100(understat_df, main_df['kickoff_time'][x], 'assists') for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'xAp90l100', [rates100(understat_df, main_df['kickoff_time'][x], 'xA') for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'kp_ratel100', [rates100(understat_df, main_df['kickoff_time'][x], 'key_passes') for x in range(main_df.shape[0])], True)

            main_df = main_df.drop(['fixture', 'opponent_team'], axis=1)
            aframes.append(main_df)

    data = pd.concat(aframes)
    data = data.drop(['round', 'value', 'element', 'kickoff_time', 'total_points'], axis=1)

    cols = data.columns.tolist()
    cols = [cols[2], cols[1], cols[0], cols[3], cols[5], cols[8], cols[7], cols[6], cols[4], cols[9], cols[11], cols[10], cols[13], cols[14], cols[12]] 
    data = data[cols]

    data = data.dropna()
    data = data[data['spi_team'] > 0]
    print('Dataset size: ' ,data.shape)
    #data = data[data['minutes'] != 0]

    return data

def team_goals_dataset_creation(seasons, fixtures, teams, team_stats_dict, gw_no_limit):
    frames = []
    for season in seasons:
        for x in tqdm(range(fixtures[season].shape[0])):
            if not fixtures[season]['finished'][x]:
                break
            data = pd.DataFrame()
            home_team = teams[season].iloc[fixtures[season]['team_h'][x]-1, 5]
            away_team = teams[season].iloc[fixtures[season]['team_a'][x]-1, 5]
            kickoff_time = fixtures[season]['kickoff_time'][x]

            data.insert(0, 'team1_npxG', [opp_npxGp90(home_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(1, 'team2_npxGA', [npxGAp90(away_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(2, 'was_home', [True], True)
            data.insert(3, 'team1_npxGp90(L4)', [opp_last4npxGp90(home_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(4, 'team2_npxGAp90(L4)', [last4npxGAp90(away_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(5, 'team1_goals', [fixtures[season]['team_h_score'][x]], True)
            frames.append(data)

            data = pd.DataFrame()
            data.insert(0, 'team1_npxG', [opp_npxGp90(away_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(1, 'team2_npxGA', [npxGAp90(home_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(2, 'was_home', [False], True)
            data.insert(3, 'team1_npxGp90(L4)', [opp_last4npxGp90(away_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(4, 'team2_npxGAp90(L4)', [last4npxGAp90(home_team, kickoff_time, season, team_stats_dict, gw_no_limit)], True)
            data.insert(5, 'team1_goals', [fixtures[season]['team_a_score'][x]], True)
            frames.append(data)

    data = pd.concat(frames)
    data = data.dropna()
    return data


def bps_dataset_creation(seasons, player_info_dict, teams, players_raw, team_stats_dict, fixtures, gw_no_limit):
    frames = []
    for season in seasons:
        for row in tqdm(range(len(player_info_dict[season]))): 
            
            main_df = player_info_dict[season][row][0]
            understat_df = player_info_dict[season][row][1]

            # Change some things in the dataframe
            main_df = main_df.drop(['creativity', 'ict_index', 'influence', 'threat', 'saves', 'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards', 'yellow_cards', 'bps', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'team_a_score', 'team_h_score', 'transfers_balance', 'transfers_in', 'transfers_out', 'selected'], axis=1)

            main_df['opponent_team'] = [teams[season].iloc[main_df['opponent_team'][x]-1, 5] for x in range(main_df.shape[0])]
            main_df.insert(0, 'opp_npxGAp90', [npxGAp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGp90', [npxGp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'xAp90', [xAp90(understat_df, int(season[:4]), main_df['kickoff_time'][x], gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'position', [int(players_raw[season][players_raw[season]['id'] == int(main_df['element'].iloc[0])]['element_type']) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_npxGp90', [opp_npxGp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGAp90', [npxGAp90(team(main_df['fixture'][x], main_df['was_home'][x], season, teams, fixtures), main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            #main_df.insert(0, 'bonusp90', [main_df['bonus'].iloc[:x].mean() for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'bonusp90', [p90_main_df(main_df, 'bonus', x) for x in range(main_df.shape[0])], True)

            main_df = main_df.drop(['fixture', 'opponent_team'], axis=1)
            frames.append(main_df)

    data = pd.concat(frames)
    data = data.drop(['round', 'value', 'element', 'kickoff_time', 'total_points'], axis=1)

    cols = data.columns.tolist()
    cols = [cols[0], cols[3], cols[5], cols[4], cols[1], cols[2], cols[6], cols[8], cols[9], cols[7]] 
    data = data[cols]
    data = data.dropna()
    return data


def saves_dataset_creation(seasons, player_info_dict, players_raw, teams, team_stats_dict, fixtures, gw_no_limit):
    frames = []
    for season in seasons:
        for row in tqdm(range(len(player_info_dict[season]))): 
            main_df = player_info_dict[season][row][0]
            pos = int(players_raw[season][players_raw[season]['id'] == int(main_df['element'].iloc[0])]['element_type'])
            if pos != 1:
                continue

            main_df = main_df.drop(['creativity', 'ict_index', 'influence', 'threat', 'bonus', 'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards', 'yellow_cards', 'bps', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 'team_a_score', 'team_h_score', 'transfers_balance', 'transfers_in', 'transfers_out', 'selected'], axis=1)
            main_df['opponent_team'] = [teams[season].iloc[main_df['opponent_team'][x]-1, 5] for x in range(main_df.shape[0])]
            main_df.insert(0, 'opp_npxGp90(L4)', [opp_last4npxGp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_npxGp90', [opp_npxGp90(main_df['opponent_team'][x], main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGAp90(L4)', [last4npxGAp90(team(main_df['fixture'][x], main_df['was_home'][x], season, teams, fixtures), main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'npxGAp90', [npxGAp90(team(main_df['fixture'][x], main_df['was_home'][x], season, teams, fixtures), main_df['kickoff_time'][x], season, team_stats_dict, gw_no_limit) for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'opp_proj_goals', [proj_scores(team(main_df['fixture'][x], main_df['was_home'][x], season, teams, fixtures), main_df['opponent_team'][x], int(season[:4]), main_df['was_home'][x])[1] for x in range(main_df.shape[0])], True)
            main_df.insert(0, 'savesp90', [p90_main_df(main_df, 'saves', x) for x in range(main_df.shape[0])], True)

            main_df = main_df.drop(['fixture', 'opponent_team'], axis=1)
            frames.append(main_df)

    data = pd.concat(frames)
    data = data.drop(['round', 'value', 'element', 'kickoff_time', 'total_points'], axis=1)

    cols = data.columns.tolist()
    cols = [cols[0], cols[1], cols[2], cols[4], cols[3], cols[5], cols[6], cols[8], cols[7]] 
    data = data[cols]
    data = data.dropna()
    return data



def pens_dataset_creation():
    df = pd.read_html('https://fbref.com/en/comps/9/1631/2017-2018-Premier-League-Stats')[8]
    df.columns = df.columns.droplevel()
    df = df[['Squad', 'Sh/90', 'PKatt', 'npxG']]
    pen_area_touches = pd.read_html('https://fbref.com/en/comps/9/1631/2017-2018-Premier-League-Stats')[18]
    pen_area_touches.columns= pen_area_touches.columns.droplevel()
    pen_area_touches = pen_area_touches[['Squad', 'Att Pen']]
    df_2017 = df.merge(pen_area_touches, on='Squad', how='left')
    time.sleep(10)

    df = pd.read_html('https://fbref.com/en/comps/9/1889/2018-2019-Premier-League-Stats')[8]
    df.columns = df.columns.droplevel()
    df = df[['Squad', 'Sh/90', 'PKatt', 'npxG']]
    pen_area_touches = pd.read_html('https://fbref.com/en/comps/9/1889/2018-2019-Premier-League-Stats')[18]
    pen_area_touches.columns= pen_area_touches.columns.droplevel()
    pen_area_touches = pen_area_touches[['Squad', 'Att Pen']]
    df_2018 = df.merge(pen_area_touches, on='Squad', how='left')
    time.sleep(20)

    df = pd.read_html('https://fbref.com/en/comps/9/3232/2019-2020-Premier-League-Stats')[8]
    df.columns = df.columns.droplevel()
    df = df[['Squad', 'Sh/90', 'PKatt', 'npxG']]
    pen_area_touches = pd.read_html('https://fbref.com/en/comps/9/3232/2019-2020-Premier-League-Stats')[18]
    pen_area_touches.columns= pen_area_touches.columns.droplevel()
    pen_area_touches = pen_area_touches[['Squad', 'Att Pen']]
    df_2019 = df.merge(pen_area_touches, on='Squad', how='left')
    time.sleep(40)

    df = pd.read_html('https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats')[8]
    df.columns = df.columns.droplevel()
    df = df[['Squad', 'Sh/90', 'PKatt', 'npxG']]
    pen_area_touches = pd.read_html('https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats')[18]
    pen_area_touches.columns= pen_area_touches.columns.droplevel()
    pen_area_touches = pen_area_touches[['Squad', 'Att Pen']]
    df_2020 = df.merge(pen_area_touches, on='Squad', how='left')
    time.sleep(80)

    df = pd.read_html('https://fbref.com/en/comps/9/11160/2021-2022-Premier-League-Stats')[8]
    df.columns = df.columns.droplevel()
    df = df[['Squad', 'Sh/90', 'PKatt', 'npxG']]
    pen_area_touches = pd.read_html('https://fbref.com/en/comps/9/11160/2021-2022-Premier-League-Stats')[18]
    pen_area_touches.columns= pen_area_touches.columns.droplevel()
    pen_area_touches = pen_area_touches[['Squad', 'Att Pen']]
    df_2021 = df.merge(pen_area_touches, on='Squad', how='left')

    df_2017 = df_2017.merge(df_2018.drop(['npxG', 'Sh/90', 'Att Pen'], axis=1), on='Squad', how='inner')
    df_2017.rename(columns = {'PKatt_x':'prev_pens', 'PKatt_y':'pens'}, inplace = True)

    df_2018 = df_2018.merge(df_2019.drop(['npxG', 'Sh/90', 'Att Pen'], axis=1), on='Squad', how='inner')
    df_2018.rename(columns = {'PKatt_x':'prev_pens', 'PKatt_y':'pens'}, inplace = True)

    df_2019 = df_2019.merge(df_2020.drop(['npxG', 'Sh/90', 'Att Pen'], axis=1), on='Squad', how='inner')
    df_2019.rename(columns = {'PKatt_x':'prev_pens', 'PKatt_y':'pens'}, inplace = True)

    df_2020 = df_2020.merge(df_2021.drop(['npxG', 'Sh/90', 'Att Pen'], axis=1), on='Squad', how='inner')
    df_2020.rename(columns = {'PKatt_x':'prev_pens', 'PKatt_y':'pens'}, inplace = True)

    data = pd.concat([df_2017, df_2018, df_2019, df_2020])
    data = data.drop(['Squad'], axis=1)
    cols = data.columns.tolist()
    #cols = [cols[2], cols[4], cols[3], cols[1], cols[5], cols[6], cols[7], cols[0]] 
    data = data[cols]
    data = data.dropna()

    return data, df_2021



def spi_dataset_creation(matches_path):
    matches = pd.read_csv(matches_path)
    pl_matches = matches[matches['league_id']==2411]
    df1 = pl_matches[['spi1', 'spi2', 'score1', 'score2', 'xg1', 'xg2']]
    df2 = df1.rename(columns={'spi1': 'spi2', 'spi2': 'spi1', 'score1': 'score2', 'score2': 'score1', 'xg1': 'xg2', 'xg2': 'xg1'})
    df2 = df2[['spi1', 'spi2', 'score1', 'score2', 'xg1', 'xg2']]
    df2.insert(6, 'was_home', [False]*df2.shape[0], True)
    df1.insert(6, 'was_home', [True]*df1.shape[0], True)
    df1.insert(7, 'next_spi', [next_spi(pl_matches, pl_matches['team1'].iloc[x], pl_matches['date'].iloc[x]) for x in range(pl_matches.shape[0])], True)
    df2.insert(7, 'next_spi', [next_spi(pl_matches, pl_matches['team2'].iloc[x], pl_matches['date'].iloc[x]) for x in range(pl_matches.shape[0])], True)
    data = df1.append(df2, ignore_index=True).dropna()
    return data

def proj_goals_dataset_creation(matches_path):
    matches = pd.read_csv(matches_path)
    pl_matches = matches[matches['league_id']==2411]
    df1 = pl_matches[['spi1', 'spi2']]
    df2 = df1.rename(columns={'spi1': 'spi2', 'spi2': 'spi1'})
    df2 = df2[['spi1', 'spi2']]
    df2.insert(2, 'was_home', [False]*df2.shape[0], True)
    df1.insert(2, 'was_home', [True]*df1.shape[0], True)
    df1.insert(3, 'proj_goals', [pl_matches['proj_score1'].iloc[x] for x in range(pl_matches.shape[0])], True)
    df2.insert(3, 'proj_goals', [pl_matches['proj_score2'].iloc[x] for x in range(pl_matches.shape[0])], True)
    data = df1.append(df2, ignore_index=True).dropna()
    return data