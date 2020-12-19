from flask import request
from flask_jsonpify import jsonify
from .global_data import app, mysql, scopes, blacklist
from .db import get_query

import datetime
import jwt 

@app.route("/energy/api/Login",methods=['POST'])
def login():
    if request.method=="POST":     
        username, password = request.form['username'], request.form['passw']
        data = get_query( mysql, "SELECT apikey FROM users where username = '%s' and password = '%s'" % ( username,password ) )
        if data == ("Error"):
            return "Bad request", 400
        elif data:
            apikey = data[ 0 ][ 0 ]
            res = get_query( mysql, "UPDATE users SET remaining_quota = total_quota where apikey = '%s'" % apikey )
            if res == ("Error"):
                return "Bad request", 400
            token = jwt.encode( {'apikey': apikey, 'timestamp': str(datetime.datetime.utcnow())}, app.config['SECRET_KEY'] )
            json_results = jsonify( {'token': token.decode('UTF-8') } )
            return json_results, 200
        else:
            return "Incorrect username/password", 400

@app.route("/energy/api/Logout",methods=['POST'])
def logout():
    if request.method == "POST":
        token = request.form['token']
        blacklist.add( token )
    return "OK", 200

@app.route("/energy/api/HealthCheck",methods=['GET'])
def health():
    res = get_query( mysql, "show tables;" )
    if res != ("Error"):
        return jsonify( {'status':'OK'} )
    return jsonify( {'status':'BAD'} )

@app.route("/energy/api/Reset",methods=['POST'])
def reset():
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
    else:
        print("Admin access")
    for scope in scopes:
        get_query( mysql, "DELETE from energy.%s" % scope )
    ret = get_query( mysql, "DELETE from energy.users where not username = 'admin'" )
    if ret == ("Error"):
        return "Bad Request", 400
    for scope in scopes:
        res = get_query( mysql, "SELECT * from energy.%s" % scope )
        if res:
            return jsonify( { 'status': 'BAD' } )
    res = get_query( mysql, "SELECT * from energy.users;")
    if not res or res[ 0 ][ 0 ] != "admin":
        return jsonify( { 'status': 'BAD' } )
    return jsonify( { 'status': 'OK' } )
