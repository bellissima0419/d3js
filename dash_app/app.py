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

@app.route("/api/impsyn")
def impsyn():
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

# @app.route("/api/socialmedia")
# def socialmedia():

#     query = "SELECT SocialMedia, COUNT(SocialMedia) FROM jso11k WHERE SocialMedia IS NOT NULL GROUP BY SocialMedia"
#     response = get_data(query)
#     return jsonify(response)




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


@app.route("/api/employment")
def employment():

    query = "SELECT Employment, COUNT(Employment) FROM jso11k WHERE Employment IS NOT NULL GROUP BY Employment"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/careersat")
def careersat():

    query = "SELECT CareerSat, COUNT(CareerSat) FROM jso11k WHERE CareerSat IS NOT NULL GROUP BY CareerSat"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/jobsat")
def jobsat():

    query = "SELECT JobSat, COUNT(JobSat) FROM jso11k WHERE JobSat IS NOT NULL GROUP BY JobSat"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/mgridiot")
def mgridiot():

    query = "SELECT MgrIdiot, COUNT(MgrIdiot) FROM jso11k WHERE MgrIdiot IS NOT NULL GROUP BY MgrIdiot"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/mgrmoney")
def mgrmoney():

    query = "SELECT MgrMoney, COUNT(MgrMoney) FROM jso11k WHERE MgrMoney IS NOT NULL GROUP BY MgrMoney"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/mgrwant")
def mgrwant():

    query = "SELECT MgrWant, COUNT(MgrWant) FROM jso11k WHERE MgrWant IS NOT NULL GROUP BY MgrWant"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/jobseek")
def jobseek():

    query = "SELECT JobSeek, COUNT(JobSeek) FROM jso11k WHERE JobSeek IS NOT NULL GROUP BY JobSeek"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/soaccount")
def soaccount():

    query = "SELECT SOAccount, COUNT(SOAccount) FROM jso11k WHERE SOAccount IS NOT NULL GROUP BY SOAccount"
    response = get_data(query)
    return jsonify(response)
@app.route("/api/fizzbuzz")
def fizzbuzz():

    query = "SELECT FizzBuzz, COUNT(FizzBuzz) FROM jso11k WHERE FizzBuzz IS NOT NULL GROUP BY FizzBuzz"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/workplan")
def workplan():

    query = "SELECT WorkPlan, COUNT(WorkPlan) FROM jso11k WHERE WorkPlan IS NOT NULL GROUP BY WorkPlan"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/workloc")
def workloc():

    query = "SELECT WorkLoc, COUNT(WorkLoc) FROM jso11k WHERE WorkLoc IS NOT NULL GROUP BY WorkLoc"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/blockchainis")
def blockchainis():

    query = "SELECT BlockChainIs, COUNT(BlockChainIs) FROM jso11k WHERE BlockChainIs IS NOT NULL GROUP BY BlockChainIs"
    response = get_data(query)
    return jsonify(response)

@app.route("/api/opsys")
def opsys():

    query = "SELECT OpSys, COUNT(OpSys) FROM jso11k WHERE OpSys IS NOT NULL GROUP BY OpSys"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/betterlife")
def betterlife():

    query = "SELECT BetterLife, COUNT(BetterLife) FROM jso11k WHERE BetterLife IS NOT NULL GROUP BY BetterLife"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/trans")
def trans():

    query = "SELECT Trans, COUNT(Trans) FROM jso11k WHERE Trans IS NOT NULL GROUP BY Trans"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/offon")
def offon():

    query = "SELECT OffOn, COUNT(OffOn) FROM jso11k WHERE OffOn IS NOT NULL GROUP BY OffOn"
    response = get_data(query)
    return jsonify(response)


@app.route("/api/undergradmajor")
def undergradmajor():

    query = "SELECT UndergradMajor, COUNT(UndergradMajor) FROM jso11k WHERE UndergradMajor IS NOT NULL GROUP BY UndergradMajor"
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
