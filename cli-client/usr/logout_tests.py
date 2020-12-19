import unittest

from os import path
from user_log import login, logout

class Logout( unittest.TestCase ):
    def test_file_removed( self ):
        login( "admin", "nimda123" )
        logout()
        self.assertFalse( path.exists("softeng19bAPI.token") )

if __name__ == '__main__':
    unittest.main()
