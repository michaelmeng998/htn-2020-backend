# Imports
from flask import Flask, g, jsonify, Response, abort, request
import sqlite3
import os
import sys

# good to have imports
import json
import ast
import re


DATABASE = "./hackers2.db"

# Create app
app = Flask(__name__)


# check if the database exist, if not create the table and insert a few lines of data
# if not os.path.exists(DATABASE):
conn = sqlite3.connect(DATABASE, check_same_thread=False)
# This enables column access by name: row['column_name']
conn.row_factory = sqlite3.Row

'''
need some code here to call a script to create hackers.db if not already created...
'''

'''
after creating hackers.db, can then get the
'''


# helper method to get the database since calls are per thread,
# and everything function is a new thread when called


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db


# helper to close
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# API route for the HOME PAGE :))
@app.route("/")
def start():
    return ('HOME PAGE :)')

# API route for creating the database from JSON file
@app.route("/create_db")
def create_db():
    return ('SUCESFULLY CREATED THE DATABASE!')

# ----------------------USERS ENDPOINTS----------------------

# API route handler to get all users information from database
@app.route("/users", methods=['GET'])
def get_users():
    cur = conn.cursor()
    cur.execute('''
        SELECT company, email, latitude, longitude, name, phone, picture,
        GROUP_CONCAT('{"name":"' || eventName || '"}') events
        FROM users AS u
        LEFT JOIN userEvents AS ue ON u.userID = ue.userID
        LEFT JOIN events AS e ON ue.eventID = e.eventID
        GROUP BY u.userID 
        ''')
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        dictionary = dict(zip(columns[:7], row))
        # for events column
        # create dictionary for events:
        dict_events = []
        event_list = ast.literal_eval(row['events'])
        if len(event_list) == 1:
            dict_events.append(event_list)
            dictionary["events"] = dict_events
        else:
            for event in event_list:
                dict_events.append(event)
            dictionary["events"] = dict_events
        results.append(dictionary)
    return Response(json.dumps(results),  mimetype='application/json', status=200)

# API route handler to get user information with a specific ID
@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    # input validation
    # regex checks for positive integer, need to implement error check where there is question mark at end of <id>
    if re.search('^[0-9]*[1-9][0-9]*$', id) == None:
        abort(400, "'userID' must be positive interger number")
        # return Response("ERROR: 'userID' must be positive interger number", status=400)

    cur = conn.cursor()
    cur.execute('''
        SELECT company, email, latitude, longitude, name, phone, picture,
        GROUP_CONCAT('{"name":"' || eventName || '"}') events
        FROM users AS u 
        LEFT JOIN userEvents AS ue ON u.userID = ue.userID
        LEFT JOIN events AS e ON ue.eventID = e.eventID
        WHERE u.userID = ?
        GROUP BY u.userID 
        ''', [id])
    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        dictionary = dict(zip(columns[:7], row))
        # for events column create dictionary for events:
        dict_events = []
        event_list = ast.literal_eval(row['events'])
        if len(event_list) == 1:
            dict_events.append(event_list)
            dictionary["events"] = dict_events
        else:
            for event in event_list:
                dict_events.append(event)
            dictionary["events"] = dict_events
        results.append(dictionary)
    # there might be easier way to check for [] results before hand, implement as tech debt later on
    if results == []:
        return Response("[], userID does not exist")

    return Response(json.dumps(results),  mimetype='application/json')

# API route handler to get user information within a latitude and longitude range
# input rule, only put in float point numbers, no letters
@app.route("/users/params", methods=['GET'])
def get_user_in_range():

    latitude = request.args.get('lat', None)
    longitude = request.args.get('long', None)
    loc_range = request.args.get('range', None)

    if latitude is None or longitude is None or loc_range is None:
        abort(400, "ERROR: must specify latitude (lat), longitude (long) and range (range)")

    # validation to check for any letters
    if re.search('[a-zA-Z]', latitude) != None or re.search('[a-zA-Z]', longitude) != None or re.search('[a-zA-Z]', loc_range) != None:
        abort(400, "ERROR: latitude (lat), longitude (long) and range (range) must be floating point numbers")

    cur = conn.cursor()
    cur.execute('''
        SELECT company, email, latitude, longitude, name, phone, picture,
        GROUP_CONCAT('{"name":"' || eventName || '"}') events
        FROM users AS u 
        LEFT JOIN userEvents AS ue ON u.userID = ue.userID
        LEFT JOIN events AS e ON ue.eventID = e.eventID
        WHERE ROUND(ABS(u.latitude - ?), 4) <= ABS(?)  AND ROUND(ABS(u.longitude - ?), 4) <= ABS(?)
        GROUP BY u.userID 
        ''', [latitude, loc_range, longitude, loc_range])

    columns = [column[0] for column in cur.description]
    results = []
    for row in cur.fetchall():
        dictionary = dict(zip(columns[:7], row))
        # for events column
        # create dictionary for events:
        dict_events = []
        event_list = ast.literal_eval(row['events'])
        if len(event_list) == 1:
            dict_events.append(event_list)
            dictionary["events"] = dict_events
        else:
            for event in event_list:
                dict_events.append(event)
            dictionary["events"] = dict_events
        results.append(dictionary)

    return Response(json.dumps(results),  mimetype='application/json')

# ----------------------EVENTS ENDPOINTS----------------------


if __name__ == "__main__":
    """
        Use python sqlite3 to create a local database, insert some basic data and then
        display the data using the flask templating.

        http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
    """
    app.run(debug=True)
