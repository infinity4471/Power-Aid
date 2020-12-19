from flask import request, url_for, redirect
from flask_jsonpify import jsonify
import datetime
import jwt

from .db import get_query
from .file_operations import dict_to_csv
from .global_data import app, mysql, resolutions, inv_resolutions, area_type_codes, map_codes, blacklist
from .auth import apikey_valid, quota_update, is_admin

@app.route( "/energy/api/ActualTotalLoad/<AreaName>/<Resolution>/date/<date>", methods=['GET'] )
def ActualGetAllData( AreaName, Resolution, date ):
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
        if not apikey_valid( mysql, apikey ):
            return "Not Authorized",401
        if not quota_update( mysql, apikey ):
            return "Out of quota",402
    if len(date.split("-")) != 3:
        return "Bad request", 400 
    Year, Month, Day = tuple( date.split("-") )
    sql_query = "SELECT * from ActualTotalLoad where AreaName = '%s' and ResolutionCodeId = '%s'" % ( AreaName, resolutions[ Resolution ] )
    sql_query += " and Year = '%s' and Month = '%s' and Day = '%s' order by DateTime;" % ( Year, Month, Day )     
    
    data = get_query( mysql, sql_query )
    if data == ("Error"):
        return "Bad request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "ActualTotalLoad",
                "AreaName": datum[ 9 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 12 ]) ],
                "MapCode": map_codes[ str(datum[ 15 ]) ],
                "ResolutionCode": Resolution,
                "Year": datum[ 5 ],
                "Month": datum[ 6 ],
                "Day": datum[ 7 ],
                "DateTimeUTC": datum[ 8 ],
                "ActualTotalLoadValue": str(datum[ 11 ]),
                "UpdateTimeUTC": datum[ 10 ]
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/ActualTotalLoad/<AreaName>/<Resolution>", methods=['GET'] )
def ActualGetTodayData( AreaName, Resolution ):
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
        if not apikey_valid( mysql, apikey ):
            return "Not Authorized",401
        if not quota_update( mysql, apikey ):
            return "Out of quota",402
    now = datetime.datetime.now()
    date = "" + str(now.year) + "-"
    if (now.month < 10):
        date += "0"
    date += str(now.month) + "-"
    if (now.day < 10):
        date += "0"
    date += str(now.day)
    return redirect( url_for( 'ActualGetAllData', AreaName=AreaName, Resolution=Resolution, date = date ) )

@app.route( "/energy/api/ActualTotalLoad/<AreaName>/<Resolution>/month/<date>", methods=['GET'] )
def ActualSumPerDay( AreaName, Resolution, date ):
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
        if not apikey_valid( mysql, apikey ):
            return "Not Authorized",401
        if not quota_update( mysql, apikey ):
            return "Out of quota",402
    if len( date.split("-") ) != 2:
        return "Bad request", 400
    Year, Month = tuple( date.split("-") )
    sql_query = "SELECT AreaName, AreaTypeCodeId, MapCodeId, ResolutionCodeId, Year, Month, Day, SUM( TotalLoadValue )"
    sql_query += " from ActualTotalLoad where AreaName = '%s' and ResolutionCodeId = '%s'" % ( AreaName, resolutions[ Resolution ] )
    sql_query += " and Year = '%s' and Month = '%s' group by Day, AreaTypeCodeId, MapCodeId;" % (  Year, Month ) 

    data = get_query( mysql, sql_query )
    if data == ("Error"):
        return "Bad Request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "ActualTotalLoad",
                "AreaName": datum[ 0 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": Resolution,
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "Day": datum[ 6 ],
                "ActualTotalLoadByDayValue": str(datum[ 7 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/ActualTotalLoad/<AreaName>/<Resolution>/year/<Year>", methods=['GET'] )
def ActualSumPerMonth( AreaName, Resolution, Year ):
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
        if not apikey_valid( mysql, apikey ):
            return "Not Authorized",401
        if not quota_update( mysql, apikey ):
            return "Out of quota",402
    sql_query = "SELECT AreaName, AreaTypeCodeId, MapCodeId, ResolutionCodeId, Year, Month, SUM( TotalLoadValue ) from ActualTotalLoad"
    sql_query += " where AreaName = '%s' and ResolutionCodeId = '%s'" % ( AreaName, resolutions[ Resolution ] )
    sql_query += " and Year = '%s' group by Month, AreaTypeCodeId, MapCodeId;" % Year

    data = get_query( mysql, sql_query )
    if data == ("Error"):
        return "Bad request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "ActualTotalLoad",
                "AreaName": datum[ 0 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": Resolution,
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "ActualTotalLoadByMonthValue": str(datum[ 6 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

