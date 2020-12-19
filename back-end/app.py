from endpoints.global_data import app
from endpoints import ActualTotalLoad
from endpoints import AggregatedGenerationPerType
from endpoints import DayAheadTotalLoadForecast
from endpoints import ActualvsForecast
from endpoints import users
from endpoints import admin

from flask import redirect, url_for

@app.route("/")
def base_url():
    return redirect( url_for('home') )

@app.route("/energy/api")
def home():
    return "OK", 200

if __name__ == '__main__':
    app.run(host="localhost",port=8765 )

