import unittest
import requests
import json

from connectivity import connected

class connectivity( unittest.TestCase ):
    def test_connected( self ):
        self.assertEqual( connected("https://www.google.com"), True )
        self.assertEqual( connected("https://www.ntua.gr"), True )
        self.assertEqual( connected("randon-radodff.com"), False )
        self.assertEqual( connected("https://www.yahoo.com"), True )
        self.assertEqual( connected("oidsfioseiso"), False )

if __name__ == '__main__':
    unittest.main()
