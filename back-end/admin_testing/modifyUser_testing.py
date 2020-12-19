import unittest
import requests
import json
from active_user import *

class modifyUser_testing( unittest.TestCase ):
    def test_getInfo( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        url = "http://localhost:8765/energy/api/Admin/users/tester1"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token })
        self.assertEqual( response.status_code, 200 )
        admin.logout()
    
    def test_modifyInfo( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        modify_data = {
                'username': 'tester1',
                'email': 'tester100@test.gr', 
                'passw': 'password',
                'quota': '0',
                'admin' : 'False'}
        url = "http://localhost:8765/energy/api/Admin/users/tester1"
        response = requests.post( url, modify_data,  headers = { "X-OBSERVATORY-AUTH": token })
        self.assertEqual( response.status_code, 200 )
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token })
        resp_data = json.loads( response.text )
        email = resp_data['email']
        self.assertEqual( email, 'tester100@test.gr' )
        admin.logout()
    

if __name__ == '__main__':
    unittest.main()