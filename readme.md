# Hack the North 2020 Backend Challenge

:rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker:

(This repo contains a sqlite + Flask install. The current directory is mounted as a volume under `/home/api` so that you do not have to rebuild the image every time. Building and running the image will start the Flask server on port 5000.)

# Documenting Design Decisions

1. For **database design descisions**, look at the database_design word document in the **/design_doc directory in this repo**

2. All API's are in one main.py file for simplicity sake, the db_table.py file is not necessary for the API, but it shows the script that creates the hackers database

3. I have added in a /create_db and /drop_db route for ease of creating and dropping the database tables via HTTP requests

# API routes

```
/users [GET]
```

This endpoint gets all users (along with all their information), in a JSON list form.
an example response is:

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
            },
            {
                "name": "Pitch Workshop"
            }
        ],
        "phone": "+1 (913) 504-2495",
        "latitude": 48.4862,
        "email": "elizawright@slambda.com"
    },
    .
    .
    .
]
```

This endpoint gets all users (along with all their information), in a JSON list form.
an example response is:

# What types of improvements can be made?

1. adding logging

2. imporving error handling

3. containerization, kubernetes

4. floating point arithmetic for the location query, need to improve this and not have hard coded solution to round the subtraction to 4 decimal places, this is not scalable and will not account for further accuracies. Also, the floating point arithmetic should be defined and referenced from the problem statement
