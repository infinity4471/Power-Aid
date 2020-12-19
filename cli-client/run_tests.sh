#!/bin/sh

echo "Running functional test for ActualTotalLoad"
python3 ActualTotalLoad_test.py

echo "Running functional test for AggregatedGenerationPerType"
python3 AggregatedGenerationPerType_test.py

echo "Running functional test for ActualvsForecast"
python3 ActualvsForecast_test.py

echo "Running functional test for DayAheadTotalLoadForecast"
python3 DayAheadTotalLoadForecast_test.py

cd db
echo "Running connectivity test"
python3 connectivity_testing.py

cd ..
cd usr
echo "Running login tests"
python3 login_tests.py
echo "Running logout tests"
python3 logout_tests.py
