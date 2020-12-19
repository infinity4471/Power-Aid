import requests
import json

class active_user:
    def __init__( self, username, passw ):
        self.username = username
        self.passw = passw
        self.token = None

    def login( self ):
        login_data = {
                'username': self.username,
                'passw': self.passw }
        
        response = requests.post( "http://localhost:8765/energy/api/Login", login_data )
        resp_data = json.loads( response.text )
        self.token = resp_data[ 'token' ]
        return self.token

    def logout( self ):
        response = requests.post( "http://localhost:8765/energy/api/Logout", {'token': self.token} )
