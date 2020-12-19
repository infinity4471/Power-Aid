from flask import request,url_for ,redirect
from flask_jsonpify import jsonify
import jwt
import datetime

from .db import get_query
from .file_operations import dict_to_csv
from .global_data import app, mysql, resolutions, inv_resolutions, blacklist, area_type_codes, map_codes
from .auth import apikey_valid, quota_update, is_admin

@app.route( "/energy/api/DayAheadTotalLoadForecast/<AreaName>/<Resolution>/date/<date>", methods=['GET'] )
def DayAheadGetAllData( AreaName, Resolution, date ):
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
    
    if len( date.split("-")) != 3:
        return "Bad request", 400 
    Year, Month, Day = date.split("-")
    
    sql_query = "SELECT * from DayAheadTotalLoadForecast where AreaName = '%s' and ResolutionCodeId = '%s'" % ( AreaName, resolutions[ Resolution ] )
    sql_query += " and Year = '%s' and Month = '%s' and Day = '%s';" % ( Year, Month, Day )

    data = get_query( mysql, sql_query )
    if data == ("Error"):
        return "Bad request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "DayAheadTotalLoadForecast",
                "AreaName": datum[ 9 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 12 ]) ],
                "MapCode": map_codes[ str(datum[ 15 ]) ],
                "ResolutionCode": Resolution,
                "Year": datum[ 5 ],
                "Month": datum[ 6 ],
                "Day": datum[ 7 ],
                "DateTimeUTC": datum[ 8 ],
                "DayAheadTotalLoadForecastValue": str(datum[ 11 ]),
                "UpdateTimeUTC": datum[ 10 ]
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/DayAheadTotalLoadForecast/<AreaName>/<Resolution>/month/<date>", methods=['GET'] )
def DayAheadSumPerDay( AreaName, Resolution, date ):
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
    if len(date.split("-")) != 2:
        return "Bad request", 400
    Year, Month = date.split("-")
    
    sql_query = "SELECT AreaName, AreaTypeCodeId, MapCodeId, ResolutionCodeId, Year, Month, Day, SUM( TotalLoadValue )"
    sql_query += " from DayAheadTotalLoadForecast where AreaName = '%s' and ResolutionCodeId = '%s'" % ( AreaName, resolutions[ Resolution ] )
    sql_query += " and Year = '%s' and Month = '%s' group by Day, AreaTypeCodeId, MapCodeId;" % (  Year, Month )

    data = get_query( mysql, sql_query )
    if data == ("Error"):
        return "Bad request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "DayAheadTotalLoadForecast",
                "AreaName": datum[ 0 ], 
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": Resolution,
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "Day": datum[ 6 ],
                "DayAheadTotalLoadForecastByDayValue": str(datum[ 7 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/DayAheadTotalLoadForecast/<AreaName>/<Resolution>/year/<Year>", methods=['GET'] )
def DayAheadSumPerMonth( AreaName, Resolution, Year ):
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
    
    sql_query = "SELECT AreaName, AreaTypeCodeId, MapCodeId, ResolutionCodeId, Year, Month, SUM( TotalLoadValue ) from DayAheadTotalLoadForecast"
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
                "Dataset": "DayAheadTotalLoadForecast",
                "AreaName": datum[ 0 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": Resolution,
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "DayAheadTotalLoadForecastByMonthValue": str(datum[ 6 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/DayAheadTotalLoadForecast/<AreaName>/<Resolution>", methods=['GET'] )
def DayAheadGetTodayData( AreaName, Resolution ):
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
    now = datetime.datetime.now()
    if not is_admin(mysql, apikey):
        if not apikey_valid( mysql, apikey ):
            return "Not Authorized",401
        if not quota_update( mysql, apikey ):
            return "Out of quota",402
    date = "" + str(now.year) + "-"
    if (now.month < 10):
        date += "0"
    date += str(now.month) + "-"
    if (now.day < 10):
        date += "0"
    date += str(now.day)
    return redirect( url_for( 'DayAheadGetAllData', AreaName=AreaName, Resolution=Resolution, date = date ) )
