from flask import request, redirect, url_for
from flask_jsonpify import jsonify
import datetime
import jwt

from .db import get_query
from .file_operations import dict_to_csv
from .global_data import app, mysql, resolutions, inv_resolutions, blacklist, area_type_codes, map_codes
from .auth import apikey_valid, quota_update, is_admin

@app.route( "/energy/api/ActualvsForecast/<AreaName>/<Resolution>/date/<date>", methods=['GET'] )
def ActualvsForecast( AreaName, Resolution, date ):
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
    Year, Month, Day = date.split("-")
    
    sql_query = "SELECT actual.AreaName, actual.AreaTypeCodeId, actual.MapCodeId, actual.ResolutionCodeId, actual.Year, " 
    sql_query += "actual.Month, actual.Day, actual.DateTime, dayahead.TotalLoadValue, actual.TotalLoadValue "
    sql_query += "FROM ( SELECT * FROM `ActualTotalLoad` WHERE AreaName = '%s' AND ResolutionCodeId = '%s' AND Year = '%s' AND Month = '%s' \
                    AND DAY = '%s') actual, " % ( AreaName, resolutions[ Resolution ], Year, Month, Day )
    sql_query += "( SELECT * FROM `DayAheadTotalLoadForecast` WHERE AreaName = '%s' AND ResolutionCodeId = '%s' AND Year = '%s' \
                    AND Month = '%s' AND DAY = '%s') dayahead " % ( AreaName, resolutions[ Resolution ], Year, Month, Day )
    sql_query += "WHERE actual.Datetime = dayahead.Datetime ORDER BY actual.Datetime"
    
    data = get_query( mysql, sql_query )
    if data == ("Error"):
        return "Bad request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "ActualvsForecast",
                "AreaName": datum[ 0 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": inv_resolutions[ str(datum[ 3 ]) ],
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "Day": datum[ 6 ],
                "DateTimeUTC": datum[ 7 ],
                "DayAheadTotalLoadForecastValue": str(datum[ 8 ]),
                "ActualTotalLoadValue": str(datum[ 9 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data


@app.route( "/energy/api/ActualvsForecast/<AreaName>/<Resolution>/month/<date>", methods=['GET'] )
def TotalSumPerDay( AreaName, Resolution, date ):
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
    
    sql_query = "SELECT actual.AreaName, actual.AreaTypeCodeId, actual.MapCodeId, actual.ResolutionCodeId, actual.Year, "
    sql_query += "actual.Month, actual.Day ,dayaheadsum, actualsum "
    sql_query += "FROM (SELECT *, SUM(TotalLoadValue) AS actualsum FROM `ActualTotalLoad` WHERE AreaName = '%s' " % ( AreaName)
    sql_query += "AND ResolutionCodeId = '%s' AND Year = '%s' and Month = '%s' GROUP BY Day) actual, " % ( resolutions[ Resolution ], Year, Month )
    sql_query += "(SELECT *, SUM(TotalLoadValue) AS dayaheadsum FROM `DayAheadTotalLoadForecast` WHERE AreaName = '%s' " % ( AreaName)
    sql_query += "AND ResolutionCodeId = '%s' AND Year = '%s' and Month = '%s' GROUP BY Day) dayahead " % ( resolutions[ Resolution ], Year, Month )
    sql_query += "WHERE actual.AreaName = dayahead.AreaName AND actual.ResolutionCodeId = dayahead.ResolutionCodeId and "
    sql_query += "actual.Year = dayahead.Year AND actual.Month = dayahead.Month and actual.Day = dayahead.Day"
    data = get_query( mysql, sql_query )
    
    if data == ("Error"):
        return "Bad request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "ActualvsForecast",
                "AreaName": datum[ 0 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": inv_resolutions[ str(datum[ 3 ]) ],
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "Day": datum[ 6 ],
                "DayAheadTotalLoadForecastByDayValue": str(datum[ 7 ]),
                "ActualTotalLoadByDayValue": str(datum[ 8 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/ActualvsForecast/<AreaName>/<Resolution>/year/<Year>", methods=['GET'] )
def TotalSumPerMonth( AreaName, Resolution, Year ):
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
    sql_query = "SELECT actual.AreaName, actual.AreaTypeCodeId, actual.MapCodeId, actual.ResolutionCodeId, actual.Year, "
    sql_query += "actual.Month, dayaheadsum, actualsum "  
    sql_query += "FROM (SELECT *, SUM(TotalLoadValue) AS actualsum FROM `ActualTotalLoad` WHERE AreaName = '%s' " % ( AreaName)
    sql_query += "AND ResolutionCodeId = '%s' AND Year = '%s' GROUP BY Month) actual, " % ( resolutions[ Resolution ], Year )
    sql_query += "(SELECT *, SUM(TotalLoadValue) AS dayaheadsum FROM `DayAheadTotalLoadForecast` WHERE AreaName = '%s' " % ( AreaName)
    sql_query += "AND ResolutionCodeId = '%s' AND Year = '%s' GROUP BY Month) dayahead " % ( resolutions[ Resolution ], Year )
    sql_query += "WHERE actual.AreaName = dayahead.AreaName AND actual.ResolutionCodeId = dayahead.ResolutionCodeId and "
    sql_query += "actual.Year = dayahead.Year AND actual.Month = dayahead.Month"
    data = get_query( mysql, sql_query )
    
    if data == ("Error"):
        return "Bad Request", 400
    if not data:
        return "No data", 403
    sql_replies = []
    for datum in data:
        dict_datum = {
                "Source": "entso-e",
                "Dataset": "ActualvsForecast",
                "AreaName": datum[ 0 ],
                "AreaTypeCode": area_type_codes[ str(datum[ 1 ]) ],
                "MapCode": map_codes[ str(datum[ 2 ]) ],
                "ResolutionCode": inv_resolutions[ str(datum[ 3 ]) ],
                "Year": datum[ 4 ],
                "Month": datum[ 5 ],
                "DayAheadTotalLoadForecastByMonthValue": str(datum[ 6 ]),
                "ActualTotalLoadByMonthValue": str(datum[ 7 ])
                }
        sql_replies.append( dict_datum )
    Format = request.args.get( 'format' )
    if Format == "csv":
        return dict_to_csv( sql_replies )
    json_data = jsonify( sql_replies )
    return json_data

@app.route( "/energy/api/ActualvsForecast/<AreaName>/<Resolution>", methods=['GET'] )
def TotalGetTodayData( AreaName, Resolution ):
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
    return redirect( url_for( 'ActualvsForecast', AreaName=AreaName, Resolution=Resolution, date = date ) )
