from .db import get_query
import random
import string

def apikey_valid( mysql_instance, apikey):
    sql_query = "SELECT COUNT(*) FROM `users` WHERE apikey = '%s'" %(apikey)
    data = get_query( mysql_instance, sql_query )
    return data[0][0]

def is_admin(mysql_instance, apikey):
    sql_query = "SELECT admin FROM `users` WHERE apikey = '%s'" %(apikey)
    data = get_query( mysql_instance, sql_query )
    if (data[0][0] == 1):
        result = True
    else:
        result = False
    return result

def apikey_generator():
    apikey = ""
    for rep in range( 3 ):
        apikey += ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        if rep < 2:
            apikey += '-'
    return apikey

def apikey_create( mysql_instance ):
    while True:
        apikey = apikey_generator()
        sql_query = "SELECT COUNT(*) FROM `users` WHERE apikey = '%s'" %(apikey)
        data = get_query( mysql_instance, sql_query )
        count = data[0][0]
        if count == 0:
            return apikey
