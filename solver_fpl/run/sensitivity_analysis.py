import pandas as pd
import os
import glob
import shutil

def sensitivity_analysis(directory, next_gw, no_runs):
    
    # Delete results directory and create it again
    shutil.rmtree(directory) 
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i in range(no_runs):
        print('Run no: ' + str(i))
        os.system('python solve_regular.py')
    
    no_plans = len(os.listdir(directory))
    goalkeepers = []
    defenders = []
    midfielders = []
    forwards = []
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            plan = pd.read_csv(f)
            goalkeepers += plan[(plan['week']==next_gw) & (plan['squad']==1) & (plan['pos']=='GKP')]['name'].to_list()
            defenders += plan[(plan['week']==next_gw) & (plan['squad']==1) & (plan['pos']=='DEF')]['name'].to_list()
            midfielders += plan[(plan['week']==next_gw) & (plan['squad']==1) & (plan['pos']=='MID')]['name'].to_list()
            forwards += plan[(plan['week']==next_gw) & (plan['squad']==1) & (plan['pos']=='FWD')]['name'].to_list()

    keepers = pd.DataFrame(goalkeepers, columns=['player']).value_counts().reset_index(name='PSB')
    defs = pd.DataFrame(defenders, columns=['player']).value_counts().reset_index(name='PSB')
    mids = pd.DataFrame(midfielders, columns=['player']).value_counts().reset_index(name='PSB')
    fwds = pd.DataFrame(forwards, columns=['player']).value_counts().reset_index(name='PSB')

    keepers['PSB'] = ["{:.0%}".format(keepers['PSB'][x]/no_plans) for x in range(keepers.shape[0])]
    defs['PSB'] = ["{:.0%}".format(defs['PSB'][x]/no_plans) for x in range(defs.shape[0])]
    mids['PSB'] = ["{:.0%}".format(mids['PSB'][x]/no_plans) for x in range(mids.shape[0])]
    fwds['PSB'] = ["{:.0%}".format(fwds['PSB'][x]/no_plans) for x in range(fwds.shape[0])]

    print('Goalkeepers:')
    print('\n'.join(keepers.to_string(index = False).split('\n')[1:]))
    print()
    print('Defenders:')
    print('\n'.join(defs.to_string(index = False).split('\n')[1:]))
    print()
    print('Midfielders:')
    print('\n'.join(mids.to_string(index = False).split('\n')[1:]))
    print()
    print('Forwards:')
    print('\n'.join(fwds.to_string(index = False).split('\n')[1:]))


next_gw = 8
no_runs = 50
directory = '../data/results/'

sensitivity_analysis(directory, next_gw, no_runs)