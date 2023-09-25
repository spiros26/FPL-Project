import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def best_options(ev_df, next_gw, horizon, num):
    plt.style.use('fivethirtyeight') 
    plt.figure(figsize=(6, 4), dpi=100)
    horizon_pts = [sum([ev_df[str(next_gw+q)+'_Pts'].iloc[x] for q in range(horizon)]) for x in range(ev_df.shape[0])]
    ev_df.insert(3, 'horizon_pts', horizon_pts)
    ev_df.insert(3, 'horizon_value', [round(ev_df['horizon_pts'].iloc[x]/ev_df['BV'].iloc[x],2) for x in range(ev_df.shape[0])])
    df = ev_df[ev_df['BV']<1499].sort_values(by='horizon_pts',ascending=False)[:num]
    ev_df.drop(['horizon_pts', 'horizon_value'], axis=1, inplace=True)
    sns.scatterplot(x=df['BV'], y=df['horizon_pts'], size=df['horizon_value'], legend=False, sizes=(100, 1000))
    ax = plt.gca()
    ax.set_ylim([0.9*min(df['horizon_pts'].tolist()), 1.05*max(df['horizon_pts'].tolist())])
    for i in range(df.shape[0]):
        plt.annotate(df['Name'].iloc[i], (df['BV'].iloc[i]+0.05, df['horizon_pts'].iloc[i]+0.05), fontsize=10)

    plt.xlabel('Price')
    plt.ylabel('xPts')
    plt.show()



pink = '#E5007E'
pink_80 = '#FFC7E6'
pink_60='#FF8FCC'
aqua='#00B4DF'
aqua_80='#C6F4FF'
pink_40='#FF56B3'
pink_d25='#AC005F'
aqua_60='#8CE9FF'
aqua_40='#53DEFF'
aqua_d25='#0087A7'

color_list = [pink, aqua,
              aqua_80, pink_80,aqua_60, pink_60,aqua_40,pink_40,aqua_d25,pink_d25]
goal_points = {
    'G': 0,
    'D': 6,
    'M': 5,
    'F': 4
}

cs_points = {
    'G': 4,
    'D': 4,
    'M': 1,
    'F': 0
}

save_points = {
    'G': 1,
    'D': 0,
    'M': 0,
    'F': 0
}

md_points = {
    'G': 1,
    'D': 1,
    'M': 0,
    'F': 0
}

def barplots(an_ev_df, next_gw, horizon, ids_list):
    plt.style.use('seaborn-darkgrid') 
    plt.figure(figsize=(6, 4), dpi=100)
    names = []
    goals = []
    assists = []
    cs = []
    bonus = []
    md = []
    yc = []
    saves = []
    app = []
    pen_miss_points = []
    for id in ids_list:
        df = an_ev_df[an_ev_df['ID']==id]
        pos = df['Pos'].iloc[0]
        names.append(df['Name'].iloc[0])
        goals.append(sum([goal_points[pos]*df[str(next_gw+q)+'_xG'].iloc[0] for q in range(horizon)]))
        assists.append(sum([3*df[str(next_gw+q)+'_xA'].iloc[0] for q in range(horizon)]))
        cs.append(sum([cs_points[pos]*df[str(next_gw+q)+'_xCS'].iloc[0] for q in range(horizon)]))
        bonus.append(sum([df[str(next_gw+q)+'_xbonus'].iloc[0] for q in range(horizon)]))
        yc.append(sum([-1*df[str(next_gw+q)+'_xyc'].iloc[0] for q in range(horizon)]))
        saves.append(sum([save_points[pos]*df[str(next_gw+q)+'_xsaves'].iloc[0] for q in range(horizon)]))
        md.append(sum([md_points[pos]*df[str(next_gw+q)+'_xmd'].iloc[0] for q in range(horizon)]))
        app.append(sum([df[str(next_gw+q)+'_xapp'].iloc[0] for q in range(horizon)]))
        pen_miss_points.append(sum([df[str(next_gw+q)+'_xpm'].iloc[0] for q in range(horizon)]))
    goals = np.array(goals)
    assists = np.array(assists)
    cs = np.array(cs)
    app = np.array(app)
    bonus = np.array(bonus)
    yc = np.array(yc)
    saves = np.array(saves)
    md = np.array(md)
    pen_miss_points = np.array(pen_miss_points)
    
    # plot bars in stack manner
    plt.bar(names, app, edgecolor='white', color=color_list[0], label='app')
    plt.bar(names, goals, bottom=app, edgecolor='white', color=color_list[1], label='goals')
    plt.bar(names, assists, bottom=app+goals, edgecolor='white', color=color_list[2], label='assists')
    plt.bar(names, cs, bottom=app+goals+assists, edgecolor='white', color=color_list[3], label='cs')
    plt.bar(names, bonus, bottom=app+goals+assists+cs, edgecolor='white', color=color_list[4], label='bonus')
    plt.bar(names, saves, bottom=app+goals+assists+cs+bonus, edgecolor='white', color=color_list[5], label='saves')
    plt.bar(names, yc, edgecolor='white', color=color_list[6], label='yc')
    #plt.bar(names, pen_miss_points, bottom=yc, edgecolor='white', color=color_list[7], label='pen_miss_points')
    plt.bar(names, md, bottom=yc, edgecolor='white', color=color_list[8], label='md')

    ax = plt.gca()
    for i in range(len(ids_list)):
        s = app[i]+goals[i]+assists[i]+cs[i]+bonus[i]+saves[i]
        ax.text(i-0.03*len(ids_list), s, str(round(s+md[i]+yc[i]+pen_miss_points[i], 2)), color='black', fontsize=10)

    ax.set_ylim([-1*horizon, 1.05*(app[0]+goals[0]+assists[0]+cs[0]+bonus[0]+saves[0])])
    plt.xticks(names, fontsize = 10, rotation=45)
    plt.yticks(fontsize = 10)
    plt.legend(loc='upper left', prop={'size': 10}, bbox_to_anchor=(1,1), ncol=1)
    plt.title("xPts Breakdown")
    plt.show()