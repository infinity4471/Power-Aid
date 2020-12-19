#!/bin/sh
echo "Running new user tests"
python3 newUser_testing.py
echo "Running modify user tests"
python3 modifyUser_testing.py
echo "Running upload tests"
python3 uploadFile_testing.py
echo "Running quota tests"
python3 quota_testing.py

echo "Cleanup"
python3 delete_insertedData.py 


