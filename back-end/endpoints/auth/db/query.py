import MySQLdb

def get_query( sql_instance, sql_query ):
    cur = sql_instance.connection.cursor()
    try:
        cur.execute( sql_query )
        sql_instance.connection.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print( e )
        return ("Error")
    return cur.fetchall()

def count_rows( sql_instance, table ):
    return get_query( sql_instance, "SELECT COUNT(*) from  %s;" % table )[ 0 ][ 0 ]

def username_exists( sql_instance, username ):
    query = "SELECT * from users where username = '%s';" % username
    data = get_query( sql_instance, query )
    return any( data )

def email_exists( sql_instance, email ):
    query = "SELECT * from users where email = '%s';" % email
    data = get_query( sql_instance, query )
    return any( data )
