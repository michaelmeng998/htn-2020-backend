# Imports
from flask import Flask, g, jsonify, Response, abort, request
import sqlite3
import os
import sys

# good to have imports
import json
import ast
import re


DATABASE = "./hackers.db"

app = Flask(__name__)

conn = sqlite3.connect(DATABASE, check_same_thread=False)
conn.row_factory = sqlite3.Row

# ----------------------USEFUL ENDPOINTS----------------------


# API ROUTE for the HOME PAGE
@app.route("/")
def start():
    return ('HOME PAGE :)')


# API ROUTE for creating database tables from JSON file data.json
@app.route("/create_db")
def create_db():
    database = json.load(open('data.json'))
    c = conn.cursor()

    # create db table for users
    c.execute('''
    CREATE TABLE IF NOT EXISTS [users] (
        [userID] INTEGER PRIMARY KEY,
        [company] TEXT NOT NULL,
        [email] TEXT NOT NULL,
        [latitude] REAL NOT NULL,
        [longitude] REAL NOT NULL,
        [name] TEXT NOT NULL,
        [phone] TEXT NOT NULL,
        [picture] TEXT NOT NULL
    );''')

    # create db table for events
    c.execute('''
    CREATE TABLE IF NOT EXISTS [events] (
        [eventID] INTEGER PRIMARY KEY,
        [eventName] TEXT NOT NULL UNIQUE
    );''')

    # create db table for user to event mappings
    c.execute('''
    CREATE TABLE IF NOT EXISTS [userEvents] (
        [eventID] INTEGER NOT NULL,
        [userID] INTEGER  NOT NULL,
        UNIQUE (eventID, userID)
    );''')

    conn.commit()

    # query for users table
    query_insert_users = "INSERT OR IGNORE INTO users (company, email, latitude, longitude, name, phone, picture) VALUES (?,?,?,?,?,?,?)"

    # query for events table
    query_insert_events = "INSERT OR IGNORE INTO events (eventName) VALUES (?)"
    # query_events = "INSERT INTO events (eventName) VALUES ('test event')"

    # query for userID
    query_userID = "SELECT userID FROM users WHERE name = ?"

    # query for eventID
    query_eventID = "SELECT eventID FROM events WHERE eventName = ?"

    # query for mapping
    query_mapping = "INSERT OR IGNORE INTO userEvents (eventID, userID) VALUES (?,?)"

    columns = ['company', 'email', 'latitude',
               'longitude', 'name', 'phone', 'picture']

    for data in database:
        # insert into users table
        keys = tuple(data[c] for c in columns)
        cur = conn.cursor()
        cur.execute(query_insert_users, keys)

        # insert into events table
        for event in data["events"]:
            cur.execute(query_insert_events, (event["name"],))

            # for every event, need to link userID with the eventID and store into userEvents table
            # need to get userID with a query, then store with corresponding eventID
            temp1 = cur.execute(query_userID, (data["name"],))
            userID, = temp1.fetchone()
            temp2 = cur.execute(query_eventID, (event["name"],))
            eventID, = (temp2.fetchone())
            cur.execute(query_mapping, (eventID, userID))

    conn.commit()
    return ('SUCESFULLY CREATED THE DATABASE TABLES!')


# API ROUTE for dropping all hacker database tables
@app.route("/drop_db")
def drop_db():
    c = conn.cursor()

    # drop users table
    c.execute('''
    DROP TABLE IF EXISTS users;''')

    # drop events table
    c.execute('''
    DROP TABLE IF EXISTS events;''')

    # drop userEvents table
    c.execute('''
    DROP TABLE IF EXISTS userEvents;''')

    return ("SUCESFULLY DROPPED DATABASE TABLES!")

# ----------------------USERS ENDPOINTS----------------------


# API ROUTE HANDLER to GET all users information from database
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
        # for events column, create dictionary for events:
        dict_events = []
        event_list = ast.literal_eval(row['events'])
        # edge case: handling case where user is only attending 1 event
        if len(event_list) == 1:
            dict_events.append(event_list)
            dictionary["events"] = dict_events
        else:
            for event in event_list:
                dict_events.append(event)
            dictionary["events"] = dict_events
        results.append(dictionary)
    return Response(json.dumps(results),  mimetype='application/json', status=200)


# API ROUTE HANDLER to GET user information with a specific ID
@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    # input validation
    # regex checks if id is a positive integer number
    if re.search('^[0-9]*[1-9][0-9]*$', id) == None:
        abort(400, "ERROR: 'userID' must be positive interger number")

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

    all_rows = cur.fetchall()
    if all_rows == []:
        return Response('[]', status=200)

    columns = [column[0] for column in cur.description]
    for row in all_rows:
        user_dict = dict(zip(columns[:7], row))
        # for events column, create user_dict for events:
        dict_events = []
        event_list = ast.literal_eval(row['events'])
        if len(event_list) == 1:
            dict_events.append(event_list)
            user_dict["events"] = dict_events
        else:
            for event in event_list:
                dict_events.append(event)
            user_dict["events"] = dict_events
    return Response(json.dumps(user_dict),  mimetype='application/json', status=200)


# API ROUTE HANDLER to GET user information within a latitude and longitude range
@app.route("/users/params", methods=['GET'])
def get_user_in_range():

    latitude = request.args.get('lat', None)
    longitude = request.args.get('long', None)
    loc_range = request.args.get('range', None)

    # validation to check if latitude, longitude, and range are all passed in
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
        # for events column, create dictionary for events:
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

# ----------------------EVENTS ENDPOINTS----------------------

# API ROUTE HANDLER to GET information for a specific event
@app.route("/events/<id>", methods=['GET'])
def get_event(id):
    # input validation
    # regex checks if id is a positive integer number
    if re.search('^[0-9]*[1-9][0-9]*$', id) == None:
        abort(400, "ERROR: 'eventID' must be positive interger number")

    cur = conn.cursor()
    cur.execute('''
        SELECT e.eventID, e.eventName, u.name, u.company, u.email, u.latitude, u.longitude, u.phone, u.picture
        FROM events AS e
        JOIN userEvents AS ue ON e.eventID = ue.eventID
        JOIN users AS u ON ue.userID = u.userID
        WHERE e.eventID = ?
        ''', [id])

    # check if query returned nothing, means eventID does not exist
    all_rows = cur.fetchall()
    if all_rows == []:
        return Response("[]", status=200)

    dictionary = {}
    dict_users = []

    columns = [column[0] for column in cur.description]
    dictionary["eventName"] = all_rows[0][1]
    dictionary["eventID"] = id

    for row in all_rows:
        # for every row, need to extract user objects in dict form, and append to a list that will be under "attendees" key in dictionary
        row_slice = []
        for i in range(2, 9):
            row_slice.append(row[i])
        user_dict = dict(zip(columns[2:], row_slice))
        dict_users.append(user_dict)

    dictionary["attendees"] = dict_users
    return Response(json.dumps(dictionary),  mimetype='application/json', status=200)

# API ROUTE HANDLER to POST attendees to an event
@app.route("/events/<id>/attendees", methods=['POST'])
def post_attendee(id):
    # input validation
    # regex checks if id is a positive integer
    if re.search('^[0-9]*[1-9][0-9]*$', id) == None:
        abort(400, "ERROR: 'eventID' must be positive interger number")

    cur = conn.cursor()

    # catch case where eventID does not exist
    cur.execute('''
        SELECT * from userEvents WHERE eventID = ?
    ''', [id])
    fetch = cur.fetchall()
    if fetch == []:
        return Response("eventID does not exist", status=200)

    # first need to validate the request JSON body
    userID = request.get_json()

    if 'user_id' not in userID or len(userID) > 1:
        abort(
            400, "ERROR: request body must contain single userID with key named 'user_id'")

    if re.search('^[0-9]*[1-9][0-9]*$', userID['user_id']) == None:
        abort(400, "ERROR: 'user_id' must be positive interger number")

    # catch case where userID does not exist
    cur.execute('''
        SELECT * from users where userID = ?
    ''', [userID['user_id']])
    fetch = cur.fetchall()
    if fetch == []:
        return Response("userID does not exist", status=200)

    try:
        cur.execute('''
            INSERT into userEvents (eventID, userID) VALUES (?,?)
        ''', [id, userID["user_id"]])
    except sqlite3.IntegrityError:
        return Response("IntegrityError: user is already attending event", status=200)

    conn.commit()
    return Response("User has been sucesfully added to event :)", status=200)


if __name__ == "__main__":
    app.run(debug=True)
