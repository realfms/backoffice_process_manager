#/bin/bash

echo  "Installing base platform dependencies!"

sudo yum erase -y ruby rubygems
sudo rm /usr/bin/gem /usr/bin/ruby

sudo yum -y install git python27 python-pip
sudo easy_install virtualenv

sudo ln -s /usr/bin/python-pip /usr/bin/pip

#FMS - Download from repo the ruby19 package to /dev/shm and install
wget http://10.95.158.5/repo/backoffice_process_manager/ruby-1.9.3p448-1.el6.x86_64.rpm -O /dev/shm/ruby19.rpm
sudo rpm -i /dev/shm/ruby19.rpm

sudo ln -s /usr/bin/gem1.9 /usr/bin/gem
sudo ln -s /usr/bin/ruby1.9 /usr/bin/ruby

sudo gem install foreman

echo  "Installation FINISHED!"

