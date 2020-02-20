# Hack the North 2020 Backend Challenge

:rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker:

(This repo contains a sqlite + Flask install. The current directory is mounted as a volume under `/home/api` so that you do not have to rebuild the image every time. Building and running the image will start the Flask server on port 5000.)

# Documenting Design Decisions

1. For **database design descisions**, look at the database_design word document in the **/design_doc directory in this repo**

2. All API's are in one main.py file for simplicity sake, the db_table.py file is not necessary for the API, but it shows the script that creates the hackers database

3. I have added in a /create_db and /drop_db route for ease of creating and dropping the database tables via HTTP requests

# HOW TO RUN THE API

1. Open up the Docker desktop app, sign in
2. in the base of this repo ,run docker-compose up
3. hit the http://localhost:5000/create_db endpoint once (would recommend using something like postman for testing)
4. start testing out the API :))

# API routes

## /create_db

```
/create_db
```

This api will parse the data.json value and create the corresponding database tables based off of the structure mentioned in the /design_doc/database_design document in this repo.

**IMPORTANT: This API should only be hit once during the beggining. If this endpoint is hit multiple times, then the database will have duplicated data and will corrupt query results. (This is tech debt that needs to be addressed as an improvement).**

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

This endpoint gets a specific user with a certain \<id> from the database. The user object includes picture url, name, company, longitude, latitude, phone, email, and all of their attended events.

An example successful response for user \<id> = 1212 :

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

In the case where the userID is a positive integer, but the userID does not exist (like passing in id = 100000), an empty list [] is returned.

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

This endpoint gets all user objects associated with the event \<id>. The response is a json object with eventName, eventID, and an attendees list of user objects. Every user object will only contain the picture url, name, company, longitude, phone, latitude, and email.

An example successful response for event \<id> = 1 :

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

In the case where the eventID is a positive integer, but the eventID does not exist (like passing in id = 100000), an empty list [] is returned.

## /events/\<id>/attendees

```
/events/<id>/attendees [POST]
```

This endpoint allows the ability to add a user to an event. The \<id> is the eventID that you want to add a user to. The \<id> must be a positive integer number (a 400 status code and error message is returned if the id is negative or contains letters). Also, if the eventID does not exist (like an eventID = 10000), a error message is returned saying so.

Furthermore, the userID is defined in the form:

```json
{
  "user_id": "1"
}
```

the key must be named 'user_id' and the endpoint can only add 1 user_id at a time to an event. Also, the user_id should be a positive integer number. If any of these restrictions are broken, a 400 status code is returned along with an error message. If the user_id does not exist in the database, then the api will return a message saying so.

When the request to add the user to the event is successful, then the following success message is returned:

```
User has been sucesfully added to event :)
```

If the user is already attending the event, then the endpoint will return the following message:

```
IntegrityError: user is already attending event
```

# What types of improvements can be made?

1. number one improvement would be to utilize a primary key / foreign key database design. This would help with the users/\<id>/attendees POST route in terms of dealing with userID's and eventID's that don't exist in the database. Right now, I am running query's to check the existence of those entities in the DB, but a primary/foreign key constraint would be a much more efficient method to tackle this issue.

2. improving error handling, being more specific, catching more edge cases

3. floating point arithmetic for the location query, need to improve this and not have hard coded solution to round the subtraction to 4 decimal places, this is not scalable and will not account for further accuracies. Also, the floating point arithmetic should be defined and referenced from the problem statement

4. fix the error so hitting the create_db endpoint multiple times will not add duplicate data

5. adding unit tests to each route (for time sake, I did not add any unit tests to the API's. I did mostly manual testing)

6. adding in support to format the order of the JSON response. the JSON responses are created using python dictionaries, which are hard to define an order when they are being zipped and packaged into a dict object to be returned as a response

7. if the API's will be experiencing high loads, I would containerize and deploy the API's into kubernetes clusters. This would provide load balancing, pod re-creation, and other features that would help support the activity of the API'.
