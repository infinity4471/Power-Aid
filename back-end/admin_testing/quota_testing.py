import unittest
import requests
import json
from active_user import *

class newUser_testing( unittest.TestCase ):
    def test_adminQuota( self ):
        admin = active_user( "admin", "nimda123" )
        token = admin.login()
        response = requests.get("http://localhost:8765/energy/api/Admin/users/admin", headers = { "X-OBSERVATORY-AUTH": token } )
        quota = response.json()[ 'remaining_quota' ]
        url = "http://localhost:8765/energy/api/ActualTotalLoad/Montenegro/PT15M/month/2018-01"
        requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        response = requests.get("http://localhost:8765/energy/api/Admin/users/admin", headers = { "X-OBSERVATORY-AUTH": token } )
        new_data = response.json()
        new_quota = new_data[ 'remaining_quota' ] 
        self.assertTrue( new_quota, quota )

if __name__ == '__main__':
    unittest.main()
