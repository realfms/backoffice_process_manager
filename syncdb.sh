#!/bin/bash

Q1="CREATE DATABASE IF NOT EXISTS bpm;"

source venv/bin/activate

mysql -uroot --password='' -e "$Q1"

./manage.py syncdb --noinput
