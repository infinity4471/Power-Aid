from flask import request
from flask_jsonpify import jsonify
from werkzeug.utils import secure_filename
import jwt

import io
import csv

from .file_operations import is_csv, valid_header, get_rows
from .auth import apikey_valid, apikey_create, is_admin
from .global_data import app, mysql, scopes, blacklist
from .db import get_query, count_rows, username_exists, email_exists

@app.route( "/energy/api/Admin/users", methods=['POST'] )
def new_user():
    token = request.headers.get( 'X-OBSERVATORY-AUTH', None )
    if token is None:
        return "Bad request", 400
    if token in blacklist:
        return "Not Authorized", 401
    try:
        data = jwt.decode( token, app.config['SECRET_KEY'] )
        apikey = data[ 'apikey' ]
    except DecodeError:
        return "Problem during token decoding", 400
    if not is_admin(mysql, apikey):
        return "Not Authorized", 401
    if request.method == "POST":
        fields = request.form
        username, email, password, quota, admin= fields['username'], fields['email'], fields['passw'], fields['quota'], fields['admin']
        if not isinstance( int( quota ), int ):
            return "Quota Not an Integer", 400
        if username is None or email is None or password is None or quota is None or admin is None:
            return "Missing parameters", 400
        if username_exists( mysql, username ):
            return "Username Exists", 400
        elif email_exists( mysql, email ):
            return "Email Exists", 400
        else:
            user_apikey = apikey_create( mysql )
            insert_query = "INSERT INTO users(username,email,password, apikey, total_quota, remaining_quota, admin ) VALUES('%s','%s','%s', '%s', '%s', '%s', %s );" \
                            % ( username, email, password, user_apikey, quota, quota, admin )
            res = get_query( mysql, insert_query )
            if res == ("Error") or res is None:
                return "Bad request", 400
            return user_apikey, 200

@app.route( "/energy/api/Admin/users/<usr>", methods=['GET', 'POST'] )
def modify_user( usr ):
    token = request.headers.get( 'X-OBSERVATORY-AUTH', None )
    if token is None:
        return "Bad request", 400
    if token in blacklist:
        return "Not Authorized", 401
    try:
        data = jwt.decode( token, app.config['SECRET_KEY'] )
        apikey = data[ 'apikey' ]
    except DecodeError:
        return "Problem during token decoding", 400
    if not is_admin(mysql, apikey):
        return "Not Authorized", 401
    if request.method == 'POST': #modify user data
        fields = request.form
        username, new_email, new_password, new_quota, admin = fields['username'], fields['email'], fields['passw'], fields['quota'], fields['admin']
        if not isinstance( int( new_quota ), int ):
            return "Quota Not an Integer", 400
        if username is None or new_email is None or new_password is None or new_quota is None or admin is None:
            return "Missing parameters", 400
        sql_query = "UPDATE `users` SET email='%s', password='%s', total_quota='%s', remaining_quota='%s', admin = %s WHERE username = '%s';" \
                    % ( new_email, new_password, new_quota, new_quota, admin, usr)
        ret = get_query( mysql, sql_query ) 
        if ret == ("Error"):
            return "Bad Request", 400
        return "OK", 200
    elif request.method == 'GET': #show user data
        query = "SELECT * from users where username = '%s';" % usr 
        sql_data = get_query( mysql, query )
        if not sql_data:
            return "No Data", 403
        user_data = {
                    'username': sql_data[ 0 ][ 0 ],
                    'email': sql_data[ 0 ][ 1 ],
                    'total_quota': sql_data[ 0 ][ 4 ],
                    'remaining_quota': sql_data[ 0 ][ 5 ],
                    'admin' : sql_data[ 0 ][ 6 ]
                }
        json_data = jsonify( user_data )
        return json_data

@app.route("/energy/api/Admin/<scope>", methods=['POST'] )
def new_file( scope ):
    token = request.headers.get( 'X-OBSERVATORY-AUTH', None )
    if token is None:
        return "Bad request", 400
    if token in blacklist:
        return "Not Authorized", 401
    try:
        data = jwt.decode( token, app.config['SECRET_KEY'] )
        apikey = data[ 'apikey' ]
    except DecodeError:
        return "Problem during token decoding", 400
    if not is_admin(mysql, apikey):
        return "Not Authorized", 401
    if scope not in scopes[ 0:3 ]: #We don't want ActualVsForecast
        return "Bad Request", 400
    if request.method == 'POST': #upload file and insert into db
        if 'file' not in request.files:
            return "Bad Request", 400
        file = request.files['file']
        if file.filename == '':
            return "Bad Request", 400
        if file and is_csv(file.filename):
            filep = io.StringIO( file.stream.read().decode("utf-8-sig"), newline = None) 
            if not valid_header( mysql, scope, filep ): #check if columns match 
                return "Bad Request", 400
            file_rows = get_rows( filep )
            totalRecordsInFile, totalRecordsImported = len( file_rows ), 0
            for row in file_rows:
                insert_query = "INSERT INTO %s VALUES( %s );" % ( scope, str( row )[ 1:-1 ] )
                if get_query( mysql, insert_query ) != ("Error"):
                    totalRecordsImported += 1
            totalRecordsInDatabase = count_rows( mysql, scope )
            ret_val = {
                    'totalRecordsInFile': totalRecordsInFile,
                    'totalRecordsImported': totalRecordsImported,
                    'totalRecordsInDatabase': totalRecordsInDatabase,
                    }
            return jsonify( ret_val ), 200
        return "Bad Request", 400
