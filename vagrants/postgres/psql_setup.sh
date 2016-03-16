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

apt-get install -y libpq-dev
apt-get install -y postgresql postgresql-contrib
pip3 install psycopg2

sudo -i -u postgres
createdb noctisdb

createuser -P noctis
psql -d noctisdb -c GRANT ALL PRIVILEGES ON DATABASE noctisdb TO noctis;

## And Finally finish up!
date > "$PROVISIONED_ON"
echo "Completed setting up VM for initial postgres work. The next step is allowing to communicate with other machines..."
echo "MODIFY: /etc/postgresql/9.4/main/postgresql.conf >> listen_addresses = '*' "
echo "MODIFY: /etc/postgresql/9.4/main/pg_hba.conf >> host  all  all 0.0.0.0/0 md5 "
echo "RUN: sudo service postgresql restart"
