# from flask import Flask
# import sqlite3
# conn = sqlite3.connect('hackers.db')

# app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello, World! Michael Meng'

from __future__ import print_function
from flask import Flask, g, jsonify
import itertools
import sqlite3
import os
import sys
import json


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


@app.route("/")
def start():
    return 'start app :)'


@app.route("/users")
def index():
    print('before get_db cursor')
    cur = conn.cursor()
    cur.execute("select * from users where userID = 1")
    row = cur.fetchone()

    for row in cur:
        rowDict = dict(zip(row.keys(), row))
        print(rowDict)

    return "done"

    # rowDict = dict(zip(row.keys(), row))

    # return rowDict

    # return jsonify(data=res.fetchall())

    # cur = get_db().cursor(dictionary=True)
    # rows = cur.execute('''
    # SELECT * from users
    # ''').fetchall()
    # return json.dumps([dict(ix) for ix in rows])  # CREATE JSON
    # res = cur.execute("select * from users")
    # return jsonify(data=res.fetchall())
# return 'check your console :)'


if __name__ == "__main__":
    """
        Use python sqlite3 to create a local database, insert some basic data and then
        display the data using the flask templating.

        http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
    """
    app.run(debug=True)
