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


@app.route("/columns")
def names():
    """Return Column names from  a random sample   n = 11000 rows from the original dataset."""

    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()
    cols = '''
        SELECT name, sql FROM sqlite_master
        WHERE type='table' AND name = 'jso11k'
    '''

    cur.execute(cols)
    rows = cur.fetchall()
    col_string = rows[0][1]
    pattern = r'`([A-Za-z0-9]*)`'
    column_names = re.findall(pattern, col_string)[:-1]

    return jsonify(column_names)

####################################################
    # COUNTRIES API
@app.route("/countries")
def countries():
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
####################################################
####################################################

#  SEPARETE ROUTES FOR EACH CHART WHILE IN DEVELOPMENT

####################################################
    # MAP CHART ROUTE
    # @TODO route for the map chart
# THE CSS STYLE IS JUST A DEMO
@app.route("/mapChart")
def mapChart():
    """Return the mapChart page."""
    return render_template("mapChart.html")
###################################################

####################################################
    # LINE CHART ROUTE
    # @TODO route for the LINE chart
# THE CSS STYLE IS JUST A DEMO
@app.route("/lineChart")
def lineChart():
    """Return the lineChart page."""
    return render_template("lineChart.html")

####################################################

####################################################
    # LINE CHART ROUTE
    # @TODO route for the donutChart chart
# THE CSS STYLE IS JUST A DEMO
@app.route("/donutChart")
def donutChart():
    """Return the lineChart page."""
    return render_template("donutChart.html")
    
####################################################
####################################################

    # BAR CHART ROUTE
    # @TODO route for the  BAR chart
# THE CSS STYLE IS JUST A DEMO
@app.route("/barChart")
def barChart():
    """Return the barChart page."""
    return render_template("barChart.html")####################################################

if __name__ == "__main__":
    app.run()

####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

# import pandas as pd
# import numpy as np
# from flask import Flask, jsonify, render_template
# import sqlite3
# import re

# app = Flask(__name__)


# @app.route("/")
# def index():
#     """Return the homepage."""
#     return render_template("index.html")


# @app.route("/columns")
# def names():
#     """Return a list of columns from 11000 rows from the original dataset."""

#     conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
#     cur = conn.cursor()
#     cols = '''
#         SELECT name, sql FROM sqlite_master
#         WHERE type='table' AND name = 'jso11k'
#     '''

#     cur.execute(cols)
#     rows = cur.fetchall()
#     col_string = rows[0][1]
#     pattern = r'`([A-Za-z0-9]*)`'
#     column_names = re.findall(pattern, col_string)[:-1]

#     return jsonify(column_names)


# #  SEPARETE ROUTES FOR EACH CHART WHILE IN DEVELOPMENT

# ####################################################
#     # MAP CHART ROUTE
#     # @TODO route for the map chart
# # @app.route("/map")
# ####################################################

# ####################################################
#     # DONUT CHART ROUTE
#     # @TODO route for the DONUT chart
# # @app.route("/donut")
# ####################################################

# ####################################################
#     # LINE CHART ROUTE
#     # @TODO route for the LINE chart
# # @app.route("/line")
# ####################################################

# ####################################################
#     # DONUT CHART ROUTE
#     # @TODO route for the DONUT chart
# # @app.route("/bar")
# ####################################################

# if __name__ == "__main__":
#     app.run()
