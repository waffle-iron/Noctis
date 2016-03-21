#!/bin/bash

########################################
# Basic Setup and package installation #
########################################

PROVISIONED_ON=/etc/vm_provision_on_timestamp
if [ -f "$PROVISIONED_ON" ]
then
  echo "VM was already provisioned at: $(cat $PROVISIONED_ON)"
  echo "To run system updates manually login via 'vagrant ssh' and run 'apt-get update && apt-get upgrade'"
  echo ""
  exit
fi

## For Me. ST3 to edit anything I don't want to use vim for.
add-apt-repository ppa:webupd8team/sublime-text-3

# Now update whatever we can
apt-get update

# Code Modification
apt-get install -y git
apt-get install -y sublime-text-installer
apt-get install -y vim

# screen for multi buffer work
apt-get install -y screen

# Python
apt-get install -y python3 python3-pip
apt-get install -y python-dev # Not needed but nice to have.

ln -s /vagrant /home/vagrant/vagrant # symlink

## Okay now let's get the actual server setup ready...
# Virtual Environment
pip3 install virtualenv
virtualenv /opt/poolgresenv

# Django
pip3 install django

# git repos
mkdir ~/Documents/git
cd ~/Documents/git
# jsonrpc
git clone git://github.com/samuraisam/django-json-rpc.git
cd django-json-rpc
python3 setup.py install
# noctis itself
cd ~Documents/git
git clone https://github.com/PrettyTrue/noctis.git

## And Finally finish up!
date > "$PROVISIONED_ON"
echo ""
echo "------------------------------------------------------------------------------------------------"
echo "Completed setting up VM for initial django work. The next step is linking it with your database."
echo "You can by all means change your config to use sqlite3 if you want to avoid the postgresql setup."
echo "To make those changes go to ~/Documents/git/noctis/noctis/noctis/settings.py"
echo "When using the runserver command you'll want to set the ip/port to 0.0.0.0:9878 if using defaults."
echo "------------------------------------------------------------------------------------------------"
echo ""