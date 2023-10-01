#!/bin/bash

wget https://www.coin-or.org/download/binary/CoinAll/COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
tar -zxvf COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz
rm COIN-OR-1.7.4-linux-x86_64-gcc4.7.2-static.tar.gz

# export PATH="${PATH}:/opt/render/project/src/bin"

pip install -r requirements.txt