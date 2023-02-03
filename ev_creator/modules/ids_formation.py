import pandas as pd


def isNaN(num):
    return num != num

def ids_formation(PATH, PATH2):
    id_dict_df = pd.read_csv(PATH + '2021-22/id_dict.csv')
    ids2019 = pd.read_csv(PATH + '2019-20/player_idlist.csv')
    ids2020 = pd.read_csv(PATH + '2020-21/player_idlist.csv')
    id_dict_2022 = pd.read_csv(PATH + '2022-23/id_dict.csv')

    id_dict_df = id_dict_df.rename(columns = {' FPL_ID': 'FPL_ID_2021'})

    ids2019['first_name'] = [ids2019['first_name'][x] + ' ' + ids2019['second_name'][x] for x in range(ids2019.shape[0])]
    ids2019 = ids2019.drop(['second_name'], axis=1)
    ids2019 = ids2019.rename(columns = {'id': 'FPL_ID_2019'})

    ids2020['first_name'] = [ids2020['first_name'][x] + ' ' + ids2020['second_name'][x] for x in range(ids2020.shape[0])]
    ids2020 = ids2020.drop(['second_name'], axis=1)
    ids2020 = ids2020.rename(columns = {'id': 'FPL_ID_2020'})

    id_dict_df = id_dict_df.merge(ids2020, left_on=' FPL_Name', right_on='first_name', how='left').merge(ids2019, left_on=' FPL_Name', right_on='first_name', how='left')
    id_dict_df = id_dict_df.drop(['first_name_x', 'first_name_y'], axis=1)
    id_dict_df[['FPL_ID_2020', 'FPL_ID_2019']] = id_dict_df[['FPL_ID_2020', 'FPL_ID_2019']].fillna(0.0).astype(int)

    id_dict_df = id_dict_df.merge(id_dict_2022, left_on=' Understat_Name', right_on='Understat_Name', how='outer')
    id_dict_df['Understat_ID_x'] = [id_dict_df['Understat_ID_x'][x] if not isNaN(id_dict_df['Understat_ID_x'][x]) else id_dict_df['Understat_ID_y'][x] for x in range(id_dict_df.shape[0])]
    id_dict_df['Understat_Name'] = [id_dict_df['Understat_Name'][x] if not isNaN(id_dict_df['Understat_Name'][x]) else id_dict_df[' Understat_Name'][x] for x in range(id_dict_df.shape[0])]
    id_dict_df['FPL_Name'] = [id_dict_df['FPL_Name'][x] if not isNaN(id_dict_df['FPL_Name'][x]) else id_dict_df[' FPL_Name'][x] for x in range(id_dict_df.shape[0])]
    id_dict_df = id_dict_df.rename(columns = {'FPL_ID': 'FPL_ID_2022', 'Understat_ID_x': 'Understat_ID'})
    id_dict_df = id_dict_df.drop([' Understat_Name', ' FPL_Name', 'Understat_ID_y'], axis=1)
    id_dict_df[['FPL_ID_2019','FPL_ID_2020','FPL_ID_2021','FPL_ID_2022','Understat_ID']] = id_dict_df[['FPL_ID_2019','FPL_ID_2020','FPL_ID_2021','FPL_ID_2022','Understat_ID']].fillna(0.0).astype(int)

    chris_map = pd.read_csv(PATH2)
    id_dict_df = pd.merge(chris_map, id_dict_df, left_on='understat', right_on='Understat_ID', how='right')
    id_dict_df.drop(id_dict_df.columns.difference(['Understat_ID', 'fbref', 'FPL_ID_2022', 'FPL_ID_2021', 'FPL_ID_2020', 'FPL_ID_2019', 'Understat_Name', 'FPL_Name']), 1, inplace=True)
    
    return id_dict_df