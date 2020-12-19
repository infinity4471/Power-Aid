import unittest
import mysql.connector
import requests
import json

energy = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="energy"
)

mycursor = energy.cursor()

sql_query = "DELETE FROM users WHERE username = 'tester1'"
mycursor.execute(sql_query)

sql_query = "DELETE FROM ActualTotalLoad WHERE Id = 10000000"
mycursor.execute(sql_query)
