import unittest
import requests
import json
import jwt

class user_testing( unittest.TestCase ):
    def test_authentication( self ):
        login_data = {
                'username': 'admin',
                'passw': 'nimda123' }
        login_url = "http://localhost:8765/energy/api/Login"
        response = requests.post( login_url, login_data )
        resp_data = json.loads( response.text )
        token = resp_data[ 'token' ]
        self.assertEqual( response.status_code, 200 )
        logout_url = "http://localhost:8765/energy/api/Logout"
        response = requests.post( logout_url, {'token': token} )
        login_data = {
                'username': 'admin',
                'passw': 'nimda' }
        response = requests.post( login_url, login_data )
        self.assertEqual( response.status_code, 400 )

    def test_token( self ):
        login_data = {
                'username': 'admin',
                'passw': 'nimda123' }
        login_url = "http://localhost:8765/energy/api/Login"
        response = requests.post( login_url, login_data )
        resp_data = json.loads( response.text )
        token = resp_data[ 'token' ]
        self.assertEqual( response.status_code, 200 )
        url = "http://localhost:8765/energy/api/ActualTotalLoad/Austria/PT60M/date/2018-01-04"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertEqual( response.status_code, 200 )
        logout_url = "http://localhost:8765/energy/api/Logout"
        response = requests.post( logout_url, {'token': token} )
    
    

if __name__ == '__main__':
    unittest.main()
