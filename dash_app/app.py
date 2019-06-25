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


#  SEPARETE ROUTES FOR EACH CHART WHILE IN DEVELOPMENT

####################################################
    # MAP CHART ROUTE
    # @TODO route for the map chart
# @app.route("/map")
####################################################

####################################################
    # DONUT CHART ROUTE
    # @TODO route for the DONUT chart
# @app.route("/donut")
####################################################

####################################################
    # LINE CHART ROUTE
    # @TODO route for the LINE chart
# @app.route("/line")
####################################################

####################################################
    # DONUT CHART ROUTE
    # @TODO route for the DONUT chart
# @app.route("/bar")
####################################################

if __name__ == "__main__":
    app.run()
