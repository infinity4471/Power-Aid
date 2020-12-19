from flask import Flask,request,render_template,session
from flask_restful import Api
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import json

def initialize():
    app = Flask(__name__)
    app.secret_key='okboomer'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'energy'

    mysql=MySQL()
    mysql.init_app(app)
    
    blacklist = set()
    return app, mysql, blacklist
