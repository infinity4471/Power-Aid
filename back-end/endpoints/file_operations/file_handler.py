from .db import get_query
import csv

def is_csv( filename ):
    return '.' in filename and filename.split('.')[ 1 ].lower() == 'csv'

def valid_header( sql_instance, table, filep ):
    iterator = csv.reader( filep, delimiter=';' )
    csv_columns = next( iterator )
    db_columns = get_query( sql_instance, "show columns from %s;" % table )
    column_names = [ column[ 0 ] for column in db_columns ]
    return csv_columns == column_names

def get_rows( filep ):
    iterator = csv.reader( filep, delimiter=';' )
    return [ row for row in iterator ]
