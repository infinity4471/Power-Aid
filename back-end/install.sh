#!/bin/bash

sudo apt-get upgrade;
sudo apt-get update;

#pip and virtual environment
sudo apt-get install python-virtualenv;
sudo apt-get install python-pip;
sudo apt-get install virtualenv;

#mysql server
sudo apt install mysql-server;
sudo mysql_secure_installation;

#mysql client

sudo apt-get install mysql-client;

#update tools for pip

sudo -H pip install --upgrade setuptools;
sudo -H pip install wheel;

#miscelaneous installations

sudo apt-get install python3.6-dev libmysqlclient-dev;
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev;
sudo apt-get install unzip;

#pip modules for python

sudo -H pip install --upgrade pip

sudo -H pip install pyjwt;
sudo -H pip install werkzeug;
sudo -H pip install mysql-connector;
sudo -H pip install mysql-connector-python;
sudo -H pip install Flask;
sudo -H pip install flask_restful;
sudo -H pip install flask-mysql;
sudo -H pip install flask-mysqldb;
sudo -H pip install flask-jsonpify;
sudo -H pip install flask_jwt_extended;
sudo -H pip install flask_ext;
sudo -H pip install unittest2;
