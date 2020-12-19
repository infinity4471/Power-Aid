import csv
import io

def list_to_row( lst ):
    output = ""
    for key in lst:
        output += "%s," % str( key )
    output = output[:-1]
    return output

def dict_to_csv( mydict ):
    csv_output=""
    if len( mydict ) == 0:
        return csv_output
    csv_output += list_to_row( list( mydict[ 0 ].keys() ) )
    csv_output += "\n"
    for elem in mydict:
        csv_output += list_to_row( list( elem.values() ) )
        csv_output += "\n"
    return csv_output
