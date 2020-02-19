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

**Important This API should only be hit once during the beggining. If this endpoint is hit multiple times, then the database will have duplicated data and will corrupt query results. (This is tech debt that needs to be addressed as an improvement).**

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

An example successful response is:

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

An example successful response for user <id> = 1212 :

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
[], userID does not exist
```

## /users/params\?lat=\<REAL>\&long=\<REAL>\&range=\<REAL>

```
/users/params?lat=<REAL>&long=<REAL>&range=<REAL> [GET]
```

This endpoint takes in 3 parameters (latitude, longitude, and range). Then it finds and returns all user objects whose latitude and longitude are within +/- of the 'range' corresponding to the input 'lat' and 'long' values.

Given the following request:

```
http://localhost:5000/users/params?lat=48.4862&long=-34.7754&range=0.088
```

The successful response would be in the form:

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
  {
    "picture": "http://lorempixel.com/200/200/sports/6",
    "name": "Rhea Mills",
    "company": "Irack",
    "longitude": -34.7397,
    "events": [
      {
        "name": "Intro to Android"
      },
      {
        "name": "Mochi Ice Cream Balls"
      },
      {
        "name": "Bubble Soccer"
      }
    ],
    "phone": "+1 (882) 436-3069",
    "latitude": 48.5742,
    "email": "wilsonmaxwell@irack.com"
  }
]
```

There is also error handling implemented. For instance, if any of the inputs are missing, a 400 status code with a message is returned. If any of the inputs contain alphabetical letters (invalid input) a 400 status code with a message is returned.

In the case where no users within range are found, an empty list [] is returned

One design choice implemented here was in the search query WHERE clause:

```sql
WHERE ROUND(ABS(u.latitude - ?), 4) <= ABS(?)  AND ROUND(ABS(u.longitude - ?), 4) <= ABS(?)
```

I chose to round the difference between the latitudes and longitudes to 4 decimal places to account for floating point arithmetic inconsistiencies with sqlite's arithemtic operations. I saw that in the json data, the maximum precision of all latitude and longitude values were to 4 decimal places. This made a big difference in being able to include users who were right on the border of the range within the input latitude and longitude values.

## /events/\<id>

```
/events/<id> [GET]
```

This endpoint gets all user objects associated with the event <id>. The user objects are returned to only show

An example successful response for event <id> = 1 :

```json
{
    "eventName": "Intro to Android",
    "eventID": "1",
    "attendees": [
        {
            "picture": "http://lorempixel.com/200/200/sports/8",
            "name": "Jenna Luna",
            "company": "Slambda",
            "longitude": -34.7754,
            "phone": "+1 (913) 504-2495",
            "latitude": 48.4862,
            "email": "elizawright@slambda.com"
        },
        ...
    ]
}
```

There is error handling implemented where if the id is not a positive integer (like a negative integer or contains letters), then a 400 response with an error message is sent back.

In the case where the eventID is a positive integer, but the eventID does not exist (like passing in id = 100000), the following response is returned:

```json
[], eventID does not exist
```

# What types of improvements can be made?

1. adding logging

2. imporving error handling

3. containerization, kubernetes

4. floating point arithmetic for the location query, need to improve this and not have hard coded solution to round the subtraction to 4 decimal places, this is not scalable and will not account for further accuracies. Also, the floating point arithmetic should be defined and referenced from the problem statement
