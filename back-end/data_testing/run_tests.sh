#!/bin/sh
echo "Running Tests for ActualTotalLoad"
python3 ActualTotalLoad_tests.py
echo "Running Tests for AggregatedGenerationPerType"
python3 AggregatedGenerationPerType_tests.py
echo "Running Tests for DayAheadTotalLoadForecast"
python3 DayAheadTotalLoadForecast_tests.py
echo "Running Tests for ActualvsForecast"
python3 ActualvsForecast_tests.py
