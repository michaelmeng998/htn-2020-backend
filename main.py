# from flask import Flask
# import sqlite3
# conn = sqlite3.connect('hackers.db')

# app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello, World! Michael Meng'

from __future__ import print_function
from flask import Flask, g, jsonify
import sqlite3
import os
import sys

DATABASE = "./hackers.db"

# Create app
app = Flask(__name__)

# check if the database exist, if not create the table and insert a few lines of data
# if not os.path.exists(DATABASE):
conn = sqlite3.connect(DATABASE)
# cur = conn.cursor()
# cur.execute("CREATE TABLE users (fname TEXT, lname TEXT, age INTEGER);")
# conn.commit()
# cur.execute("INSERT INTO users VALUES('Mike', 'Tyson', '40');")
# cur.execute("INSERT INTO users VALUES('Thomas', 'Jasper', '40');")
# cur.execute("INSERT INTO users VALUES('Jerry', 'Mouse', '40');")
# cur.execute("INSERT INTO users VALUES('Peter', 'Pan', '40');")
# conn.commit()
# conn.close()


# helper method to get the database since calls are per thread,
# and everything function is a new thread when called
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


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
    cur = get_db().cursor()
    res = cur.execute("select * from users")
    return jsonify(data=res.fetchall())
    # return 'check your console :)'


if __name__ == "__main__":
    """
        Use python sqlite3 to create a local database, insert some basic data and then
        display the data using the flask templating.

        http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
    """
    app.run(debug=True)
