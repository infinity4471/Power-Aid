import unittest
import requests
import json
import datetime

from active_user import *
from global_data import *


class DayAheadTotalLoadForecast( unittest.TestCase ):
    def test_parameters( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        urls = [ "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Slovakia/PT15M/date/2018-01-01", \
                 "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Slovakia/PT15M/month/2018-01", \
                 "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Slovakia/PT15M/year/2018" ]
        for url in urls:
            response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( response.status_code == 200 or response.status_code == 403)
            if response.status_code == 403:
                admin.logout()
                return
            data = response.json()
            for packet in data:
                self.assertEqual( packet[ 'AreaName' ], 'Slovakia' )
                self.assertEqual( packet[ 'ResolutionCode' ], 'PT15M' )
                self.assertEqual( packet[ 'Year' ], 2018 )
                if 'DayAheadTotalLoadForecastValue' in packet.keys():
                    self.assertEqual( packet[ 'Day' ], 1 )
                    self.assertEqual( packet[ 'Month' ], 1 )
                elif 'DayAheadTotalLoadForecastValue' in packet.keys():
                    self.assertEqual( packet[ 'Month' ], 1 )
        admin.logout()

    def test_ValuesPerDay( self ):
        url = "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Italy/PT15M/month/2018-01"
        admin = active_user( "admin", "nimda123")
        token = admin.login()
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403)
        if response.status_code == 403:
            admin.logout()
            return
        data = response.json()
        for packet in data:
            if packet[ 'Day' ] < 10:
                day = "0" + str( packet[ 'Day' ] )
            else:
                day = str( packet[ 'Day' ] )
            total = 0
            day_response = requests.get("http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Italy/PT15M/date/2018-01-%s" % str( day ), \
                        headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( day_response.status_code == 200 or day_response.status_code == 403)
            if day_response.status_code == 403:
                admin.logout()
                return
            day_data = day_response.json()
            for day_packet in day_data:
                total += float( day_packet[ 'DayAheadTotalLoadForecastValue' ] )
            self.assertEqual( round( total, 3 ), float( packet[ 'DayAheadTotalLoadForecastByDayValue' ] ) )
        admin.logout()

    def test_ValuesPerMonth( self ):
        url = "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Romania/PT15M/year/2018"
        admin = active_user( "admin", "nimda123")
        token = admin.login()
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403)
        if response.status_code == 403:
            admin.logout()
            return
        data = response.json()
        for packet in data:
            if packet[ 'Month' ] < 10:
                month = "0" + str( packet[ 'Month' ] )
            else:
                month = str( packet[ 'Month' ] )
            total = 0
            month_response = requests.get("http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Romania/PT15M/month/2018-%s" % str( month ), \
                        headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( month_response.status_code == 200 or month_response.status_code == 403)
            if month_response.status_code == 403:
                admin.logout()
                return
            month_data = month_response.json()
            for month_packet in month_data:
                total += float( month_packet[ 'DayAheadTotalLoadForecastByDayValue' ] )
            self.assertEqual( round( total, 3 ), float( packet[ 'DayAheadTotalLoadForecastByMonthValue' ] ) )
        admin.logout()
    
    def test_NowParameters( self ):
        admin = active_user( "admin","nimda123" )
        token = admin.login()
        url = "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Italy/PT15M"  
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403)
        if response.status_code == 403:
            admin.logout()
            return
        data = response.json()
        now = datetime.datetime.now()
        for packet in data:
            self.assertEqual( packet[ 'AreaName' ], 'Slovakia' )
            self.assertEqual( packet[ 'ResolutionCode' ], 'PT15M' )
            self.assertEqual( packet[ 'Year' ], str(now.year) )
            if 'DayAheadTotalLoadForecastValue' in packet.keys():
                self.assertEqual( packet[ 'Day' ], str(now.day) )
                self.assertEqual( packet[ 'Month' ], str(now.month) )
            elif 'DayAheadTotalLoadForecastByDayValue' in packet.keys():
                self.assertEqual( packet[ 'Month' ], str(now.month) )
        admin.logout()



if __name__ == '__main__':
    unittest.main()
