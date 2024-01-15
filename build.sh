#!/bin/bash

cd home/ubuntu

sudo apt update
sudo apt-get update
sudo apt upgrade -y
sudo apt install git tar wget -y
git clone https://github.com/spiros26/FPL-Project.git
sudo apt install python3 python3-pip -y

wget https://www.coin-or.org/download/binary/CoinAll/COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
tar -zxvf COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
rm COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz

echo "Putting CBC into the PATH"
export PATH="${PATH}:/home/ubuntu/bin"

echo "Setting DETA KEY env variable.."
export DETA_KEY=a0esqedqz8y_i3PsPysgdTmg2nbLmesiSGhTCkg3dqdr

pip install deta
pip install pandas
pip install plotly
pip install python-dotenv
pip install streamlit
pip install streamlit_authenticator==0.1.5
pip install streamlit_option_menu
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


cd FPL-Project
python3 -m streamlit run streamlit_app.py

#tail -f /var/log/cloud-init-output.log
