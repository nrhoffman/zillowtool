import configparser
import connection
import csvreader
import pandas as pd
import sys
from flask import Flask, jsonify
from flask_cors import CORS

#Set up Flask:
app = Flask(__name__)
#Set up Flask to bypass CORS:
cors = CORS(app)

#Read the config file
config = configparser.ConfigParser()
config.read('./backend/config/config.cfg')

#Setup connection with Postgres database
psql = connection.Connection(config, config["VALUES"]["CreateTables"])

# csvreader.csvreader(config, psql)

#Create the get-states API POST endpoint:
@app.route("/getstates", methods=["GET"])
def getStates():
    data = psql.getstates()
    return jsonify(data)

@app.route("/getcities/<state>", methods=["GET"])
def getCities(state):
    data = psql.getcities(state)
    return jsonify(data)

@app.route("/getdata/<state>/<city>", methods=["GET"])
def getData(state, city):
    data = psql.getdata(state, city)
    return data.to_json(orient="records")

if __name__ == "__main__": 
   app.run(debug=True)