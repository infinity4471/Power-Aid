import requests

scopes = [ 'ActualTotalLoad', 'AggregatedGenerationPerType', 'DayAheadTotalLoadForecast', 'AcualVsForecast' ]

def add_user( newuser, passw, email, quota ):
    try: 
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
    except EnvironmentError:
        return "Could not find token! Please try logging in!"
    if passw is None or email is None or quota is None:
       return "Error please enter parameters"
    else:
        data = {
            'username': newuser,
            'passw': passw,
            'email': email,
            'quota': quota, 
            'admin': 0 }
        response = requests.post( "http://localhost:8765/energy/api/Admin/users", data, headers = { "X-OBSERVATORY-AUTH": token }  )
        return response.text

def modify_user( moduser, passw, email, quota ):
    try: 
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
    except EnvironmentError:
        return "Could not find token! Please try logging in!"
    if passw is None or email is None or quota is None:
        return "Error please enter parameters"
    else:
        data = {
            'username': moduser,
            'passw': passw,
            'email': email,
            'quota': quota,
            'admin': 0 }
        response = requests.post( "http://localhost:8765/energy/api/Admin/users/%s" % moduser, data, headers = { "X-OBSERVATORY-AUTH": token }  )
        return response.text

def user_status( usr ):
    try: 
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
    except EnvironmentError:
        return "Could not find token! Please try logging in!"
    response = requests.get( "http://localhost:8765/energy/api/Admin/users/%s" % usr, headers = { "X-OBSERVATORY-AUTH": token }  )
    return response.text

def new_data( scope, source ):
    try: 
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
    except EnvironmentError:
        return "Could not find token! Please try logging in!"
    if scope not in scopes[ 0:3 ] or source is None:
        return "Please specify source filename"
    with open( source, "r" ) as f:
        response = requests.post("http://localhost:8765/energy/api/Admin/%s" % scope, files=dict( file = f ), headers = { "X-OBSERVATORY-AUTH": token }  )
        return response.text
