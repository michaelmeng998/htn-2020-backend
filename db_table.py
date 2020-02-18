from __future__ import print_function
# from flask import Flask, g, jsonify
import itertools
import sqlite3
import os
import sys
import json

DATABASE = "hackers2.db"

database = json.load(open('data.json'))

conn = sqlite3.connect(DATABASE)

c = conn.cursor()

# create db table for users
c.execute('''
CREATE TABLE IF NOT EXISTS [users] (
	[userID] INTEGER PRIMARY KEY,
	[company] TEXT NOT NULL,
    [email] TEXT NOT NULL,
    [latitude] REAL NOT NULL,
    [longitude] REAL NOT NULL,
    [name] TEXT NOT NULL UNIQUE,
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
# query = "INSERT INTO users VALUES (?,?,?,?,?,?,?)"

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

print("done creating sql table!!!")
