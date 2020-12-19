#!/bin/sh
cd admin_testing
echo "Running admin tests"
sh run_tests.sh

cd ..
cd user_testing
echo "Running user tests"
sh run_tests.sh

cd ..
cd data_testing
echo "Running data tests"
sh run_tests.sh

cd ..
