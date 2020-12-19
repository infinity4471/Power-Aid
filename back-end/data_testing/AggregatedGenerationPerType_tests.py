import unittest
import requests
import json
import datetime 

from active_user import *
from global_data import *

class AggregatedGenerationPerType( unittest.TestCase ):
    def test_parameters( self ):
        admin = active_user("admin","nimda123")
        token = admin.login()
        urls = [ "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/1/PT60M/date/2018-01-06", \
                 "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/1/PT60M/month/2018-01", \
                 "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/1/PT60M/year/2018" ]
        for url in urls:
            response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( response.status_code == 200 or response.status_code == 403 )
            if response.status_code == 403:
                admin.logout()
                return
            data = response.json()
            for packet in data:
                self.assertEqual( packet[ 'AreaName' ], 'Austria' )
                self.assertEqual( packet[ 'ProductionType' ], prod_types[ '1' ] )
                self.assertEqual( packet[ 'ResolutionCode' ], 'PT60M' )
                self.assertEqual( packet[ 'Year' ], 2018 )
                if 'ActualGenerationOutputValue' in packet.keys():
                    self.assertEqual( packet[ 'Day' ], 6 )
                    self.assertEqual( packet[ 'Month' ], 1 )
                elif 'ActualGenerationOutputByDayValue' in packet.keys():
                    self.assertEqual( packet[ 'Month' ], 1 )
        admin.logout()

    def test_ValuesPerDay( self ):
        url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Romania/12/PT15M/month/2018-01"
        admin = active_user("admin","nimda123")
        token = admin.login()
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403 )
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
            url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Romania/12/PT15M/date/2018-01-%s" % str( day )
            day_response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( day_response.status_code == 200 or day_response.status_code == 403)
            if day_response.status_code == 403:
                admin.logout()
                return
            day_data = day_response.json()
            for day_packet in day_data:
                total += float( day_packet[ 'ActualGenerationOutputValue' ] )
            self.assertEqual( round( total, 3 ), float( packet[ 'ActualGenerationOutputByDayValue' ] ) )
        admin.logout()

    def test_ValuesPerMonth( self ):
        url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Romania/12/PT15M/year/2018"
        admin = active_user("admin","nimda123")
        token = admin.login()
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403 )
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
            url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Romania/12/PT15M/month/2018-%s" % str( month )
            month_response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( month_response.status_code == 200 or month_response.status_code == 403 )
            if month_response.status_code == 403:
                admin.logout()
                return
            month_data = month_response.json()
            for month_packet in month_data:
                total += float( month_packet[ 'ActualGenerationOutputByDayValue' ] )
            self.assertEqual( round( total, 3 ), float( packet[ 'ActualGenerationOutputByMonthValue' ] ) )
        admin.logout()
    
    def test_AllTypesParameters( self ):
        admin = active_user("admin","nimda123")
        token = admin.login()
        urls = [ "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/AllTypes/PT60M/date/2018-01-06", \
                 "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/AllTypes/PT60M/month/2018-01", \
                 "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/AllTypes/PT60M/year/2018" ]
        for url in urls:
            response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( response.status_code == 200 or response.status_code == 403 )
            if response.status_code == 403:
                admin.logout()
                return
            data = response.json()
            for packet in data:
                self.assertEqual( packet[ 'AreaName' ], 'Austria' )
                self.assertEqual( packet[ 'ResolutionCode' ], 'PT60M' )
                self.assertEqual( packet[ 'Year' ], 2018 )
                self.assertTrue( packet[ 'ProductionType' ] in prod_types.values() ) 
                if 'ActualGenerationOutputValue' in packet.keys():
                    self.assertEqual( packet[ 'Day' ], 6 )
                    self.assertEqual( packet[ 'Month' ], 1 )
                elif 'ActualGenerationOutputByDayValue' in packet.keys():
                    self.assertEqual( packet[ 'Month' ], 1 )
        admin.logout()
        
    def test_AllTypesPerDay( self ):
        url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Netherlands/AllTypes/PT60M/month/2018-01"
        admin = active_user("admin","nimda123")
        token = admin.login()
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403 )
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
            self.assertTrue( packet[ 'ProductionType' ] in prod_types.values() )
            url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Netherlands/AllTypes/PT60M/date/2018-01-%s" % str( day )
            day_response = requests.get(url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( day_response.status_code == 200 or day_response.status_code == 403)
            if day_response.status_code == 403:
                admin.logout()
                return

            day_data = day_response.json()
            for day_packet in day_data:
                if day_packet[ 'ProductionType' ] == packet[ 'ProductionType' ]:
                    total += float( day_packet[ 'ActualGenerationOutputValue' ] )
                self.assertTrue( day_packet[ 'ProductionType' ] in prod_types.values() )
            self.assertTrue( packet[ 'ProductionType' ] in prod_types.values() )
            self.assertEqual( round( total, 3 ), float( packet[ 'ActualGenerationOutputByDayValue' ] ) )
        admin.logout()
    
    def test_AllTypesPerMonth( self ):
        url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Romania/AllTypes/PT15M/year/2018"
        admin = active_user("admin","nimda123")
        token = admin.login()
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403 )
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
            self.assertTrue( packet[ 'ProductionType' ] in prod_types.values() )
            url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Romania/AllTypes/PT15M/month/2018-%s" % str( month )
            month_response = requests.get(url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( month_response.status_code == 200 or month_response.status_code == 403)
            if month_response.status_code == 403:
                admin.logout()
                return

            month_data = month_response.json()
            for month_packet in month_data:
                if month_packet[ 'ProductionType' ] == packet[ 'ProductionType' ]:
                    total += float( month_packet[ 'ActualGenerationOutputByDayValue' ] )
                self.assertTrue( month_packet[ 'ProductionType' ] in prod_types.values() )
            self.assertTrue( packet[ 'ProductionType' ] in prod_types.values() )
            self.assertEqual( round( total, 3 ), float( packet[ 'ActualGenerationOutputByMonthValue' ] ) )
        admin.logout()

    def test_NowParameters( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/1/PT60M"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403)
        if response.status_code == 403:
            admin.logout()
            return
        data = response.json()
        now = datetime.datetime.now()
        for packet in data:
            self.assertEqual( packet[ 'AreaName' ], 'Austria' )
            self.assertEqual( packet[ 'ProductionType' ], prod_types[ '1' ] )
            self.assertEqual( packet[ 'ResolutionCode' ], 'PT60M' )
            self.assertEqual( packet[ 'Year' ], str(now.year) )
            if 'ActualTotalLoadValue' in packet.keys():
                self.assertEqual( packet[ 'Day' ], str(now.day) )
                self.assertEqual( packet[ 'Month' ], str(now.month) )
            elif 'ActualTotalLoadByDayValue' in packet.keys():
                self.assertEqual( packet[ 'Month' ], str(now.month) )
        admin.logout()

    def test_AllTypesNowParameters( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        url = "http://localhost:8765/energy/api/AggregatedGenerationPerType/Austria/AllTypes/PT60M"
        response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
        self.assertTrue( response.status_code == 200 or response.status_code == 403)
        if response.status_code == 403:
            admin.logout()
            return
        data = response.json()
        now = datetime.datetime.now()
        for packet in data:
            self.assertEqual( packet[ 'AreaName' ], 'Austria' )
            self.assertEqual( packet[ 'ResolutionCode' ], 'PT60M' )
            self.assertEqual( packet[ 'Year' ], str(now.year) )
            self.assertTrue( packet[ 'ProductionType' ] in prod_types.values())
            if 'AggregatedGenerationOutputValue' in packet.keys():
                self.assertEqual( packet[ 'Day' ], str(now.day) )
                self.assertEqual( packet[ 'Month' ], str(now.month) )
            elif 'AggregatedGenerationOutputByDayValue' in packet.keys():
                self.assertEqual( packet[ 'Month' ], str(now.month) )
        admin.logout()

if __name__ == '__main__':
    unittest.main()
