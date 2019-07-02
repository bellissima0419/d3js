# FLASK_APP=dash_app/app.py flask run
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/api/countries")
def country_api():
    """
     Return a list of number of survey respondents by country
    """
    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()

    query_string = '''
        SELECT Country, count(country) FROM jso11k
        GROUP BY Country
        ORDER BY COUNT(Country) DESC
    '''

    cur.execute(query_string)
    rows = cur.fetchall()

    country_data = []

    for row in rows:
        tempDict = {}
        tempDict["country"] = row[0]
        tempDict["respondentCount"] = int(row[1])
        # tempDict[row[0]] = int(row[1])
        country_data.append(tempDict)

    return jsonify(country_data)



def get_data(query_string):
    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()
    cur.execute(query_string)
    rows = cur.fetchall()
    data = []
    for row in rows:
        temp_dict = {}
        temp_dict[row[0]] = row[1]
        data.append(temp_dict)
    return data

@app.route("/api/imp_syn")
def imp_syn_api():
    "Impostor Syndrome"

    query = "select ImpSyn, count(ImpSyn) from jso11k group by ImpSyn"
    
    imp_syn = get_data(query)

    return jsonify(imp_syn)


@app.route("/impSyn")
def impSyn():
    
    return render_template("impSyn.html")

@app.route("/countries")
def countries():
    """Return count of respondents per countries page."""
    return render_template("countries.html")

@app.route("/languages")
def languages():
    """Return the language popularity in males page."""
    return render_template("languages.html")


if __name__ == "__main__":
    app.run()
# ===============================
