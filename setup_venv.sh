#!/bin/bash

echo Installing the virtualenv program
pip install virtualenv
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install virtualenv)
echo

echo Creating virtual environment...
virtualenv venv
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to create the environment)
echo

echo Installing postgresql, may ask for password
sudo apt-get install -y postgresql
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install postgresql)
echo

echo Installing postgresql-server, may ask for password
sudo apt-get install -y postgresql-server-dev-all
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install postgresql-server)
echo

echo Installing the python-dev package
sudo apt-get install -y python-dev
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install python-dev)
echo

echo Installing requirements from requirements.txt...
pip install -E venv -r ./requirements.txt
RETVAL=$?
[ $RETVAL -eq 0 ] && (echo; echo Success)
[ $RETVAL -ne 0 ] && (echo; echo Failed to install the requirements)
echo