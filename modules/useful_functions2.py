import pandas as pd
import numpy as np
from tqdm import tqdm
from modules.useful_functions import npg, pens_per_game, xpens_2022, save_points, minus_points_def, clean_sheets, xAppPoints, el_per_app, finishing_rate, penalty_finishing_rate, fixture_info, team_id, convert, previous, npxGAp90, last4npxGp90, npxGp90, shp90, opp_npxGp90, xAp90, kpp90, last4xAp90, opp_last4npxGp90, last4npxGAp90
from modules.useful_functions import p90_main_df, avg, rates100, npg_rate_season, assist_rate_season


is_home = {
    'H': True,
    'A': False
}

def add_fixture(fixtures, season, fix_prob, gw, idd, team_h, team_a):
    adjusted_fixtures = fixtures
    adj_fix = fixtures[season]
    if 'fix_prob' not in adj_fix:
        adj_fix.insert(0, 'fix_prob', [1] * adj_fix.shape[0], True)
    if ((adj_fix.team_h == team_h) & (adj_fix.team_a == team_a) & (adj_fix.event == gw)).any():
        i = adj_fix[((adj_fix.team_h == team_h) & (adj_fix.team_a == team_a) & (adj_fix.event == gw))].index
        adj_fix.at[i, 'fix_prob'] = fix_prob
        return adjusted_fixtures

    adj_fix.loc[len(adj_fix.index)] = [fix_prob, 0, gw, False, False, idd, '2023-05-28T15:00:00Z', 0, False, False, team_a, np.NaN, team_h, np.NaN, '[]', 0, 0, 0]
    return adjusted_fixtures


def adjust_fixtures(review_detailed, fixtures, teams, season, gws):
    teams_df = teams[season]
    review_detailed = review_detailed[review_detailed[str(gws[0])+'_xmins']!=0]
    l = []
    m = []
    for gw in gws:
        l.append(str(gw)+'_fix')
        m.append(str(gw)+'_likelihood')
    review_detailed[l] = review_detailed[l].fillna('')
    review_detailed[m] = review_detailed[m].fillna('0')
    idd = 1000
    for i in range(20):
        df = review_detailed.drop_duplicates(subset='Team', keep='first').iloc[i]
        for gw in gws:
            f_info = df[str(gw)+'_fix'].split('(')
            fp_info = df[str(gw)+'_likelihood'].split()
            '''
            if len(f_info)-1 == 0:
                opp_team = fixture_info2(i, season, gw, fixtures, teams)[0][0]
                home = fixture_info2(i, season, gw, fixtures, teams)[0][1]
                if home:
                    fixtures = add_fixture(fixtures, season, float(fp_info[i]), gw, idd, i, teams_df[teams_df['name']==opp_team]['id'].iloc[0])
                else:
                    fixtures = add_fixture(fixtures, season, float(fp_info[i]), gw, idd, teams_df[teams_df['name']==opp_team]['id'].iloc[0], i)
                idd = idd + 1
            '''
            for i in range(len(f_info)-1):
                if is_home[f_info[i+1][0]]:
                    team_h = teams_df[teams_df['short_name']==df['Team']]['id'].iloc[0]
                    team_a = teams_df[teams_df['short_name']==f_info[i+1][4:]]['id'].iloc[0]
                else:
                    team_a = teams_df[teams_df['short_name']==df['Team']]['id'].iloc[0]
                    team_h = teams_df[teams_df['short_name']==f_info[i+1][4:]]['id'].iloc[0]   
                fixtures = add_fixture(fixtures, season, float(fp_info[i]), gw, idd, team_h, team_a)
                idd = idd + 1
    return fixtures


teams538 = {
    'Arsenal': 'Arsenal',
    'Aston Villa': 'Aston Villa',
    'Bournemouth': 'AFC Bournemouth',
    'Brentford': 'Brentford',
    'Brighton': 'Brighton and Hove Albion',
    'Chelsea': 'Chelsea',
    'Crystal Palace': 'Crystal Palace',
    'Everton': 'Everton',
    'Fulham': 'Fulham',
    'Leicester': 'Leicester City',
    'Leeds': 'Leeds United',
    'Liverpool': 'Liverpool',
    'Man City': 'Manchester City',
    'Man Utd': 'Manchester United',
    'Newcastle': 'Newcastle',
    'Nott\'m Forest': 'Nottingham Forest',
    'Southampton': 'Southampton',
    'Spurs': 'Tottenham Hotspur',
    'West Ham': 'West Ham United',
    'Wolves': 'Wolverhampton',
    'Watford': 'Watford',
    'Norwich': 'Norwich City',
    'Burnley': 'Burnley',
    'West Brom' : 'West Bromwich Albion',
    'Sheffield Utd': 'Sheffield United'
}


def proj_scores(team_1, team_2, season, home):
    proj_scores_df = pd.read_csv('soccer-spi/spi_matches.csv')
    proj_scores_df = proj_scores_df[proj_scores_df['league_id']==2411]
    df = proj_scores_df[proj_scores_df['season']==season]
    if home:
        df = df[(df['team1']==teams538[team_1]) & (df['team2']==teams538[team_2])]
        xg1 = float(df['proj_score1'])
        xg2 = float(df['proj_score2'])
        return xg1,xg2
    else:
        df = df[(df['team1']==teams538[team_2]) & (df['team2']==teams538[team_1])]
        xg1 = float(df['proj_score1'].iloc[0])
        xg2 = float(df['proj_score2'].iloc[0])
        return xg2,xg1 

def prev_rate(PATH, season, fpl_str, gw, gw_no_lim, el):
    if el == 'bonus':
        try:
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            if gw >= gw_no_lim:
                ret_value = p90_main_df(main_df, el, gw)
                return ret_value
            else:
                raise Exception()
        except:
            try:
                history_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/history.csv')
                ret_value = 90*sum(history_df['bonus'].to_list())/sum(history_df['minutes'].to_list())
                return ret_value
            except:
                ret_value = 0.3
                return ret_value
    elif el == 'saves':
        try:
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            if gw >= gw_no_lim:
                ret_value = p90_main_df(main_df, el, gw)
                return ret_value
            else:
                raise Exception()
        except:
            try:
                history_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/history.csv')
                ret_value = 90*sum(history_df['saves'].to_list())/sum(history_df['minutes'].to_list())
                return ret_value
            except:
                ret_value = 2.5
                return ret_value
    elif el == 'yc':
        try:
            main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            if gw >= gw_no_lim:
                ret_value = el_per_app(main_df, gw, el)
                return ret_value
            else:
                raise Exception()
        except:
            try:
                history_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/history.csv')
                ret_value = 90*sum(history_df['yellow_cards'].to_list())/sum(history_df['minutes'].to_list())
                return ret_value
            except:
                ret_value = 0.15
                return ret_value



def xPoints(df, npgoals, assists, team_goals, bonus, saves, pens, x): 
    points = pd.DataFrame()
    try:
        position = df['position'][x]
        npxGp90 = df['npxGp90'][x]
        npxGp90l4 = df['npxGp90(L4)'][x]
        npxGAp90 = df['npxGAp90'][x]
        shp90 = df['shp90'][x]
        kpp90 = df['kpp90'][x]
        teamnpxGp90 = df['teamnpxGp90'][x]
        oppnpxGAp90 = df['opp_npxGAp90'][x]
        team_proj_goals = df['team_proj_goals'][x]
        opp_proj_goals = df['opp_proj_goals'][x]
        xAp90 = df['xAp90'][x]
        xAp90l4 = df['xAp90(L4)'][x]
        mins = df['minutes'][x]
        oppnpxGp90l4 = df['opp_npxGp90l4'][x]
        npxGAp90l4 = df['npxGAp90l4'][x]
        team = df['team'][x]
        player_id = df['id'][x]
        home = df['was_home'][x]
        oppnpxGp90 = df['opp_npxGp90'][x]
        teamnpxGp90l4 = df['teamnpxGp90l4'][x]
        oppnpxGAp90l4 = df['opp_npxGAp90l4'][x]
        pen_rate = df['pen_rate'][x]
        bonusp90 = df['bonusp90'][x]
        finishing_rate = df['finishing_rate'][x]
        penalty_finishing_rate = df['penalty_finishing_rate'][x]
        xYC = df['xYC'][x]
        npg_rate = df['npg_rate'][x]
        assist_rate = df['assist_rate'][x]
        assist_ratel100 = df['assist_ratel100'][x] 
        xAp90l100 = df['xAp90l100'][x]
        kp_ratel100 = df['kp_ratel100'][x]
        npg_ratel100 = df['npg_ratel100'][x]
        npxGp90l100 = df['npxGp90l100'][x]
        sh_ratel100 = df['sh_ratel100'][x]
        savesp90 = df['savesp90'][x]

        app = xAppPoints(int(mins))[0]
        chance60 = xAppPoints(int(mins))[1]

        xpen_goals = 0
        miss_pen_points = 0
        xg_pen = 0.79
        xpens = pens.predict([[teamnpxGp90, oppnpxGAp90, home, pen_rate, team_proj_goals, teamnpxGp90l4, oppnpxGAp90l4]])[0]
        pen_takers = xpens_2022[team]

        for x in range(len(pen_takers)):
            if pen_takers[x][0] == player_id:
                xpen_goals = (mins/90)*pen_takers[x][1] * xpens* xg_pen * penalty_finishing_rate  # pen_takers[x][1] is the chance of the player being 1st choice pen taker
                #miss_pen_points = -2*xpens*(1-xg_pen*penalty_finishing_rate)
                
        xGoals = npgoals.predict([[npg_ratel100, npxGp90l100, sh_ratel100, npg_rate, npxGp90, npxGp90l4, shp90, teamnpxGp90, oppnpxGAp90, mins, home]])[0] + xpen_goals
        xAssists = assists.predict([[assist_ratel100, xAp90l100, kp_ratel100, assist_rate, xAp90, xAp90l4, kpp90, teamnpxGp90, oppnpxGp90, oppnpxGAp90, mins, home]])[0]
        #xCS = clean_sheets(team_goals.predict([[oppnpxGp90, npxGAp90, home, oppnpxGp90l4, npxGAp90l4]])[0])
        xCS = clean_sheets(opp_proj_goals)
        xBonus = bonus.predict([[bonusp90, position, npxGp90, xAp90, npxGAp90, oppnpxGp90, oppnpxGAp90, mins, home]])[0]
        #xMinus_def = minus_points_def(team_goals.predict([[oppnpxGp90, npxGAp90, home, oppnpxGp90l4, npxGAp90l4]])[0])
        xMinus_def = minus_points_def(opp_proj_goals)
        xSave_points = save_points(saves.predict([[savesp90, opp_proj_goals, npxGAp90, oppnpxGp90, npxGAp90l4, oppnpxGp90l4, mins, home]])[0])

        points.insert(0, 'goals', [xGoals], True)
        points.insert(1, 'assists', [xAssists], True)
        points.insert(2, 'CS', [chance60*xCS], True)
        points.insert(3, 'md', [chance60*xMinus_def], True)
        points.insert(4, 'bonus', [xBonus], True)
        points.insert(5, 'appearance', [app], True)
        points.insert(6, 'saves', [xSave_points], True)
        points.insert(7, 'yellow_cards', [xYC], True)
        points.insert(8, 'pen_miss_points', [miss_pen_points], True)

        if position == 1:
            total = app + 3*xAssists + 4*chance60*xCS + xBonus + chance60*xMinus_def + xSave_points - xYC + miss_pen_points
        if position == 2:
            total = app + 6*xGoals + 3*xAssists + 4*chance60*xCS + xBonus + chance60*xMinus_def - xYC + miss_pen_points
        if position == 3:
            total = app + 5*xGoals + 3*xAssists + chance60*xCS + xBonus - xYC + miss_pen_points
        if position == 4:
            total = app + 4*xGoals + 3*xAssists + xBonus - xYC + miss_pen_points

        points.insert(9, 'total', [total], True)

        return points
        
    except:
        points.insert(0, 'goals', [0.0], True)
        points.insert(1, 'assists', [0.0], True)
        points.insert(2, 'CS', [0.0], True)
        points.insert(3, 'md', [0.0], True)
        points.insert(4, 'bonus', [0.0], True)
        points.insert(5, 'appearance', [0.0], True)
        points.insert(6, 'saves', [0.0], True)
        points.insert(7, 'yellow_cards', [0.0], True)
        points.insert(8, 'pen_miss_points', [0.0], True)
        points.insert(9, 'total', [0.0], True)
        return points
        
        

def compute_ev(next_gw, horizon, review_horizon, season, review_df, review_detailed, players_raw, ids, id_dict_df, fpl_str_df_path, PATH, fixtures, teams, team_stats_dict, xpens_2022, npgoals, assists, team_goals, bonus, saves, gw_no_lim, seasons):
    xpoints = {}
    for q in range(horizon):
        xpoints['gw_'+str(next_gw+q)] = []
    mins = {}
    for q in range(horizon):
        mins['gw_'+str(next_gw+q)] = []
    total = []
    xmins = []
    fpl_id = ids[season]
    #review_df = review_df[:5]      #for tests
    for player_id in tqdm(review_df['ID'].to_list()): 
        try:
            name = players_raw[season][players_raw[season]['id']==player_id]['web_name'].iloc[0]
            row = id_dict_df[id_dict_df[fpl_id]==player_id].index[0]
            gws = list(range(next_gw, next_gw + horizon))
            xmins = []
            xp = []
            for q in range(horizon):
                try:
                    xmins.append(list(map(float, str(review_detailed[review_detailed['ID']==player_id][str(gws[q])+'_dmins'].iloc[0]).split())))
                except:
                    xmins.append(list(map(float, str(review_detailed[review_detailed['ID']==player_id][str(next_gw + review_horizon - 1)+'_dmins'].iloc[0]).split())))
            df = pd.DataFrame()

            understat_str = convert(str(id_dict_df.iloc[row]['Understat_Name'])) + '_' + str(id_dict_df.iloc[row]['Understat_ID']) + '.csv'
            #fpl_str_prev = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][ids[previous(season)]])
            try:
                fpl_str = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][ids[season]])
                main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            except:
                fpl_str_df = pd.read_csv(fpl_str_df_path)
                fpl_str_df = fpl_str_df[fpl_str_df['22-23']==player_id]
                fpl_str = fpl_str_df['first_name'].iloc[0] + '_' + fpl_str_df['second_name'].iloc[0] + '_' + str(fpl_str_df['22-23'].iloc[0])
            understat_df = pd.read_csv(PATH + season + '/understat/' + understat_str)

            for gw in gws:
                opponent_team = []
                home = []
                kickoff_time = []
                xp_gw = []
                bpm = prev_rate(PATH, season, fpl_str, gw, gw_no_lim, 'bonus')
                yc = prev_rate(PATH, season, fpl_str, gw, gw_no_lim, 'yc')
                team_name = teams[season].iloc[team_id(player_id, season, players_raw)-1, 5]
                fix = fixture_info(player_id, season, gw, fixtures, teams, players_raw)
                for i in range(len(fix)):
                    cmp_df = pd.DataFrame()
                    opponent_team.append(fix[i][0])
                    home.append(fix[i][1])
                    kickoff_time.append(fix[i][2])   

                    pos = int(players_raw[season][players_raw[season]['id'] == int(id_dict_df.iloc[row][fpl_id])]['element_type'])
            
                    cmp_df.insert(0, 'opp_npxGAp90', [npxGAp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGp90(L4)', [last4npxGp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'xAp90(L4)', [last4xAp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGp90', [npxGp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'xAp90', [xAp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'position', [pos], True)
                    cmp_df.insert(0, 'opp_npxGp90l4', [opp_last4npxGp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'opp_npxGp90', [opp_npxGp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGAp90l4', [last4npxGAp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGAp90', [npxGAp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'kpp90', [kpp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'shp90', [shp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'teamnpxGp90', [opp_npxGp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'team_proj_goals', [proj_scores(team_name, opponent_team[i], int(season[:4]), home[i])[0]], True)
                    cmp_df.insert(0, 'opp_proj_goals', [proj_scores(team_name, opponent_team[i], int(season[:4]), home[i])[1]], True)
                    cmp_df.insert(0, 'bonusp90', [bpm], True) 
                    cmp_df.insert(0, 'was_home', [home[i]], True)
                    cmp_df.insert(0, 'xYC', [yc], True)
                    cmp_df.insert(0, 'team', [team_name], True)
                    cmp_df.insert(0, 'id', [player_id], True)
                    cmp_df.insert(0, 'minutes', [xmins[gw-gws[0]][i]], True)
                    cmp_df.insert(0, 'finishing_rate', [finishing_rate(understat_df)], True)
                    cmp_df.insert(0, 'penalty_finishing_rate', [penalty_finishing_rate(understat_df)], True)

                    points_df = xPoints(cmp_df,xpens_2022,npgoals, assists, team_goals, bonus, saves, 0)
                    xp_gw.append(points_df['total'][0])
                xp.append(xp_gw)
            
            tot = 0
            for q in range(horizon):
                xpoints['gw_'+str(next_gw+q)].append(round(sum(xp[q]),2))
                tot += sum(xp[q])
            total.append(round(tot,2))
            
        except:
            for q in range(horizon):
                xpoints['gw_'+str(next_gw+q)].append(0)
                mins['gw_'+str(next_gw+q)].append(0)
            total.append(0)
            
    for q in range(horizon):
        try:
            review_df.insert(7+3*q, str(next_gw+q)+'_xP', xpoints['gw_'+str(next_gw+q)], True)
        except:
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xMins', xmins[q], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xP', xpoints['gw_'+str(next_gw+q)], True)
    review_df.insert(len(review_df.keys()), 'total', total, True)

    for q in range(horizon):
        try:
            review_df.drop([str(next_gw+q)+'_Pts'], axis=1, inplace=True)
            review_df.rename(columns={str(next_gw+q)+'_xP': str(next_gw+q)+'_Pts'}, inplace=True)
        except:
            review_df.rename(columns={str(next_gw+q)+'_xP': str(next_gw+q)+'_Pts'}, inplace=True)
    
    review_df = review_df.iloc[:,list(range((5+2*horizon+1))) + [-1]]
    return review_df


def compute_analytical_ev(next_gw, horizon, review_horizon, season, review_df, review_detailed, players_raw, ids, id_dict_df, fpl_str_df_path, PATH, fixtures, teams, team_stats_dict, npgoals, assists, team_goals, bonus, saves, pens, gw_no_lim, seasons):
    xpoints = {}
    xbp = {}
    xgoals = {}
    xassists = {}
    xcs = {}
    xmd = {}
    xsave_points = {}
    xapp = {}
    xpm = {}
    xyc = {}
    for q in range(horizon):
        xpoints['gw_'+str(next_gw+q)] = []
        xgoals['gw_'+str(next_gw+q)] = []
        xassists['gw_'+str(next_gw+q)] = []
        xbp['gw_'+str(next_gw+q)] = []
        xcs['gw_'+str(next_gw+q)] = []
        xmd['gw_'+str(next_gw+q)] = []
        xpm['gw_'+str(next_gw+q)] = []
        xyc['gw_'+str(next_gw+q)] = []
        xapp['gw_'+str(next_gw+q)] = []
        xsave_points['gw_'+str(next_gw+q)] = []
    mins = {}
    for q in range(horizon):
        mins['gw_'+str(next_gw+q)] = []
    total = []
    xmins = []
    fpl_id = ids[season]
    gws = list(range(next_gw, next_gw + horizon))
    # Update fixture probabilities
    fixtures = adjust_fixtures(review_detailed, fixtures, teams, season, gws)
    #review_df = review_df[:5]      #for tests
    for player_id in tqdm(review_df['ID'].to_list()): 
        try:
            name = players_raw[season][players_raw[season]['id']==player_id]['web_name'].iloc[0]
            row = id_dict_df[id_dict_df[fpl_id]==player_id].index[0]
            #pos = review_df[review_df['ID']==player_id]['Pos'].iloc[0]
            xmins = []
            xp = []
            xg = []
            xa = []
            cs = []
            md = []
            ycc = []
            save_points = []
            app = []
            bp = []
            pm = []
            for q in range(horizon):
                try:
                    xmins.append(list(map(float, str(review_detailed[review_detailed['ID']==player_id][str(gws[q])+'_dmins'].iloc[0]).split())))
                except:
                    xmins.append(list(map(float, str(review_detailed[review_detailed['ID']==player_id][str(next_gw + review_horizon - 1)+'_dmins'].iloc[0]).split())))
            df = pd.DataFrame()

            understat_str = convert(str(id_dict_df.iloc[row]['Understat_Name'])) + '_' + str(id_dict_df.iloc[row]['Understat_ID']) + '.csv'
            #fpl_str_prev = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][ids[previous(season)]])
            try:
                fpl_str = convert(str(id_dict_df.iloc[row]['FPL_Name'])) + '_' + str(id_dict_df.iloc[row][ids[season]])
                main_df = pd.read_csv(PATH + season + '/players/' + fpl_str + '/gw.csv')
            except:
                fpl_str_df = pd.read_csv(fpl_str_df_path)
                fpl_str_df = fpl_str_df[fpl_str_df['22-23']==player_id]
                fpl_str = fpl_str_df['first_name'].iloc[0] + '_' + fpl_str_df['second_name'].iloc[0] + '_' + str(fpl_str_df['22-23'].iloc[0])
            understat_df = pd.read_csv(PATH + season + '/understat/' + understat_str)

            for gw in gws:
                opponent_team = []
                home = []
                kickoff_time = []
                fix_prob = []
                xp_gw = []
                xg_gw = []
                xa_gw = []
                xcs_gw = []
                xmd_gw = []
                xbp_gw = []
                xsave_points_gw = []
                xapp_gw = []
                xyc_gw = []
                xpm_gw = []
                bp90 = prev_rate(PATH, season, fpl_str, gw, gw_no_lim, 'bonus')
                sp90 = prev_rate(PATH, season, fpl_str, gw, gw_no_lim, 'saves')
                yc = prev_rate(PATH, season, fpl_str, gw, gw_no_lim, 'yc')
                teamid = team_id(player_id, season, players_raw)
                team_name = teams[season].iloc[teamid-1, 5]
                fix = fixture_info(player_id, season, gw, fixtures, teams, players_raw)
                for i in range(len(fix)):
                    cmp_df = pd.DataFrame()
                    opponent_team.append(fix[i][0])
                    home.append(fix[i][1])
                    kickoff_time.append(fix[i][2])   
                    fix_prob.append(fix[i][3])
                    pen_list = pens_per_game(fixtures, season, team_stats_dict, teams, teamid, gw_no_lim)[0]

                    pos = int(players_raw[season][players_raw[season]['id'] == int(id_dict_df.iloc[row][fpl_id])]['element_type'])
            
                    cmp_df.insert(0, 'opp_npxGAp90', [npxGAp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGp90(L4)', [last4npxGp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'xAp90(L4)', [last4xAp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGp90', [npxGp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'xAp90', [xAp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'position', [pos], True)
                    cmp_df.insert(0, 'opp_npxGp90l4', [opp_last4npxGp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'opp_npxGAp90l4', [last4npxGAp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'teamnpxGp90l4', [opp_last4npxGp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'opp_npxGp90', [opp_npxGp90(opponent_team[i], kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGAp90l4', [last4npxGAp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'npxGAp90', [npxGAp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'kpp90', [kpp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'shp90', [shp90(understat_df, int(season[:4]), kickoff_time[i], gw_no_lim)], True)
                    cmp_df.insert(0, 'teamnpxGp90', [opp_npxGp90(team_name, kickoff_time[i], season, team_stats_dict, gw_no_lim)], True)
                    cmp_df.insert(0, 'team_proj_goals', [proj_scores(team_name, opponent_team[i], int(season[:4]), home[i])[0]], True)
                    cmp_df.insert(0, 'opp_proj_goals', [proj_scores(team_name, opponent_team[i], int(season[:4]), home[i])[1]], True)
                    cmp_df.insert(0, 'bonusp90', [bp90], True) 
                    cmp_df.insert(0, 'savesp90', [sp90], True)
                    cmp_df.insert(0, 'pen_rate', [avg(pen_list)], True)
                    cmp_df.insert(0, 'was_home', [home[i]], True)
                    cmp_df.insert(0, 'xYC', [yc], True)
                    cmp_df.insert(0, 'npg_rate', [npg_rate_season(df, kickoff_time[i], int(season[:4]))], True)
                    cmp_df.insert(0, 'assist_rate', [assist_rate_season(df, kickoff_time[i], int(season[:4]))], True)
                    cmp_df.insert(0, 'npg_ratel100', [rates100(understat_df, kickoff_time[i], 'npg')], True)
                    cmp_df.insert(0, 'assist_ratel100', [rates100(understat_df, kickoff_time[i], 'assists')], True)
                    cmp_df.insert(0, 'npxGp90l100', [rates100(understat_df, kickoff_time[i], 'npxG')], True)
                    cmp_df.insert(0, 'xAp90l100', [rates100(understat_df, kickoff_time[i], 'xA')], True)
                    cmp_df.insert(0, 'sh_ratel100', [rates100(understat_df, kickoff_time[i], 'shots')], True)
                    cmp_df.insert(0, 'kp_ratel100', [rates100(understat_df, kickoff_time[i], 'key_passes')], True)
                    cmp_df.insert(0, 'team', [team_name], True)
                    cmp_df.insert(0, 'id', [player_id], True)
                    cmp_df.insert(0, 'minutes', [xmins[gw-gws[0]][i]], True)
                    cmp_df.insert(0, 'finishing_rate', [finishing_rate(understat_df)], True)
                    cmp_df.insert(0, 'penalty_finishing_rate', [penalty_finishing_rate(understat_df)], True)

                    points_df = xPoints(cmp_df, npgoals, assists, team_goals, bonus, saves, pens, 0)
                    xp_gw.append(fix_prob[i] * points_df['total'][0])
                    xg_gw.append(fix_prob[i] * points_df['goals'][0])
                    xa_gw.append(fix_prob[i] * points_df['assists'][0])
                    xbp_gw.append(fix_prob[i] * points_df['bonus'][0])
                    xapp_gw.append(fix_prob[i] * points_df['appearance'][0])
                    xyc_gw.append(fix_prob[i] * points_df['yellow_cards'][0])
                    xsave_points_gw.append(fix_prob[i] * points_df['saves'][0])
                    xcs_gw.append(fix_prob[i] * points_df['CS'][0])
                    xmd_gw.append(fix_prob[i] * points_df['md'][0])
                    xpm_gw.append(fix_prob[i] * points_df['pen_miss_points'][0])
                xp.append(xp_gw)
                xg.append(xg_gw)
                xa.append(xa_gw)
                cs.append(xcs_gw)
                md.append(xmd_gw)
                pm.append(xpm_gw)
                save_points.append(xsave_points_gw)
                bp.append(xbp_gw)
                ycc.append(xyc_gw)
                app.append(xapp_gw)
            
            tot = 0
            for q in range(horizon):
                xpoints['gw_'+str(next_gw+q)].append(round(sum(xp[q]),3))
                xgoals['gw_'+str(next_gw+q)].append(round(sum(xg[q]),3))
                xassists['gw_'+str(next_gw+q)].append(round(sum(xa[q]),3))
                xcs['gw_'+str(next_gw+q)].append(round(sum(cs[q]),3))
                xmd['gw_'+str(next_gw+q)].append(round(sum(md[q]),3))
                xpm['gw_'+str(next_gw+q)].append(round(sum(pm[q]),3))
                xapp['gw_'+str(next_gw+q)].append(round(sum(app[q]),3))
                xbp['gw_'+str(next_gw+q)].append(round(sum(bp[q]),3))
                xyc['gw_'+str(next_gw+q)].append(round(sum(ycc[q]),3))
                xsave_points['gw_'+str(next_gw+q)].append(round(sum(save_points[q]),3))
                tot += sum(xp[q])
            total.append(round(tot,3))
            
        except:
            for q in range(horizon):
                xpoints['gw_'+str(next_gw+q)].append(0)
                xgoals['gw_'+str(next_gw+q)].append(0)
                xassists['gw_'+str(next_gw+q)].append(0)
                xcs['gw_'+str(next_gw+q)].append(0)
                xmd['gw_'+str(next_gw+q)].append(0)
                xpm['gw_'+str(next_gw+q)].append(0)
                xapp['gw_'+str(next_gw+q)].append(0)
                xbp['gw_'+str(next_gw+q)].append(0)
                xyc['gw_'+str(next_gw+q)].append(0)
                xsave_points['gw_'+str(next_gw+q)].append(0)
                mins['gw_'+str(next_gw+q)].append(0)
            total.append(0)
            
    for q in range(horizon):
        try:
            review_df.insert(7+3*q, str(next_gw+q)+'_xP', xpoints['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xG', xgoals['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xA', xassists['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xCS', xcs['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xmd', xmd['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xpm', xpm['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xapp', xapp['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xbonus', xbp['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xyc', xyc['gw_'+str(next_gw+q)], True)
            review_df.insert(7+3*q, str(next_gw+q)+'_xsaves', xsave_points['gw_'+str(next_gw+q)], True)
        except:
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xMins', xmins[q], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xP', xpoints['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xG', xgoals['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xA', xassists['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xCS', xcs['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xmd', xmd['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xpm', xpm['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xapp', xapp['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xbonus', xbp['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xyc', xyc['gw_'+str(next_gw+q)], True)
            review_df.insert(len(review_df.keys()), str(next_gw+q)+'_xsaves', xsave_points['gw_'+str(next_gw+q)], True)
    review_df.insert(len(review_df.keys()), 'total', total, True)
    
    for q in range(horizon):
        try:
            review_df.drop([str(next_gw+q)+'_Pts'], axis=1, inplace=True)
            review_df.rename(columns={str(next_gw+q)+'_xP': str(next_gw+q)+'_Pts'}, inplace=True)
        except:
            review_df.rename(columns={str(next_gw+q)+'_xP': str(next_gw+q)+'_Pts'}, inplace=True)
    return review_df


def filter_df(an_ev_df, next_gw, horizon, el, sort_str, num):
    cols = ['Pos', 'ID', 'Name', 'BV', 'SV', 'Team', 'total']
    for q in range(horizon):
        cols += [str(next_gw+q)+'_xMins', str(next_gw+q)+el]
    df = an_ev_df.drop(an_ev_df.columns.difference(cols), 1)
    df = df.loc[:, cols]
    df.insert(len(df.keys()), 'sum', [sum([df[str(next_gw+q)+el].iloc[x] for q in range(horizon)]) for x in range(df.shape[0])])
    return df.sort_values(by=sort_str,ascending=False)[:num]