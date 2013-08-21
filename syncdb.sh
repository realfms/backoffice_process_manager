#!/bin/bash

Q1="CREATE DATABASE IF NOT EXISTS bpm;"

cd $HOME
cd backoffice_process_manager

source venv/bin/activate

cd backoffice_process_manager

mysql -uroot --password='' -e "$Q1"

./manage.py syncdb --noinput
