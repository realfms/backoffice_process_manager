#!/bin/bash

echo Installing the package manager 'pip'
sudo apt-get install -y python-pip python-dev build-essential 
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install pip; exit 1)
echo

echo Installing the virtualenv program
sudo pip install virtualenv --upgrade
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install virtualenv; exit 1)
echo

echo Creating virtual environment...
virtualenv venv
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to create the environment; exit 1)
echo

echo Installing postgresql, may ask for password
sudo apt-get install -y postgresql postgresql-server-dev-all
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install postgresql; exit 1)
echo

echo Installing requirements from requirements.txt...
sudo pip install -E venv -r ./requirements.txt
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install the requirements; exit 1)
echo
