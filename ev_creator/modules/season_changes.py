import pandas as pd
import requests
import numpy as np
from modules.useful_functions import team_id, fixture_info2, avg
import pickle

def add_extra_players(master):
    n = 22
    master_extra = pd.DataFrame({'code': [222683, 118342, 168090, 578614, 189776, 183751, 250735, 435973, 482609, 517052, 213198, 424876, 432422, 201440, 233821, 487053, 184254, 244954, 202641, 243557, 487702, 223434], 
                                'first_name': ['Justin', 'Mark', 'Mahmoud', 'Enock', 'Samuel', 'Manuel Benson', 'Darko', 'Lyle', 'Malo', 'Nicolas', 'Christopher', 'Dominik', 'Sandro', 'Hwang', 'Anel', 'Destiny', 'Guglielmo', 'Pau', 'André', 'Moussa', 'Luca', 'Igor Julio'], 
                                'second_name': ['Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Hedilazio', 'Churlinov', 'Foster', 'Gusto', 'Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Torres', 'Onana', 'Diaby', 'Koleosho', 'dos Santos de Paulo'], 
                                'web_name': ['Kluivert', 'Flekken', 'Dahoud', 'Agyei', 'Bastien', 'Benson', 'Churlinov', 'Foster', 'Gusto', 'N.Jackson', 'Nkunku', 'Szoboszlai', 'Tonali', 'Ui-jo', 'Ahmedhodžić', 'Udogie', 'Vicario', 'Pau', 'Onana', 'Diaby', 'Koleosho', 'Igor'], 
                                '16-17': [np.NaN]*n, '17-18': [np.NaN]*n, '18-19': [np.NaN]*n, '19-20': [np.NaN]*n, '20-21': [np.NaN]*n, '21-22': [np.NaN]*n, '22-23': [np.NaN]*n,
                                'fbref': [np.NaN]*n,
                                'understat': [6963.0, 7047.0, 205.0, 5563.0, 1343.0, 7383.0, 7790.0, 7498.0, 9017.0, 10048.0, 3300.0, 9788.0, 7958.0, 7746.0, 10386.0, 8831.0, 8858.0, 6221.0, 10913.0, 6556.0, 10620.0, 7943.0],
                                'transfermarkt': [np.NaN]*n,
                                '23-24': [72.0, 101.0, 128.0, 156.0, 158.0, 159.0, 162.0, 168.0, 203.0, 211.0, 212.0, 309.0, 429.0, 466.0, 471.0, 519.0, 520.0, 584.0, 597.0, 599.0, 605.0, 606.0]})
    master = master.append(master_extra, ignore_index=True)
    return master


def exp_mins(main_df):
    mins = main_df['minutes'].to_list()
    mins = [i for i in mins if i != 0 ]
    if len(mins) > 0 and sum(mins) > 1350:
        return round(sum(mins)/len(mins), 2)
    else:
        return 15.0

def convert(lst):     
    return ' '.join(str(item) for item in lst)

home = {
    True: '(H): ',
    False: '(A): '
}

def produce_player_dfs(season, master_path, players_raw, teams, fixtures, horizon, next_gw):
    df = players_raw[season]
    teams2023 = teams[season]
    master = pd.read_csv(master_path)
    gws = list(range(next_gw, next_gw + horizon))
    ids2023 = []
    short_teams = []
    positions = []
    prices = []
    fix = [[], [], [], [], [], []]
    xmins = [[], [], [], [], [], []]
    dmins = [[], [], [], [], [], []]
    likelihood = [[], [], [], [], [], []]

    for row in range(master.shape[0]):
        try:
            df_aux = df[df['code']==master['code'].iloc[row]]
            id = df_aux['id'].iloc[0]
            ids2023.append(id)
        except:
            ids2023.append(np.NaN)
    master['23-24'] = ids2023

    master = master[~master['23-24'].isna()]
    master = add_extra_players(master)
    master.to_csv('master.csv')

    for row in range(master.shape[0]):
        df_aux = df[df['code']==master['code'].iloc[row]]
        id = df_aux['id'].iloc[0]
        '''
        url = 'https://fantasy.premierleague.com/api/element-summary/' + str(int(id)) + '/'
        main_df = pd.DataFrame(requests.get(url).json()['history'])
        '''
        try:
            main_df = pd.read_csv('../data/Fantasy-Premier-League/data/2022-23/players/' + master['first_name'].iloc[row] + '_' + master['second_name'].iloc[row] + '_' + str(int(master['22-23'].iloc[row])) + '/gw.csv')
            expected_mins = exp_mins(main_df)
        except:
            expected_mins = 15.0
        tid = team_id(id, season, players_raw)
        short_teams.append(teams2023[teams2023['id']==tid]['short_name'].iloc[0])
        positions.append(df_aux['element_type'].iloc[0])
        prices.append(df_aux['now_cost'].iloc[0])
        for gw in gws:
            afix = []
            admins = []
            alikelihood = []
            fix_list = fixture_info2(tid, season, gw, fixtures, teams)
            for i in range(len(fix_list)):
                opp_team, was_home, kickoff_time, score1, score2 = fixture_info2(tid, season, gw, fixtures, teams)[i]
                afix.append(home[was_home] + teams2023[teams2023['name']==opp_team]['short_name'].iloc[0])
                admins.append(expected_mins)
                alikelihood.append(1)
            fix[gw-next_gw].append(convert(afix))
            dmins[gw-next_gw].append(convert(admins))
            likelihood[gw-next_gw].append(convert(alikelihood))
            xmins[gw-next_gw].append(avg(admins))

    master['Team'] = short_teams
    master['Pos'] = positions
    master['Price'] = prices

    for gw in gws:
        master[str(gw)+ '_fix'] = fix[gw-next_gw]
        master[str(gw)+ '_xmins'] = xmins[gw-next_gw]
        master[str(gw)+ '_dmins'] = dmins[gw-next_gw]
        master[str(gw)+ '_likelihood'] = likelihood[gw-next_gw]

    review_detailed = master.drop(['code', 'first_name', 'second_name', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', 'fbref', 'understat', 'transfermarkt'], axis=1)
    review_detailed = review_detailed.rename(columns={'web_name': 'Name', '23-24': 'ID'})


    fpl_review = pd.DataFrame()
    pos = {
        1: 'G',
        2: 'D',
        3: 'M',
        4: 'F'
    }
    fpl_review['Pos'] = [pos[review_detailed['Pos'].iloc[x]] for x in range(review_detailed.shape[0])] 
    fpl_review['ID'] = [review_detailed['ID'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['Name'] = [review_detailed['Name'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['BV'] = [review_detailed['Price'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['SV'] = [review_detailed['Price'].iloc[x] for x in range(review_detailed.shape[0])] 
    fpl_review['Team'] = [teams2023[teams2023['short_name']==review_detailed['Team'].iloc[x]]['name'].iloc[0] for x in range(review_detailed.shape[0])]
    for gw in gws:
        fpl_review[str(gw)+ '_xMins'] = [review_detailed[str(gw)+ '_xmins'].iloc[x] for x in range(review_detailed.shape[0])] 
        fpl_review[str(gw)+ '_Pts'] = [0] * review_detailed.shape[0]

    review_df = fpl_review

    return review_detailed, review_df


gws_left = 38
initial_spis2023 = {
        'Arsenal': [83.9]*gws_left,
        'Aston Villa': [79.3]*gws_left,
        'Brentford': [77.1]*gws_left,
        'Brighton': [80.9]*gws_left,
        'Bournemouth': [59.6]*gws_left,
        'Chelsea': [75.8]*gws_left,
        'Crystal Palace': [73.5]*gws_left,
        'Everton': [63.6]*gws_left,
        'Sheffield Utd': [52.4]*gws_left,
        'Luton': [49.5]*gws_left,
        'Liverpool': [83.9]*gws_left,
        'Man City': [92.0]*gws_left,
        'Man Utd': [79.1]*gws_left,
        'Newcastle': [83.7]*gws_left,
        'Fulham': [68.2]*gws_left,
        'Burnley': [56.1]*gws_left,
        'Spurs': [72.1]*gws_left,
        'Nott\'m Forest': [56.1]*gws_left,
        'West Ham': [71.1]*gws_left,
        'Wolves': [59.1]*gws_left
    }


def compute_new_spis(spi_model, teams, team_stats_dict, season, next_gw):
    if next_gw == 1:
        return initial_spis2023
    with open('old_spis.pkl', 'rb') as f:
        old_spis = pickle.load(f)
    t = teams[season]
    new_spis = {}
    gws_left = 38 - next_gw + 1

    for team in t:
        tid = t[t['name']==team]['id'].iloc[0]
        opp_team, home, kickoff_time, score1, score2 = fixture_info2(tid, season, next_gw-1, fixtures, teams)
        old_spi_team = old_spis[team][0]
        old_spi_opp_team = old_spis[opp_team][0]
        df = team_stats_dict[season][team].loc[0]
        xg1 = df['xG']
        xg2 = df['xGA']
        new_spi = spi_model.predict([[old_spi_team, old_spi_opp_team, score1, score2, xg1, xg2, home]])[0]
        new_spis[team] = [new_spi]*gws_left
    with open('new_spis.pkl', 'wb') as f:
        pickle.dump(new_spis, f)
    return new_spis



expected_minutes = {
# Arsenal
    1: [0.0],  # Balogun
    2: [0.0],  # Cedric
    3: [3.0],  # Elneny
    4: [15.0],  # Vieira
    5: [85.0],  # Gabriel
    6: [55.0],  # Havertz
    7: [4.0],  # Holding
    8: [77.0],  # Jesus
    9: [10.0],  # Jorginho
    10: [6.0], # Kiwior
    11: [0.0], # Marquinhos
    12: [73.0], # Martinelli
    13: [13.0], # Nketiah
    14: [82.0], # Odegaard
    15: [78.0], # Partey
    16: [3.0], # Pepe
    17: [89.0], # Ramsdale
    18: [0.0], # Runaarsson
    19: [84.0], # Saka
    20: [85.0], # Saliba
    21: [5.0], # Sambi
    22: [13.0], # Smith Rowe
    23: [2.0], # Tavares
    24: [8.0], # Tierney
    25: [12.0], # Tomiyasu
    26: [55.0], # Trossard
    27: [0.0],  # Trusty
    28: [1.0], # Turner
    29: [75.0], # White
    30: [79.0], # Xhaka
    31: [77.0], # Zinchenko
# Aston Villa
    32: [76.0], # Alex Moreno
    33: [3.0], # Archer
    34: [65.0], # Bailey
    35: [75.0], # Buendia
    36: [77.0], # Cash
    37: [8.0], # Chambers
    38: [7.0], # Coutinho
    39: [0.0], # Davis
    40: [13.0], # Dendoncker
    41: [77.0], # Diego Carlos
    42: [14.0], # Digne 
    43: [69.0], # Douglas Luiz
    44: [13.0], # Duran
    45: [8.0], # Hause 
    46: [3.0], # Iroegbunam
    47: [3.0], # Kamara
    48: [75.0], # Konsa
    49: [89.0], # Martinez
    50: [77.0], # McGinn
    51: [24.0], # Mings
    52: [8.0], # Nakamba
    53: [1.0], # Olsen
    54: [0.0], # Philogene-Bidace
    55: [75.0], # Ramsey
    56: [8.0], # Sanson
    57: [0.0], # Sinisalo
    58: [76.0], # Tielemans
    59: [15.0], # Traore
    60: [86.0], # Watkins
    61: [1.0], # Wesley
# Bournemouth
    62: [3.0], # Anthony
    63: [65.0], # Billing
    64: [45.0], # Brooks
    65: [22.0], # Christie
    66: [77.0], # Cook
    67: [12.0], # Dembele
    68: [4.0], # Fredericks
    69: [0.0], # Hill
    70: [0.0], # Kelly
    71: [0.0], # Kilkenny
    72: [8.0], # Kluivert
    73: [0.0], # Lowe
    74: [0.0], # Marcondes
    75: [3.0], # Mepham
    76: [24.0], # Moore
    77: [89.0], # Neto
    78: [65.0], # Ouattara
    79: [15.0], # Pearson
    80: [0.0], # Randolph
    81: [10.0], # Rothwell
    82: [12.0], # Semenyo
    83: [12.0], # Senesi
    84: [65.0], # Smith
    85: [85.0], # Solanke
    86: [78.0], # Tavernier
    87: [32.0], # H.Traore
    88: [1.0], # Travers
    89: [0.0], # Zabarnyi
# Brentford
    90: [43.0], # Ajer
    91: [0.0], # Balcombe
    92: [11.0], # Baptiste
    93: [0.0], # Bech
    94: [0.0], # Bidstrup
    95: [55.0], # Canos
    96: [43.0], # Collins
    97: [0.0], # Cox
    98: [67.0], # Damsgaard
    99: [23.0], # Dasilva
    100: [5.0],  # Dervisoglu
    101: [89.0],    # Flekken
    102: [0.0],    # Goode
    103: [78.0],    # Henry
    104: [11.0],    # Hickey
    105: [14.0],    # Janelt
    106: [77.0],    # Jensen
    107: [0.0],    # Lewis-Potter
    108: [83.0],    # Mbeumo
    109: [85.0],    # Mee
    110: [77.0],    # Norgaard
    111: [12.0],    # Onyeka
    112: [85.0],    # Pinnock
    113: [1.0],    # Raya
    114: [0.0],    # Roerslev
    115: [0.0],    # Schade
    116: [0.0],    # Strakosha
    117: [0.0],    # Toney
    118: [0.0],    # Trevitt
    119: [75.0],    # Wissa
    120: [0.0],    # Yarmolyuk
    121: [3.0],    #Zanka
    122: [0.0],    # Adingra
# Brighton
    123: [8.0],    # Alzate
    124: [8.0],    # Ayari
    125: [22.0],    # Buonanotte
    126: [78.0],    # Caicedo
    127: [3.0],    # Connolly
    128: [3.0],    # Dahoud
    129: [85.0],    # Dunk
    130: [62.0],    # Enciso
    131: [77.0],    # Estupinan
    132: [62.0],    # Ferguson
    133: [22.0],    # Gilmour
    134: [85.0],    # Gross
    135: [62.0],    # Joao Pedro
    136: [0.0],    # Karbownik
    137: [0.0],    # Kozlowski
    138: [12.0],    # Lallana
    139: [15.0],    # Lamptey
    140: [77.0],    # March
    141: [0.0],    # McGill
    142: [15.0],    # Milner
    143: [82.0],    # Mitoma
    144: [14.0],    # Moder
    145: [1.0],    # Sanchez
    146: [12.0],    # Sarmiento
    147: [0.0],    # Scherpen
    148: [89.0],    # Steele
    149: [22.0],    # Undav
    150: [14.0],    # Van Hecke
    151: [75.0],    # Veltman
    152: [0.0],    # Verbruggen
    153: [82.0],    # Webster
    154: [45.0],    # Wellbeck
    155: [0.0],    # Zeqiri
# Burnley
    156: [0.0],    # Agyei
    157: [0.0],    # Al-Dakhil
    158: [0.0],    # Bastien
    159: [0.0],    # Benson
    160: [75.0],    # Beyer
    161: [78.0],    # Brownhill
    162: [0.0],    # Churlinov
    163: [75.0],    # Cork
    164: [0.0],    # Costelloe
    165: [87.0],    # Cullen
    166: [0.0],    # Egan-Riley    
    167: [0.0],    # Ekdal
    168: [0.0],    # Foster
    169: [0.0],    # Franchi    
    170: [55.0],    # Gudmundsson
    171: [0.0],    # McNally
    172: [89.0],    # Muric
    173: [20.0],    # O'Shea
    174: [11.0],    # Obafemi
    175: [1.0],    # Peacock-Farrell
    176: [75.0],    # Roberts
    177: [74.0],    # Rodriguez
    178: [75.0],    # Taylor
    179: [0.0],    # Thomas
    180: [0.0],    # Twine
    181: [0.0],    # Vigouroux
    182: [72.0],    # Vitinho
    183: [55.0],    # Weghorst
    184: [0.0],    # Zaroury
    185: [76.0],    # Ampadu
    186: [0.0],    # Andrey Santos
# Chelsea
    187: [],    # Arrizabalaga
    188: [],    # Aubameyang
    189: [],    # Azpilicueta
    190: [],    # Baba Rahman
    191: [],    # Badiashile
    192: [],    # Bettinelli
    193: [],    # Broja
    194: [],    # Chalobah
    195: [],    # Chilwell
    196: [],    # Chukwuemeka
    197: [],    # Colwill
    198: [],    # Cucurella
    199: [],    # Enzo
    200: [],    # D.D.Fofana
    201: [],    # W.Fofana
    202: [],    # Gallagher
    203: [],    # Gusto
    204: [],    # Hall
    205: [],    # Hudson-Odoi
    206: [],    # James
    207: [],    # Lukaku
    208: [],    # Madueke
    209: [],    # Mount
    210: [],    # Mudryk
    211: [],    # N.Jackson
    212: [],    # Nkunku
    213: [],    # Pulisic
    214: [],    # Sarr
    215: [],    # Slonina
    216: [],    # Sterling
    217: [],    # Thiago Silva
    218: [],    # Ziyech
# Crystal Palace
    219: [],    # Ahamada
    220: [],    # Andersen
    221: [],    # J.Ayew
    222: [],    # Clyne
    223: [],    # C.Doucoure
    224: [],    # Ebiowei
    225: [],    # Edouard
    226: [],    # Eze
    227: [],    # Guaita
    228: [],    # Guehi
    229: [],    # Hughes
    230: [],    # Johnstone
    231: [],    # Lerma
    232: [],    # Mateta
    233: [],    # Matthews
    234: [],    # Mitchell
    235: [],    # O'Brien
    236: [],    # Olise
    237: [],    # Plange
    238: [],    # Richards
    239: [],    # Riedewald
    240: [],    # Schlupp
    241: [],    # Tomkins
    242: [],    # Ward
    243: [],    # Whitworth
# Everton
    244: [],    # Andre Gomes
    245: [],    # Branthwaite
    246: [],    # Calvert-Lewin
    247: [],    # Coleman
    248: [],    # Dele
    249: [],    # A.Doucoure
    250: [],    # Garner
    251: [],    # Gbamin
    252: [],    # Godfrey
    253: [],    # Gray
    254: [],    # Gueye
    255: [],    # Holgate
    256: [],    # Iwobi
    257: [],    # Keane
    258: [],    # Maupay
    259: [],    # McNeil
    260: [],    # Mykolenko
    261: [],    # Onana
    262: [],    # Patterson
    263: [],    # Pickford
    264: [],    # Simms
    265: [],    # Trakowski
    266: [],    # Virginia
# Fulham
    267: [],    # Andreas
    268: [],    # Cairney
    269: [],    # Cavaleiro
    270: [],    # De Cordova-Reid
    271: [],    # Diop
    272: [],    # Francois
    273: [],    # Knockaert
    274: [],    # Kongolo
    275: [],    # Leno
    276: [],    # Lukic
    277: [],    # Mbabu
    278: [],    # Mitrovic
    279: [],    # Muniz
    280: [],    # Palinha
    281: [],    # Ream
    282: [],    # Reed
    283: [],    # Robinson
    284: [],    # Rodak
    285: [],    # Tete
    286: [],    # Tosin
    287: [],    # Vinicius
    288: [],    # Wilson
# Liverpool
    289: [],    # Adrian
    290: [],    # Alexander-Arnold
    291: [],    # Alisson
    292: [],    # Bajcetic
    293: [],    # Darwin
    294: [],    # Diogo Jota
    295: [],    # Eliott
    296: [],    # Fabinho
    297: [],    # Gakpo
    298: [],    # Gomez
    299: [],    # Henderson
    300: [],    # Jones
    301: [],    # Kelleher
    302: [],    # Konate
    303: [],    # Luis Diaz
    304: [],    # Mac Allister
    305: [],    # Matip
    306: [],    # Phillips
    307: [],    # Robertson
    308: [],    # Salah
    309: [],    # Szoboszlai  
    310: [],    # Thiago
    311: [],    # Tsimikas
    312: [],    # Van den Berg
    313: [],    # Van Dijk
# Luton
    314: [],    # Adebayo
    315: [],    # Andersen
    316: [],    # Bell
    317: [],    # Burry
    318: [],    # Burke
    319: [],    # Campbell
    320: [],    # Clark
    321: [],    # Doughty
    322: [],    # Freeman
    323: [],    # Macey
    324: [],    # McAtee
    325: [],    # Mendes
    326: [],    # Morris
    327: [],    # Muskwe
    328: [],    # Ogbene
    329: [],    # Onyedinma
    330: [],    # Osho
    331: [],    # Pepple
    332: [],    # Pereira
    333: [],    # Potts
    334: [],    # Rea
    335: [],    # Shes
    336: [],    # Taylor
    337: [],    # Thorpe
    338: [],    # Walton
    339: [],    # Watson
    340: [],    # Woodrow
# Man City
    341: [],    # Akanji
    342: [],    # Ake
    343: [],    # Alvarez
    344: [],    # Bernardo
    345: [],    # Bobb
    346: [],    # Cancelo
    347: [],    # Carson
    348: [],    # Charles
    349: [],    # De Bruyne
    350: [],    # Dias
    351: [],    # Doyle
    352: [],    # Ederson
    353: [],    # Foden
    354: [],    # Grealish
    355: [],    # Haaland
    356: [],    # Kovacic
    357: [],    # Laporte
    358: [],    # Lewis
    359: [],    # Mahrez
    360: [],    # McAtee
    361: [],    # Ortega
    362: [],    # Palmer
    363: [],    # Perrone
    364: [],    # Phillips
    365: [],    # Rodri
    366: [],    # Sergio Gomez
    367: [],    # Steffen
    368: [],    # Stones
    369: [],    # Walker
# Man United
    370: [],    # Telles
    371: [],    # Amad
    372: [],    # Antony
    373: [],    # Fernandes
    374: [],    # B.Williams
    375: [],    # Bailly
    376: [],    # Casemiro
    377: [],    # Dalot
    378: [],    # Elanga
    379: [],    # Eriksen
    380: [],    # Alvaro Fernandez
    381: [],    # Fred
    382: [],    # Garnacho
    383: [],    # Mejbri
    384: [],    # Heaton
    385: [],    # Hendersonn
    386: [],    # Lindelof
    387: [],    # Mguire
    388: [],    # Mainoo
    389: [],    # Malacia
    390: [],    # Martial
    391: [],    # Martinez
    392: [],    # McTominay
    393: [],    # Mengi
    394: [],    # Pellistri
    395: [],    # Varane
    396: [],    # Rahford
    397: [],    # Sancho
    398: [],    # Shaw
    399: [],    # Shoretire
    400: [],    # Van de Beek
    401: [],    # Wan-Bissaka
# Newcastle
    402: [],    # Almiron
    403: [],    # Anderson
    404: [],    # Ashby
    405: [],    # Botman
    406: [],    # Bruno Guimaraes
    407: [],    # Burn
    408: [],    # Darlow
    409: [],    # Dubravka
    410: [],    # Fraser
    411: [],    # Gillespie
    412: [],    # Gordon
    413: [],    # Hayden
    414: [],    # Hendrick
    415: [],    # Isak
    416: [],    # Joelinton
    417: [],    # Krafth
    418: [],    # Kuol
    419: [],    # Lascelles
    420: [],    # Lewis
    421: [],    # S.Longstaff
    422: [],    # Manquillo
    423: [],    # Murphy
    424: [],    # Pope
    425: [],    # Ritchie
    426: [],    # Saint-Maximin
    427: [],    # Schar
    428: [],    # Targett
    429: [],    # Tonali
    430: [],    # Trippier
    431: [],    # Watts
    432: [],    # Willock    
    433: [],    # Wilson
# Nottingham Forest
    434: [],    # B.Aguilera
    435: [],    # Arter
    436: [],    # Aurier
    437: [],    # Awoniyi
    438: [],    # Biancone
    439: [],    # Boly
    440: [],    # Bowler
    441: [],    # Cook
    442: [],    # Danilo
    443: [],    # Dennis
    444: [],    # Drager
    445: [],    # Felipe
    446: [],    # Freuler
    447: [],    # Gibbs-White
    448: [],    # Hennessey
    449: [],    # Horvath
    450: [],    # Johnson
    451: [],    # Kouyate
    452: [],    # Laryea
    453: [],    # Mangala
    454: [],    # Mbe Soh
    455: [],    # McKenna
    456: [],    # Mighten
    457: [],    # Niakhate
    458: [],    # O'Brien
    459: [],    # Ojeda
    460: [],    # Panzo
    461: [],    # Richards
    462: [],    # Scarpa
    463: [],    # Shelvey
    464: [],    # Surridge
    465: [],    # Toffolo
    466: [],    # Ui-Jo
    467: [],    # N.Williams
    468: [],    # Wood
    469: [],    # Worrall
    470: [],    # Yates
# Sheffield United 
    471: [],    # Ahmedhodzic
    472: [],    # Amissah
    473: [],    # Baldock
    474: [],    # Basham
    475: [],    # Berge
    476: [],    # Bogle
    477: [],    # Brewster
    478: [],    # Coulibaly
    479: [],    # Davies
    480: [],    # Egan
    481: [],    # Fleck
    482: [],    # Foderingham
    483: [],    # Jebbison
    484: [],    # Lowe
    485: [],    # McBurnie
    486: [],    # Ndiaye
    487: [],    # Norrington-Davies
    488: [],    # Norwood
    489: [],    # Osborn
    490: [],    # Osula
    491: [],    # Austin
# Spurs
    492: [],    # Bentancur
    493: [],    # Bissouma
    494: [],    # Bryan
    495: [],    # Davies
    496: [],    # Dier
    497: [],    # Emerson Royal
    498: [],    # Forster
    499: [],    # Hojberg
    500: [],    # Kane
    501: [],    # Kulusevski
    502: [],    # LLoris
    503: [],    # Lo Celso
    504: [],    # Maddison
    505: [],    # Ndombele
    506: [],    # Pedro Porro
    507: [],    # Perisic
    508: [],    # Reguillon  
    509: [],    # Richarlison
    510: [],    # Rodon
    511: [],    # Romero
    512: [],    # Sanchez
    513: [],    # Sarr
    514: [],    # R.Sessegnon
    515: [],    # Skipp
    516: [],    # Son
    517: [],    # Spence
    518: [],    # Tanganga
    519: [],    # Udogie
    520: [],    # Vicario
    521: [],    # Whiteman
# West Ham
    522: [],    # Aguerd
    523: [],    # Antonio
    524: [],    # Areola
    525: [],    # Benrahma
    526: [],    # Bowen
    527: [],    # Cornet
    528: [],    # Coufal
    529: [],    # Coventry
    530: [],    # Cresswell
    531: [],    # Downes
    532: [],    # Emerson
    533: [],    # Fabianski
    534: [],    # Fornals
    535: [],    # Ings
    536: [],    # Johnson
    537: [],    # Kehrer
    538: [],    # Mubama
    539: [],    # Paqueta
    540: [],    # Rice
    541: [],    # Scamacca
    542: [],    # Soucek
    543: [],    # Vlasic
    544: [],    # Zouma
# Wolves
    545: [],    # Ait-Nouri
    546: [],    # Bentley
    547: [],    # Bolla
    548: [],    # Bueno
    549: [],    # Chiquinho
    550: [],    # Cundle
    551: [],    # Dawson
    552: [],    # Fabio silva
    553: [],    # Giles
    554: [],    # Guedes
    555: [],    # Hodge
    556: [],    # Hoever
    557: [],    # Hwang
    558: [],    # Jimenez
    559: [],    # Joao Gomes
    560: [],    # Jonny
    561: [],    #  Jordao
    562: [],    # Kalajdzic
    563: [],    # Kilman
    564: [],    # King
    565: [],    # Lemina
    566: [],    # Matheus Nunes
    567: [],    # Neto
    568: [],    # Podence
    569: [],    # Sa
    570: [],    # Sarabia
    571: [],    # Sarkic
    572: [],    # Semedo
    573: [],    # Toti
    574: [],    # B.Traore
# extra
    575: [],    # Lockyer
    576: [],    # Jack Robinson   
    577: [],    # Ogbonna
    578: [],    # Nelson
    579: [],    # Lonergan
    580: [],    # Karius
    581: [],    # Dummet
    582: [],    # Mpanzu
    583: [],    # Solomon
    584: [],    # Pau Torres
    585: [],    # J.Timber
    586: [],    # Chong
    587: [],    # Slimane
    588: [],    # Young
    589: [],    # Angelo
    590: [],    # Cunha
    591: [],    # Willian
    592: [],    # Larouci
    593: [],    # T.Benie
    594: [],    # Amdouni
    595: [],    # Kerkez
    596: [],    # Trafford
    597: [],    # Onana
    598: [],    # Doherty
    599: [],    # Diaby
    600: [],    # Redmond
    601: [],    # Danjuma
    602: [],    # Kabore
    603: [],    # Barness
    604: [],    # Aina
    605: [],    # Koleosho
    606: []    # Igor
 }