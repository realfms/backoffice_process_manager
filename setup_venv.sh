#!/bin/bash

echo Installing generic python requirements...
sudo apt-get install -y python-dev python-pip build-essential 
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install python requirements; exit 1)
echo

echo Installing the virtualenv program...
sudo pip install virtualenv
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install virtualenv; exit 1)
echo

echo Installing postgresql...
sudo apt-get install -y postgresql postgresql-server-dev-all
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install postgresql; exit 1)
echo

echo Creating virtual environment...
virtualenv venv
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to create the environment; exit 1)
. venv/bin/activate
echo

echo Installing requirements from requirements.txt...
cd venv
sudo pip install -r ../requirements.txt
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install the requirements; exit 1)
echo
