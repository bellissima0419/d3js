# FLASK_APP=dash_app/app.py flask run
import re
import sqlite3
from flask import Flask, jsonify, render_template
import numpy as np
import pandas as pd

# sort function for dictionaries
# howtosort = "sorted(country_data[1:], key = lambda i: i['country'],reverse=False)"


app = Flask(__name__)


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/map")
def map():
    return render_template("perCapitaMap.html")


@app.route("/perCapitaMap")
def perCapitaMap():
    return render_template("perCapitaMap.html")


@app.route("/donuts")
def donuts():
    return render_template("donuts.html")


@app.route("/scatter")
def scatter():
    return render_template("scatter.html")


@app.route("/line")
def line():
    return render_template("line.html")


@app.route("/apiroutes")
def apiroutes():
    return render_template("apiroutes.html")


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


@app.route("/api/stats")
def stats():
    '''
     Return list with count of respondents by country
     with lat and longs
    '''

    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()

    coordinates_query = '''
        SELECT * from country_coordinates
    '''
    cur.execute(coordinates_query)
    coordinates_rows = cur.fetchall()

    coordinates = []

    for row in coordinates_rows:
        tempDict = {}
        tempDict["code"] = row[0]
        tempDict["location"] = [row[1], row[2]]
        tempDict["latitude"] = row[1]
        tempDict["longitude"] = row[2]
        tempDict["name"] = row[3]
        coordinates.append(tempDict)

    country_query = '''
        SELECT Country, count(country) FROM jso11k
        GROUP BY Country
        ORDER BY COUNT(Country) DESC
    '''

    cur.execute(country_query)
    country_rows = cur.fetchall()

    countries = []

    for row in country_rows:
        tempDict = {}
        tempDict["country"] = (row[0])
        tempDict["respondentCount"] = int(row[1]*8)
        # tempDict[row[0]] = int(row[1])
        countries.append(tempDict)

    for i in range(len(countries)):
        if countries[i]['country'] == 'Russian Federation':
            countries[i]['country'] = 'Russia'
        if countries[i]['country'] == 'Czech Republic':
            countries[i]['country'] = 'Czech Republic'
        if countries[i]['country'] == 'Viet Nam':
            countries[i]['country'] = 'Vietnam'
        if countries[i]['country'] == 'Venezuela, Bolivarian Republic of...':
            countries[i]['country'] = 'Venezuela'
        if countries[i]['country'] == 'Republic of Korea':
            countries[i]['country'] = 'North Korea'
        if countries[i]['country'] == 'Syrian Arab Republic':
            countries[i]['country'] = 'Syria'
        if countries[i]['country'] == "Lao People's Democratic Republic":
            countries[i]['country'] = 'Laos'
        if countries[i]['country'] == 'The former Yugoslav Republic of Macedonia':
            countries[i]['country'] = 'Macedonia [FYROM]'
        if countries[i]['country'] == 'Republic of Moldova':
            countries[i]['country'] = 'Moldova'
        if countries[i]['country'] == 'United Republic of Tanzania':
            countries[i]['country'] = 'Tanzania'
        if countries[i]['country'] == 'Democratic Republic of the Congo':
            countries[i]['country'] = 'Congo [DRC]'

    for i in range(len(coordinates)):
        for j in range(len(countries)):
            if coordinates[i]['name'] in countries[j].values():
                countries[j]['code'] = str(coordinates[i]['code'])
                countries[j]['latitude'] = float(coordinates[i]['latitude'])
                countries[j]['longitude'] = float(coordinates[i]['longitude'])
                countries[j]['location'] = (coordinates[i]['location'])

    stats_query = '''
        SELECT * FROM country_stats
    '''

    cur.execute(stats_query)
    stats_rows = cur.fetchall()

    stats = []

    for row in stats_rows:
        tempDict = {}
        tempDict["country"] = row[0]
        tempDict["population"] = row[1]
        stats.append(tempDict)

    for i in range(len(stats)):
        for j in range(len(countries)):
            if stats[i]['country'] in countries[j].values():
                countries[j]['population'] = stats[i]['population']

    for i in range(len(countries)):
        try:
            countries[i]['devsPerMill'] = float(
                countries[i]['respondentCount']) / float((countries[i]['population']/1000000))
            countries[i]['devsPerMill'] = round(countries[i]['devsPerMill'], 2)
        except:
            continue

    countries = [item for item in countries if item['country'] is not None]

    return jsonify(countries)


def get_data(query_string):
    # q_string = f"SELECT Sexuality, COUNT(Sexuality) FROM jso11k WHERE Sexuality IS NOT NULL GROUP BY Sexuality"
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


@app.route("/api/sexuality")
def sexuality():

    query = "SELECT Sexuality, COUNT(Sexuality) FROM jso11k WHERE Sexuality IS NOT NULL GROUP BY Sexuality"
    response = get_data(query)
    return jsonify(response)


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


if __name__ == "__main__":
    app.run()
# ===============================
