#Created by Lysander Miller
import csv
class Row_from_athlete:
    def __init__(self, id_num, name, sex, height, weight, team, NOC, year, season, city, sport, event, medal):
        self.id_num = id_num
        self.name = name
        self.sex = sex
        self.height = height
        self.weight = weight
        self.team = team
        self.NOC = NOC
        self.year = year
        self.season = season
        self.city = city
        self.sport = sport
        self.event = event
        self.medal = medal
class Row_from_country:
    def __init__(self, NOC, region, notes):
        self.NOC = NOC
        self.region = region
        self.notes = notes

list_of_athlete_rows = []
kaggle_athlete_events_file = open('athlete_events.csv', 'r')
athlete_events_reader = csv.reader(kaggle_athlete_events_file)
row_num = 0
for row in athlete_events_reader:
    if row_num != 0:
        id_num = row[0]
        name = row[1]
        sex = row[2]
        if row[4].isdigit():
            height = row[4]
        else:
            height = 'NA'
        if row[5].isdigit():
            weight = row[5]
        else:
            weight = 'NA'
        team = row[6]
        NOC = row[7]
        year = row[9]
        season = row[10]
        city = row[11]
        sport = row[12]
        event = row[13]
        if row[14] != 'NA':
            medal = row[14]
        else:
            medal = 'NA'
        list_of_athlete_rows.append(Row_from_athlete(id_num, name, sex, height, weight, team, NOC, year, season, city, sport, event, medal))
    row_num += 1
list_of_country_rows = []
kaggle_noc_regions_file = open('noc_regions.csv', 'r')
noc_regions_file_reader = csv.reader(kaggle_noc_regions_file)
row_num = 0
for row in noc_regions_file_reader:
    if row_num != 0:
        NOC = row[0]
        region = row[1]
        notes = 'None'
        if row[2] != '':
            notes = row[2]
        list_of_country_rows.append(Row_from_country(NOC, region, notes))
    row_num +=1

with open('athlete.csv', 'w') as athlete_file:
    writer = csv.writer(athlete_file)
    previously_added_athlete_ids = {}
    for athlete_row in list_of_athlete_rows:
        if (athlete_row.id_num in previously_added_athlete_ids) == False:
            writer.writerow([athlete_row.id_num, athlete_row.name, athlete_row.sex, athlete_row.height, athlete_row.weight, athlete_row.team, athlete_row.sport])
            previously_added_athlete_ids[athlete_row.id_num] = None
   
with open('country.csv', 'w') as country_file:
    writer = csv.writer(country_file)
    for country_row in list_of_country_rows:
        writer.writerow([country_row.NOC, country_row.region, country_row.notes])
   
with open('athlete_and_country_and_year.csv', 'w') as athlete_and_country_and_year:
    writer = csv.writer(athlete_and_country_and_year)
    #dictionary contains athlete id as key and year as value
    dictionary = {}
    for athlete_row in list_of_athlete_rows:
        if athlete_row.id_num not in dictionary:
            dictionary[athlete_row.id_num] = [athlete_row.year]
            writer.writerow([athlete_row.id_num, athlete_row.NOC, athlete_row.year])
        elif ((athlete_row.year in dictionary.get(athlete_row.id_num)) == False):
            dictionary.get(athlete_row.id_num).append(athlete_row.year)
            writer.writerow([athlete_row.id_num, athlete_row.NOC, athlete_row.year])

with open('NOC_and_team.csv', 'w') as NOC_and_team:
    writer = csv.writer(NOC_and_team)
    previously_added_team = {}
    for athlete_row in list_of_athlete_rows:
        if (athlete_row.team in previously_added_team) == False:
            writer.writerow([athlete_row.NOC, athlete_row.team])
            previously_added_team[athlete_row.team] = None          

with open('get_city.csv', 'w') as get_city:
    writer = csv.writer(get_city)
    previously_added_information = {}
    for athlete_row in list_of_athlete_rows:
        if (athlete_row.year not in previously_added_information) or (athlete_row.season not in previously_added_information.get(athlete_row.year)):
            writer.writerow([athlete_row.year, athlete_row.season, athlete_row.city])
            if athlete_row.year in previously_added_information:
                previously_added_information.get(athlete_row.year).append(athlete_row.season)
            else:
                previously_added_information[athlete_row.year] = [athlete_row.season]

with open('get_medal.csv', 'w') as get_medal:
    writer = csv.writer(get_medal)
    for athlete_row in list_of_athlete_rows:
        writer.writerow([athlete_row.year, athlete_row.event, athlete_row.id_num, athlete_row.medal])

with open('get_event.csv', 'w') as get_event:
    writer = csv.writer(get_event)
    previously_added_information = {}
    athlete_already_done = False
    event_already_done = False
    for athlete_row in list_of_athlete_rows:
        if athlete_row.id_num in previously_added_information:
            athlete_already_done = True
            if athlete_row.event in previously_added_information.get(athlete_row.id_num):
                event_already_done = True
        if (athlete_already_done == False) and (event_already_done == False):
            previously_added_information[athlete_row.id_num] = [athlete_row.event]
        elif (athlete_already_done == True) and (event_already_done == False):
            previously_added_information.get(athlete_row.id_num).append(athlete_row.event)
        athlete_already_done = False
        event_already_done = False
    for key in previously_added_information:
        for value in previously_added_information.get(key):
            writer.writerow([key, value])

