#!/usr/bin/env python3
'''
Code by Lysander Miller
An API based on an olympics database.
'''
import flask
import json
import sys
import psycopg2
from config import password
from config import database
from config import user
app = flask.Flask(__name__)

#Try to connect to the database
try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()
'''
REQUEST: /games

RESPONSE: a JSON list of dictionaries, each of which represents one
Olympic games, sorted by year. Each dictionary in this list will have
the following fields.

    id -- (INTEGER) a unique identifier for the games in question
    year -- (INTEGER) the 4-digit year in which the games were held (e.g. 1992)
    season -- (TEXT) the season of the games (either "Summer" or "Winter")
    city -- (TEXT) the host city (e.g. "Barcelona")
'''

@app.route('/games')
def get_games():
    list_of_games = []
    try:
        cursor = connection.cursor()
        query = 'SELECT * FROM get_city ORDER BY year;'
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    row_number = 0
    for row in cursor:
        list_of_games.append({"id":row_number, "year":int(row[0]), "season":row[1], "city":row[2]}) 
        row_number +=1
    return json.dumps(list_of_games)

'''
REQUEST: /nocs

RESPONSE: a JSON list of dictionaries, each of which represents one
National Olympic Committee, alphabetized by NOC abbreviation. Each dictionary
in this list will have the following fields.

    abbreviation -- (TEXT) the NOC's abbreviation (e.g. "USA", "MEX", "CAN", etc.)
    name -- (TEXT) the NOC's full name (see the noc_regions.csv file)
'''

@app.route('/nocs')
def get_nocs():
    noc_list = []
    try:
        cursor = connection.cursor()
        query = 'SELECT NOC, region FROM country ORDER BY NOC;'
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    for row in cursor:
        noc_list.append({"abbreviation":row[0], "name":row[1]})
    return json.dumps(noc_list)


'''
REQUEST: /medalists/games/<games_id>?[noc=noc_abbreviation]

RESPONSE: a JSON list of dictionaries, each representing one athlete
who earned a medal in the specified games. Each dictionary will have the
following fields.

   athlete_id -- (INTEGER) a unique identifier for the athlete
   athlete_name -- (TEXT) the athlete's full name
   athlete_sex -- (TEXT) the athlete's sex as specified in the database ("F" or "M")
   sport -- (TEXT) the name of the sport in which the medal was earned
   event -- (TEXT) the name of the event in which the medal was earned
   medal -- (TEXT) the type of medal ("gold", "silver", or "bronze") 
If the GET parameter noc=noc_abbreviation is present, this endpoint will return
only those medalists who were on the specified NOC's team during the specified
games.

The <games_id> is whatever string (digits or otherwise) that your database/API
uses to uniquely identify an Olympic games.

'''

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    medalists_list = []
    noc = flask.request.args.get('noc')
    game_year = 0
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM get_city ORDER BY year;"
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()
    list_of_games = []
    row_number = 0
    for row in cursor:
        list_of_games.append({"id":row_number, "year":row[0], "season":row[1], "city":row[2]})
        row_number +=1
    for game in list_of_games:
        if game.get("id") == int(games_id):
            game_year = game.get("year")
    if noc is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT athlete.id, athlete.name, athlete.sex, athlete.sport, get_medal.event, get_medal.medal FROM athlete, get_medal, athletes_and_country_and_year WHERE athlete.id = get_medal.athlete_id AND get_medal.year=%s AND get_medal.medal != 'NA' AND athlete.id = athletes_and_country_and_year.athlete_id AND athletes_and_country_and_year.year=%s AND athletes_and_country_and_year.NOC IN (%s) ORDER BY athlete.id ASC;"
            cursor.execute(query, (game_year,game_year, noc))
        except Exception as e:
            print(e)
            exit()
    else:
        try:
            cursor = connection.cursor()
            query = "SELECT athlete.id, athlete.name, athlete.sex, athlete.sport, get_medal.event, get_medal.medal FROM athlete, get_medal WHERE athlete.id = get_medal.athlete_id AND get_medal.year = %s AND get_medal.medal != 'NA' ORDER BY athlete.id ASC;"
            cursor.execute(query, (game_year,))
        except Exception as e:
            print(e)
            exit()
    for row in cursor:
        medalists_list.append({"athlete_id":int(row[0]), "athlete_name":row[1], "athlete_sex": row[2], "sport": row[3], "event":row[4], "medal":row[5]})
    return json.dumps(medalists_list)

#Main method that parses the command line
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2], debug=True)
