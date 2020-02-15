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

conn.commit()

query = "INSERT INTO users (company, email, latitude, longitude, name, phone, picture) VALUES (?,?,?,?,?,?,?)"
# query = "INSERT INTO users VALUES (?,?,?,?,?,?,?)"
columns = ['company', 'email', 'latitude',
           'longitude', 'name', 'phone', 'picture']
for data in database:
    keys = tuple(data[c] for c in columns)
    cur = conn.cursor()
    cur.execute(query, keys)
    cur.close()

conn.commit()

print("done creating sql table!!!")

# cur = db.cursor()
# res = cur.execute("select * from users where userID = 2")
# print("after exit select query")
# print(res.fetchall())
