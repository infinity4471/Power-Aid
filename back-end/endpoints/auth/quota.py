from .db import get_query
import datetime
from .apikey import is_admin

def quota_update( mysql_instance, apikey):
    sql_query = "SELECT remaining_quota FROM `users` WHERE apikey = '%s'" %(apikey)
    data = get_query( mysql_instance, sql_query )
    quota = data[0][0]
    if is_admin( mysql_instance, apikey ):
        return True
    elif quota == 0:
        return False
    else:
        quota -= 1
        sql_query = "UPDATE `users` SET remaining_quota = '%s' WHERE apikey = '%s'" % (quota, apikey)
        ret = get_query( mysql_instance, sql_query )
        if ret == "Error":
            raise EnvironmentError
        return True
