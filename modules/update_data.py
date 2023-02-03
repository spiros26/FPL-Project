import os

def clone_data():
    os.system('cd ..')
    os.system('git clone https://github.com/vaastav/Fantasy-Premier-League.git')
    os.system('git clone https://github.com/ChrisMusson/FPL-ID-Map.git')

def update_data():
    os.system('cd ../Fantasy-Premier-League')
    os.system('git pull https://github.com/vaastav/Fantasy-Premier-League.git')