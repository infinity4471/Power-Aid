import unittest
import requests
import json

from active_user import *

class ActualvsForecast( unittest.TestCase ):
    def test_parameters( self ):
        admin = active_user( "admin", "nimda123" )
        token = admin.login()
        urls = [ "http://localhost:8765/energy/api/ActualvsForecast/Slovakia/PT15M/date/2018-01-01", \
                 "http://localhost:8765/energy/api/ActualvsForecast/Slovakia/PT15M/month/2018-01", \
                 "http://localhost:8765/energy/api/ActualvsForecast/Slovakia/PT15M/year/2018" ]
        
        for url in urls:
            response = requests.get( url, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( response.status_code == 200 or response.status_code == 403 )
            if response.status_code == 403:
                admin.logout()
                return
            data = response.json()
            for packet in data:
                self.assertEqual( packet[ 'AreaName' ], 'Slovakia' )
                self.assertEqual( packet[ 'ResolutionCode' ], 'PT15M' )
                self.assertEqual( packet[ 'Year' ], 2018 )
                if 'ActualTotalLoadValue' and 'DayAheadTotalLoadForecastValue' in packet.keys():
                    self.assertEqual( packet[ 'Day' ], 1 )
                    self.assertEqual( packet[ 'Month' ], 1 )
                elif 'ActualTotalLoadByDayValue' and 'DayAheadTotalLoadForecastByDayValue' in packet.keys():
                    self.assertEqual( packet[ 'Month' ], 1 )
        admin.logout()

    def test_ValuesPerDay( self ):
        url = "http://localhost:8765/energy/api/ActualvsForecast/Slovakia/PT15M/month/2018-01"
        admin = active_user( "admin", "nimda123" )
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
            actual_total, forecast_total = 0, 0
            url_actual = "http://localhost:8765/energy/api/ActualTotalLoad/Slovakia/PT15M/date/2018-01-%s" % str( day )
            url_forecast = "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Slovakia/PT15M/date/2018-01-%s" % str( day )
            actual_day_response = requests.get( url_actual, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( actual_day_response.status_code == 200 or actual_day_response.status_code == 403)
            if actual_day_response.status_code == 403:
                admin.logout()
                return
            forecast_day_response = requests.get( url_forecast, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( forecast_day_response.status_code == 200 or forecast_day_response.status_code == 403)
            if forecast_day_response.status_code == 403:
                admin.logout()
                return
            
            actual_day_data = actual_day_response.json()
            forecast_day_data = forecast_day_response.json()
            for day_packet in actual_day_data:
                if day_packet[ 'Month' ] == packet[ 'Month' ] and day_packet[ 'Year' ] == packet[ 'Year' ]:
                    actual_total += float( day_packet[ 'ActualTotalLoadValue' ] )
            for day_packet in forecast_day_data:
                if day_packet[ 'Month' ] == packet[ 'Month' ] and day_packet[ 'Year' ] == packet[ 'Year' ]:
                    forecast_total += float( day_packet[ 'DayAheadTotalLoadForecastValue' ] )

            self.assertEqual( round( actual_total, 3 ), float( packet[ 'ActualTotalLoadByDayValue' ] ) )
            self.assertEqual( round( forecast_total, 3 ), float( packet[ 'DayAheadTotalLoadForecastByDayValue' ] ) )
        admin.logout()

    def test_ValuesPerMonth( self ):
        url = "http://localhost:8765/energy/api/ActualvsForecast/Slovakia/PT15M/year/2018"
        admin = active_user( "admin", "nimda123" )
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
            actual_total, forecast_total = 0, 0
            url_actual = "http://localhost:8765/energy/api/ActualTotalLoad/Slovakia/PT15M/month/2018-%s" % str( month )
            url_forecast = "http://localhost:8765/energy/api/DayAheadTotalLoadForecast/Slovakia/PT15M/month/2018-%s" % str( month )
            actual_month_response = requests.get( url_actual, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( actual_month_response.status_code == 200 or actual_month_response.status_code == 403)
            if actual_month_response.status_code == 403:
                admin.logout()
                return
            forecast_month_response = requests.get( url_forecast, headers = { "X-OBSERVATORY-AUTH": token } )
            self.assertTrue( forecast_month_response.status_code == 200 or forecast_month_response.status_code == 403)
            if forecast_month_response.status_code == 403:
                admin.logout()
                return

            actual_month_data = actual_month_response.json()
            forecast_month_data = forecast_month_response.json()
            for month_packet in actual_month_data:
                if month_packet[ 'Year' ] == packet[ 'Year' ]:
                    actual_total += float( month_packet[ 'ActualTotalLoadByDayValue' ] )
            for month_packet in forecast_month_data:
                if month_packet[ 'Year' ] == packet[ 'Year' ]:
                    forecast_total += float( month_packet[ 'DayAheadTotalLoadForecastByDayValue' ] )
            self.assertEqual( round( actual_total, 3 ), float( packet[ 'ActualTotalLoadByMonthValue' ] ) )
            self.assertEqual( round( forecast_total, 3 ), float( packet[ 'DayAheadTotalLoadForecastByMonthValue' ] ) )
        admin.logout()

    def test_NowParameters( self ):
        admin = active_user( "admin","nimda123")
        token = admin.login()
        url = "http://localhost:8765/energy/api/ActualvsForecast/Slovakia/PT15M"
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
            if 'ActualTotalLoadValue' and 'DayAheadTotalLoadForecastValue' in packet.keys():
                self.assertEqual( packet[ 'Day' ], str(now.day) )
                self.assertEqual( packet[ 'Month' ], str(now.month) )
            elif 'ActualTotalLoadByDayValue' and 'DayAheadTotalLoadForecastByDayValue' in packet.keys():
                self.assertEqual( packet[ 'Month' ], str(now.month) )
        admin.logout()
if __name__ == '__main__':
    unittest.main()
