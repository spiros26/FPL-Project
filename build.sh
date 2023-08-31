#!/bin/bash

# exit on error
#set -o errexit
echo " cbc"
STORAGE_DIR=.

if [[ ! -d $STORAGE_DIR/cbc ]]; then
  echo "...Downloading cbc"
  mkdir -p $STORAGE_DIR/cbc
  cd $STORAGE_DIR/cbc
  wget -P ./ ftp.us.debian.org/debian/pool/main/c/coinor-cbc/coinor-cbc_2.10.10+really2.10.10+ds1-3_amd64.deb
  dpkg -x ./coinor-cbc_2.10.10+really2.10.10+ds1-3_amd64.deb $STORAGE_DIR/cbc
  rm ./coinor-cbc_2.10.10+really2.10.10+ds1-3_amd64.deb
  cd $HOME/project/src # Make sure we return to where we were
else
  echo "...Using cbc from cache"
fi

# be sure to add Chromes location to the PATH as part of your Start Command
export PATH="${PATH}:cbc/"
pip install -r requirements.txt