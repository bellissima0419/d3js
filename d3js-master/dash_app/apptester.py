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

@app.route("/api/columns")
def names():
    """Return Column names from  a random sample  n = 11000 rows from the original dataset."""

    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(jso11k)")
    rows = cur.fetchall()
    column_names = [i[1] for i in rows]
    return jsonify(column_names)

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


@app.route("/api/genders")
def api_genders():
    """
     Return a list of respondents count and percentages out of those who answered the Gender question
    """
    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()

    genders_query = "SELECT Gender, COUNT(Gender) FROM jso11k GROUP BY Gender"

    cur.execute(genders_query)
    rows = cur.fetchall()

    gender_data = []
    for row in rows:
        temp_dict = {}
        temp_dict["gender"] = row[0]
        temp_dict["gender_count"] = row[1]
        gender_data.append(temp_dict)

    return jsonify(gender_data)

def get_tech_tools(qery_obj):

    conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
    cur = conn.cursor()
    tech_tools_by_gender = []

    for key, value in qery_obj.items():

        cur.execute(value)
        rows = cur.fetchall()

         tech_tool_freq = {}
        
        for row in rows:
            languages = row[0].split(';')   
            for item in languages:
                if item in tech_tool_freq:
                    tech_tool_freq[item] += int(row[1])
                else:
                    tech_tool_freq[item] = int(row[1])
                
        tech_tools_by_gender.append({key: tech_tool_freq})
    
    return jsonify(tech_tools_by_gender)

@app.route("/api/languages")
def api_languages():
    """
     Return a list of language use frequency by gender
    """
    queries = {
            "man": '''
                SELECT LanguageWorkedWith, COUNT(LanguageWorkedWith)
                FROM jso11k WHERE Gender = 'Man' and LanguageWorkedWith > 0
                GROUP BY LanguageWorkedWith ORDER BY COUNT(LanguageWorkedWith) DESC
            ''',
            "woman": '''
                SELECT LanguageWorkedWith, COUNT(LanguageWorkedWith)
                FROM jso11k
                WHERE Gender = 'Woman' and LanguageWorkedWith > 0
                GROUP BY LanguageWorkedWith ORDER BY COUNT(LanguageWorkedWith) DESC
            ''',
            "other": '''
                SELECT LanguageWorkedWith, COUNT(LanguageWorkedWith)
                FROM jso11k
                WHERE Gender NOT IN ('Man', 'Woman') and LanguageWorkedWith > 0
                GROUP BY LanguageWorkedWith ORDER BY COUNT(LanguageWorkedWith) DESC
            ''',
                "all_genders": '''
                SELECT LanguageWorkedWith, COUNT(LanguageWorkedWith)
                FROM jso11k
                WHERE LanguageWorkedWith > 0
                GROUP BY LanguageWorkedWith ORDER BY COUNT(LanguageWorkedWith) DESC
            '''
        }
    return get_tech_tools(queries)

@app.route("/api/dbgen")
def api_dbgen():
    """
     Return a list of db's use frequency by gender
    """

    queries = {
            "man": '''
                SELECT DatabaseWorkedWith, COUNT(DatabaseWorkedWith)
                FROM jso11k WHERE Gender = 'Man' and DatabaseWorkedWith > 0
                GROUP BY DatabaseWorkedWith ORDER BY COUNT(DatabaseWorkedWith) DESC
            ''',
            "woman": '''
                SELECT DatabaseWorkedWith, COUNT(DatabaseWorkedWith)
                FROM jso11k
                WHERE Gender = 'Woman' and DatabaseWorkedWith > 0
                GROUP BY DatabaseWorkedWith ORDER BY COUNT(DatabaseWorkedWith) DESC
            ''',
            "other": '''
                SELECT DatabaseWorkedWith, COUNT(DatabaseWorkedWith)
                FROM jso11k
                WHERE Gender NOT IN ('Man', 'Woman') and DatabaseWorkedWith > 0
                GROUP BY DatabaseWorkedWith ORDER BY COUNT(DatabaseWorkedWith) DESC
            '''
        }
    return get_tech_tools(queries)

@app.route("/api/miscgen")
def misc_tech_gender():
    """
     Return a list of MiscTech use frequency by gender
    """

    queries = {
            "man": '''
                SELECT MiscTechWorkedWith, COUNT(MiscTechWorkedWith)
                FROM jso11k WHERE Gender = 'Man' and MiscTechWorkedWith > 0
                GROUP BY MiscTechWorkedWith ORDER BY COUNT(MiscTechWorkedWith) DESC
            ''',
            "woman": '''
                SELECT MiscTechWorkedWith, COUNT(MiscTechWorkedWith)
                FROM jso11k
                WHERE Gender = 'Woman' and MiscTechWorkedWith > 0
                GROUP BY MiscTechWorkedWith ORDER BY COUNT(MiscTechWorkedWith) DESC
            ''',
            "other": '''
                SELECT MiscTechWorkedWith, COUNT(MiscTechWorkedWith)
                FROM jso11k
                WHERE Gender NOT IN ('Man', 'Woman') and MiscTechWorkedWith > 0
                GROUP BY MiscTechWorkedWith ORDER BY COUNT(MiscTechWorkedWith) DESC
            '''
        }

    return get_tech_tools(queries)

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



# f"SELECT {db_col}, COUNT({db_col}) FROM jso11k WHERE Gender = {gender} and {db_col} > 0 GROUP BY {db_col} ORDER BY COUNT({Databasedb_colWorkedWith}) DESC"


# ####################################################
# @app.route("/mapChart")
# def mapChart():
#     """Return the mapChart page."""
#     return render_template("mapChart.html")

# @app.route("/lineChart")
# def lineChart():
#     """Return the lineChart page."""
#     return render_template("lineChart.html")


# @app.route("/donut")
# def donut():
#     """Return the lineChart page."""
#     return render_template("donut.html")

# @app.route("/donut2")
# def donut2():
#     """Return the lineChart page."""
#     return render_template("donut2.html")

# @app.route("/barChart")
# def barChart():
#     """Return the barChart page."""
#     return render_template("barChart.html")




####################################################
    # def CountFrequency(my_list): 
    # # Creating an empty dictionary
      
    # freq = {} 
    # for item in my_list: 
    #     if (item in freq): 
    #         freq[item] += 1
    #     else: 
    #         freq[item] = 1
  
    # for key, value in freq.items(): 
    #     print ("% d : % d"%(key, value)) 


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



# f"SELECT {db_col}, COUNT({db_col}) FROM jso11k WHERE Gender = {gender} and {db_col} > 0 GROUP BY {db_col} ORDER BY COUNT({db_col}) DESC"

# def get_tech_tools(db_col):

#     conn = sqlite3.connect("dash_app/db/js_overload.sqlite")
#     cur = conn.cursor()

#     tech_tools_by_gender = []
#     query_obj = {}
#     genders = ['Man', 'Woman'] 

#     for gender in genders:
#         query_obj[gender] = (f"SELECT {str(db_col)}, COUNT({str(db_col)}) FROM jso11k " f"WHERE Gender = {gender} and {str(db_col)} > 0 GROUP BY {str(db_col)} ORDER "
#         f"BY COUNT({str(db_col)}) DESC")


#     for key, value in qery_obj.items():

#         cur.execute(value)
#         rows = cur.fetchall()

#         tech_tool_freq = {}
        
#         for row in rows:
#             languages = row[0].split(';')   
#             for item in languages:
#                 if item in tech_tool_freq:
#                     tech_tool_freq[item] += int(row[1])
#                 else:
#                     tech_tool_freq[item] = int(row[1])
                
#         tech_tools_by_gender.append({key: tech_tool_freq})
    
#     return jsonify(tech_tools_by_gender)