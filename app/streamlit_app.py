import pandas as pd  
import plotly.express as px  
import streamlit as st  
import streamlit_authenticator as stauth  
from streamlit_option_menu import option_menu
import database as db
import bcrypt
import requests
import json
import subprocess
import pandas as pd
import os
from datetime import datetime
from PIL import Image
im = Image.open('COPILOT.png')

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def generate_transfer_suggestions(team_data, next_gw, horizon, iterations):
    # Update team data
    os.remove('../solver_fpl/data/team.json')
    with open('../solver_fpl/data/team.json', 'w') as outfile:
        json.dump(team_data, outfile, indent=4)
    # Run solver and get transfers
    os.chdir('../solver_fpl/run/')
    subprocess.call(['python', 'solve_regular.py'])
    filename_list = os.listdir('../data/results/')[-iterations:]
    transfer_breakdown_list = []
    for filename in filename_list:
        f = os.path.join('../data/results/', filename)
        if os.path.isfile(f):
            plan = pd.read_csv(f)
            gws = [next_gw + x for x in range(horizon)]
            transfers = []
            transfer_breakdown = []
            for gw in gws:
                players_in = []
                players_out = []
                players_in += plan[(plan['week']==gw) & (plan['transfer_in']==1)]['name'].to_list()
                players_out += plan[(plan['week']==gw) & (plan['transfer_out']==1)]['name'].to_list()
                transfers.append((players_in, players_out))
            for i in range(horizon):
                transfers_gw = transfers[i]
                transfer_breakdown.append(', '.join(transfers_gw[1]) + ' -> ' + ', '.join(transfers_gw[0]))
            transfer_breakdown_list.append(transfer_breakdown)
        else:
            st.error('Error with result files')
    os.chdir('../../app/')
    response = os.listdir('./results/')[-1]
    response = os.path.join('./results/', response)
    result_table = pd.read_csv(response)
    return transfer_breakdown_list, result_table[['iter', 'buy', 'sell', 'score']]



st.set_page_config(page_title="FPL Copilot", page_icon=im, layout="centered")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

placeholder_menu = st.empty()
with placeholder_menu.container():
    choice = option_menu(None, ["Home", "Login", "SignUp"], 
        icons=['house', 'check-square', "box-arrow-in-right"], 
        menu_icon="cast", default_index=0, orientation="horizontal")

if choice == "Home":
	st.title("Home ⚽")

   

elif choice == "SignUp":
    st.title("Create New Account")
    new_user = st.text_input("Username")
    new_name = st.text_input("Name")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password",type='password')
    users = db.fetch_all_users()
         
    if st.button("Signup"):
        if new_user in [user['key'] for user in users]:
             st.error("Username exists.")
        elif len(new_name) < 1:
             st.error("Please enter a valid name.")
        elif len(new_email) < 1 or '@' not in new_email:
             st.error("Please enter a valid email.")
        elif len(new_password) < 5:
             st.error("Please enter a password of atleast 5 characters.")
        else:
            db.insert_user(new_user, new_name, new_email, hash_password(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")


elif choice == "Login":
        # --- USER AUTHENTICATION ---
        users = db.fetch_all_users()

        usernames = [user["key"] for user in users]
        names = [user["name"] for user in users]
        hashed_passwords = [user["password"] for user in users]
        authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
            "cookie_name", "cookie_key", cookie_expiry_days=30)
        name, authentication_status, username = authenticator.login("Login", "main")

        if authentication_status == False:
            st.error("Username/password is incorrect")
        if authentication_status == None:
            st.warning("Please enter your username and password")
        if authentication_status:

             # Get the next gameweek
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
            df = pd.DataFrame(requests.get(url).json()['events'])
            i=0
            while dt_string > df['deadline_time'].iloc[i]:
                i = i + 1
            next_gw = df['id'].iloc[i]

            placeholder_menu.empty()
            selected = option_menu(None, ["Copilot", "Autopilot", "About"], 
                icons=['airplane', 'airplane-fill', "info-circle"], 
                menu_icon="cast", default_index=0, orientation="horizontal")
            
            st.title(f'Welcome to FPL Copilot *{name}*! ✈️')

            # Main
            st.subheader('Suggested Transfers')
            st.sidebar.header('FPL Credentials')
            team_id = st.sidebar.text_input("Team ID")

            if st.sidebar.button('Get Team Data'):
                with requests.Session() as session:
                    if next_gw == 1:
                        st.success('Preseason Time! Select the solver settings and click on Suggest Transfers.')
                    else:
                        data = session.get(f'https://fantasy.premierleague.com/api/entry/{team_id}/event/{next_gw-1}/picks/')
                        team_data = data.json()
                        with open("team_data.json", "w") as outfile:
                            json.dump(team_data, outfile, indent=4)
                        st.write('Team ID:', team_id)
            
            column1, column2 = st.columns(2)   

            #Suggest Transfers
            with open('team_data.json', 'r') as openfile:
                team_data = json.load(openfile)
                
            if team_data:
                st.sidebar.header('Solver Settings')
                # Call function to generate transfer suggestions for the user's FPL team
                decay = st.sidebar.number_input('Decay', value=0.85)
                iterations = st.sidebar.radio('Solver Iterations', options=[1,2,3,4,5], horizontal=True)
                horizon = st.sidebar.radio('Horizon', options=[1,2,3,4,5,6,7,8], horizontal=True)
                ft_value = st.sidebar.number_input('Free Transfer Value', min_value=0.0, max_value=3.0, value=1.5, step=0.1)
                no_transfer_last_gws = st.sidebar.radio('No Transfers Planned for the Last How Many Gameweeks?', options=list(range(horizon)), horizontal=True)
                locked = st.sidebar.multiselect('Locked Players', options=list(range(1,607))) 
                banned = st.sidebar.multiselect('Banned Players', options=list(range(1,607)))
                st.sidebar.header('Chips')
                use_wc = st.sidebar.radio('Wildcard', options=[None]+list(range(next_gw, next_gw+horizon)), horizontal=True) 
                use_fh = st.sidebar.radio('Free Hit', options=[None]+list(range(next_gw, next_gw+horizon)), horizontal=True) 
                use_bb = st.sidebar.radio('Bench Boost', options=[None]+list(range(next_gw, next_gw+horizon)), horizontal=True) 
                
                if st.sidebar.button('Suggest Transfers'):
                    placeholder = st.empty()
                    with placeholder.container():
                        st.write('Solver is running...Please wait...')
                    with open('../solver_fpl/data/regular_settings.json', 'r') as openfile:
                        settings_file = json.load(openfile)

                    settings_file['preseason'] = False
                    if next_gw == 1:
                        settings_file['preseason'] = True
                    settings_file['horizon'] = horizon
                    settings_file['decay_base'] = decay
                    settings_file['ft_value'] = ft_value
                    settings_file['banned'] = banned + [100] # id 100 is dervisoglu
                    settings_file['locked'] = locked
                    settings_file['iteration'] = iterations
                    settings_file['no_transfer_last_gws'] = no_transfer_last_gws
                    settings_file['use_wc'] = use_wc
                    settings_file['chip_limits']['wc'] = 0
                    settings_file['chip_limits']['fh'] = 0
                    settings_file['chip_limits']['bb'] = 0
                    if use_wc != None:
                        settings_file['chip_limits']['wc'] = 1
                    settings_file['use_fh'] = use_fh
                    if use_fh != None:
                        settings_file['chip_limits']['fh'] = 1
                    settings_file['use_bb'] = use_bb
                    if use_bb != None:
                        settings_file['chip_limits']['bb'] = 1
                    os.remove('../solver_fpl/data/regular_settings.json')
                    with open("../solver_fpl/data/regular_settings.json", "w") as outfile:
                        json.dump(settings_file, outfile, indent=4)

                    transfer_suggestions, score_table = generate_transfer_suggestions(team_data, next_gw, horizon, iterations)
                    placeholder.empty()
                    with column1:
                        st.write(score_table)
                    with column2:
                        st.write(transfer_suggestions)
                    
                    columns = st.columns(iterations) 
                    st.subheader('Detailed Plan')
                    for x in range(iterations):
                        with columns[x]:
                            with open(f'plan{x}.txt') as f:
                                plan = f.readlines()
                                for i in range(len(plan)):
                                    st.write(plan[i])
            
            # Box
            st.subheader('Expected Points')
            try:
                data = pd.read_csv('../Projections/ALEX-23/alex-GW' + str(next_gw) + '.csv')
            except:
                st.error('File not yet available. Try later.')
            st.write(data)

            # Download box
            csv = convert_df(data)
            st.download_button(
            "Download",
            csv,
            "fplcopilot.csv",
            "text/csv",
            key='download-csv'
            )
            authenticator.logout('Logout', 'main')

twitter_link1 = '[FPL Copilot - Twitter](https://twitter.com/fplcopilot)'
twitter_link2 = '[Spiros Valouxis - Twitter](https://twitter.com/SpirosValouxis)'
linkedInlink = '[Spiros Valouxis - LinkedIn](https://www.linkedin.com/in/spiros-valouxis-642511233/)'

st.header("Contact")
st.write(twitter_link1, '   |   ', twitter_link2, '   |   ', linkedInlink)