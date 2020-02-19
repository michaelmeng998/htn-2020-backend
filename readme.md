# Hack the North 2020 Backend Challenge

:rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker:

(This repo contains a sqlite + Flask install. The current directory is mounted as a volume under `/home/api` so that you do not have to rebuild the image every time. Building and running the image will start the Flask server on port 5000.)

# Documenting Design Decisions

1. For **database design descisions**, look at the database_design word document in the **/design_doc directory in this repo**

2. All API's are in one main.py file for simplicity sake, the db_table.py file is not necessary for the API, but it shows the script that creates the hackers database

3. I have added in a /create_db and /drop_db route for ease of creating and dropping the database tables via HTTP requests

# API routes

## /create_db

```
/create_db
```

This api will parse the data.json value and create the corresponding database tables based off of the structure mentioned in the /design_doc/database_design document in this repo.
**Important** This API should only be hit once during the beggining. If this endpoint is hit multiple times, then the database will have duplicated data and will corrupt query results. (This is tech debt that needs to be addressed as an improvement).

## /drop_db

```
/drop_db
```

This api will drop all of the database tables created by the /create_db route (users, events, and userEvents).

## /users

```
/users [GET]
```

This endpoint gets all users in a JSON list form. The user objects include picture url, name, company, longitude, latitude, phone, email, and all of their attended events.

An example successfull response is:

```json
[
    {
        "picture": "http://lorempixel.com/200/200/sports/8",
        "name": "Jenna Luna",
        "company": "Slambda",
        "longitude": -34.7754,
        "events": [
            {
                "name": "Intro to Android"
            },
            {
                "name": "Cup Stacking"
            }
        ],
        "phone": "+1 (913) 504-2495",
        "latitude": 48.4862,
        "email": "elizawright@slambda.com"
    },
    ...
]
```

## /users/\<id>

```
/users/<id> [GET]
```

This endpoint gets a specific user with certain <id> from the database. The user object includes picture url, name, company, longitude, latitude, phone, email, and all of their attended events.

An example successfull response is:

```json
{
  "picture": "http://lorempixel.com/200/200/sports/0",
  "name": "Lori Long",
  "company": "Bostonic",
  "longitude": -36.7292,
  "events": [
    {
      "name": "Intro to Android"
    },
    {
      "name": "API Workshop"
    }
  ],
  "phone": "+1 (851) 575-2691",
  "latitude": 48.9062,
  "email": "christianmcdaniel@bostonic.com"
}
```

There is error handling implemented where if the id is not a positive integer (like a negative integer or contains letters), then a 400 response with an error message is sent back.

In the case where the userID is a positive integer, but the userID does not exist (like passing in id = 100000), the following response is returned:

```json
[], eventID does not exist
```

## /users/params\?lat=<REAL>\&long=<REAL>\&range=<REAL>

```
/users/params?lat=<REAL>&long=<REAL>&range=<REAL> [GET]
```

This endpoint takes in 3 parameters (latitude, longitude, and range). Then it find all users whose latitude and longitude are within +/- of the 'range' corresponding to the input 'lat' and 'long' values.

An example successfull response is:

```json
{
  "picture": "http://lorempixel.com/200/200/sports/0",
  "name": "Lori Long",
  "company": "Bostonic",
  "longitude": -36.7292,
  "events": [
    {
      "name": "Intro to Android"
    },
    {
      "name": "API Workshop"
    }
  ],
  "phone": "+1 (851) 575-2691",
  "latitude": 48.9062,
  "email": "christianmcdaniel@bostonic.com"
}
```

There is error handling implemented where if the id is not a positive integer (like a negative integer or contains letters), then a 400 response with an error message is sent back.

In the case where the userID is a positive integer, but the userID does not exist (like passing in id = 100000), the following response is returned:

```json
[], eventID does not exist
```

# What types of improvements can be made?

1. adding logging

2. imporving error handling

3. containerization, kubernetes

4. floating point arithmetic for the location query, need to improve this and not have hard coded solution to round the subtraction to 4 decimal places, this is not scalable and will not account for further accuracies. Also, the floating point arithmetic should be defined and referenced from the problem statement
