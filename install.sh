#!/bin/sh
echo "install system packages"
sudo apt-get install apache2 mysql-server mysql-client python2.7 python-pip python-dev build-essential vim nano git
sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert
sudo aptitude install libapache2-mod-wsgi
sudo apt-get install python-mysqldb
echo "instll python packages"
sudo pip install django==1.9
sudo pip install Pillow
sudo pip install django-wkhtmltopdf==2.0.3
echo "instll python wkhtmltopdf"
wget https://bitbucket.org/wkhtmltopdf/wkhtmltopdf/downloads/wkhtmltox-0.13.0-alpha-7b36694_linux-trusty-amd64.deb
sudo dpkg -i wkhtmltox-0.13.0-alpha-7b36694_linux-trusty-amd64.deb
sudo apt-get -f install




