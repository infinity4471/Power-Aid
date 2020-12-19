import unittest
import requests
import json
from active_user import *

class newUser_testing( unittest.TestCase ):
    def test_register( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        register_data = {
                'username': 'tester1',
                'email': 'tester@test.gr', 
                'passw': 'password',
                'quota': 0,
                'admin': 0}
        register_url = "http://localhost:8765/energy/api/Admin/users"
        response = requests.post( register_url, register_data, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertEqual( response.status_code, 200 )
        url = "http://localhost:8765/energy/api/Admin/users/tester1"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertEqual( response.status_code, 200 )
        resp_data = json.loads( response.text )
        email = resp_data['email']
        self.assertEqual( email, 'tester@test.gr' )
        admin.logout()

if __name__ == '__main__':
    unittest.main()
