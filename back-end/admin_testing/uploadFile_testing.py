import unittest
import requests
import json
from active_user import *

class uploadFile_testing( unittest.TestCase ):
    def test_modufyInfo( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        source = "test_file.csv"
        url = "http://localhost:8765/energy/api/Admin/ActualTotalLoad"
        with open( source, "r" ) as f:
            response = requests.post(url, files=dict( file = f ), headers = { "X-OBSERVATORY-AUTH": token }  )
            self.assertEqual( response.status_code, 200 )
        admin = active_user( "admin", "nimda123" )
        url = "http://localhost:8765/energy/api/ActualTotalLoad/DE-AT-LU/PT60M/year/1075"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertEqual( response.status_code, 200 )
        admin.logout()
    
if __name__ == '__main__':
    unittest.main()
