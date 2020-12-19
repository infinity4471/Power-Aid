import requests
from os import system
from os import path
import json

def login( username, passw ):
    if path.exists( "softeng19bAPI.token" ):
        return "Logout first before logging in!"
    data = {
            'username': username,
            'passw': passw }
    response = requests.post( "http://localhost:8765/energy/api/Login", data)
    try:
        if response.status_code == 400:
            return "Bad Request while logging in"
        resp_data = json.loads( response.text )
        token = resp_data['token']
    except EnvironmentError:
        return "Bad Request"
    try:
        with open( "softeng19bAPI.token", "w" ) as f:
            f.write( token )
        return token
    except EnvironmentError:
        return "Could Not write token to file!"

def logout():
    try: 
        with open("softeng19bAPI.token","r") as f:
            lines = f.readlines()
            token = lines[0]
            response = requests.post( "http://localhost:8765/energy/api/Logout", {'token': token} )
            if response.status_code == 400:
                return "Bad Request while logging out"
            system("rm softeng19bAPI.token")
            return response.text
    except EnvironmentError:
        return "softeng19bAPI.token does not exist, try logging in first!"
