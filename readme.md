# Hack the North 2020 Backend Boilerplate

:rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker::rice_cracker:

(This boilerplate contains a sqlite + Flask install. The current directory is mounted as a volume under `/home/api` so that you do not have to rebuild the image every time. Building and running the image will start the Flask server on port 5000.)

#Documenting Design Decisions

1. setting up the sqlite database, need to parse JSON file into sqlite

1.1) What's the best way to set up the table? What kind of relationships do we have? etc?

2. write the 3 user endpoints. use the sqlite database for querying, joining tables, etc

3. idk
