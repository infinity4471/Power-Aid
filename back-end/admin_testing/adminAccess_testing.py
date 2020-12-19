import unittest
import requests
import json
from active_user import *

class newUser_testing( unittest.TestCase ):
    def test_register( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        url = "http://localhost:8765/energy/api/Admin/users/tester1"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertEqual( response.status_code, 200 )
        admin.logout()
        tester = active_user( "tester1","password")
        token = tester.login()
        url = "http://localhost:8765/energy/api/Admin/users/tester1"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertEqual( response.status_code, 401 )
        tester.logout()


if __name__ == '__main__':
    unittest.main()