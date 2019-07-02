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

    query = "SELECT ImpSyn, COUNT(ImpSyn) FROM jso11k WHERE ImpSyn IS NOT NULL GROUP BY ImpSyn"
    response = get_data(query)

    return jsonify(response)


@app.route("/api/dependents")
def dependents():
    "Dependents"

    query = "SELECT Dependents, COUNT(Dependents) FROM jso11k WHERE Dependents IS NOT NULL GROUP BY Dependents"
    response = get_data(query)

    return jsonify(response)

@app.route("/api/gender")
def gender():
    "gender"

    query = "SELECT Gender, COUNT(Gender) FROM jso11k WHERE Gender IS NOT NULL GROUP BY Gender"
    response = get_data(query)

    return jsonify(response)

@app.route("/api/extraversion")
def extraversion():
    "extraversion"

    query = "SELECT Extraversion, COUNT(Extraversion) FROM jso11k WHERE Extraversion IS NOT NULL GROUP BY Extraversion"
    response = get_data(query)

    return jsonify(response)

@app.route("/api/sojobs")
def sojobs():

    query = "SELECT SOJobs, COUNT(SOJobs) FROM jso11k WHERE SOJobs IS NOT NULL GROUP BY SOJobs"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/socialmedia")
def socialmedia():

    query = "SELECT SocialMedia, COUNT(SocialMedia) FROM jso11k WHERE SocialMedia IS NOT NULL GROUP BY SocialMedia"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/edlevel")
def edlevel():

    query = "SELECT EdLevel, COUNT(EdLevel) FROM jso11k WHERE EdLevel IS NOT NULL GROUP BY EdLevel"
    response = get_data(query)
    return jsonify(response)




# ===============================
# ===============================
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
