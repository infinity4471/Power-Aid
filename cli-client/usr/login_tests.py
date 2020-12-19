import unittest

from os import path
from user_log import login, logout

class Login( unittest.TestCase ):
    def test_file_exists( self ):
        login( "admin", "nimda123" )
        self.assertTrue( path.exists("softeng19bAPI.token") )
        logout()
    def test_token_valid( self ):
        token = login( "admin", "nimda123" )
        with open( "softeng19bAPI.token", 'r' ) as f:
            lines = f.readlines()
            file_token = lines[ 0 ]
            self.assertEqual( file_token, token )

if __name__ == '__main__':
    unittest.main()
