#!/bin/bash

sudo apt update
sudo apt-get update
sudo apt upgrade -y
sudo apt install git curl unzip tar make sudo vim wget -y
git clone https://github.com/spiros26/FPL-Project.git
sudo apt install python3-pip

wget https://www.coin-or.org/download/binary/CoinAll/COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
tar -zxvf COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
rm COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
pip install deta
pip install pandas==1.2.3
pip install plotly
pip install python-dotenv
pip install streamlit==1.12.0
pip install streamlit_authenticator==0.1.5
pip install streamlit_option_menu
pip install beutifulsoup4
pip install numpy
pip install python_dateutil
pip install Requests
pip install altair
pip install aiohttp
pip install matplotlib
pip install nest_asyncio
pip install scikit_learn
pip install seaborn
pip install tqdm
pip install understat
pip install xgboost
pip install sasoptpy
pip install fuzzywuzzy
pip install python-Levenshtein

export PATH="${PATH}:/home/ubuntu/bin"
export DETA_KEY=a0esqedqz8y_i3PsPysgdTmg2nbLmesiSGhTCkg3dqdr

nohup python3 -m streamlit run FPL-Project/streamlit_app.py