#Code by Lysander Miller
import psycopg2
import argparse
from config import password
from config import database
from config import user

#Sets up argparse
def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Helps get information from an olympics database')
    parser.add_argument('--NOC', nargs='*',default='NoData', help='Gives information related to NOCs. If you want the names of all the athletes from a specified NOC, just type --NOC and then the NOC. If you want all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals, type --NOC gold. If you want all the NOCs and the number of silver medals they have won, in decreasing order of the number of gold medals, type --NOC silver.')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    #Connect to the database
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    arguments = get_parsed_arguments()
    if arguments.NOC != 'NoData':
        index = 0
        looking_for_gold_medal = False
        looking_for_silver_medal = False
        for countries_or_medals in arguments.NOC:
            if countries_or_medals == 'gold':
                looking_for_gold_medal = True
                index +=1
            elif countries_or_medals == 'silver':
                looking_for_silver_medal = True
                index +=1
            elif (countries_or_medals != 'gold' and countries_or_medals != 'silver'):
                # This portion of the code returns all the athlete names from the specified NOC
                search_string = countries_or_medals
                try:
                    cursor = connection.cursor()
                    query = 'SELECT DISTINCT athlete.name FROM athlete, athletes_and_country_and_year WHERE CAST(athletes_and_country_and_year.NOC AS text)=%s AND CAST(athletes_and_country_and_year.athlete_id AS text) = CAST(athlete.id AS text);'
                    cursor.execute(query, (search_string,))
                except Exception as e:
                    print(e)
                    exit()
                for row in cursor:
                    print(row[0])
                    print()
            if len(arguments.NOC) == index:
                if looking_for_gold_medal == True:
                    #This portion of the code returns all of the NOCs and the number of gold medals they've won in decreasing order
                    try:
                        cursor = connection.cursor()
                        query = "SELECT COUNT(get_medal.medal), NOC FROM athletes_and_country_and_year, get_medal WHERE CAST(athletes_and_country_and_year.athlete_id AS text)= CAST(get_medal.athlete_id AS text) AND CAST(athletes_and_country_and_year.year AS text)=CAST(get_medal.year AS text) AND get_medal.medal IN ('Gold') GROUP BY NOC ORDER BY COUNT(get_medal.medal) DESC;"
                        cursor.execute(query)
                    except Exception as e:
                        print(e)
                        exit()
                    for row in cursor:
                        print(row[0], row[1])
                        print()
                elif looking_for_silver_medal == True:
                    #This portion of the code returns all the NOCs and the number of silver medals they've won in decreasing order
                    try:
                        cursor = connection.cursor()
                        query = "SELECT COUNT(get_medal.medal), NOC FROM athletes_and_country_and_year, get_medal WHERE CAST(athletes_and_country_and_year.athlete_id AS text)= CAST(get_medal.athlete_id AS text) AND CAST(athletes_and_country_and_year.year AS text)=CAST(get_medal.year AS text) AND get_medal.medal IN ('Silver') GROUP BY NOC ORDER BY COUNT(get_medal.medal) DESC;"
                        cursor.execute(query)
                    except Exception as e:
                        print(e)
                        exit()
                    for row in cursor:
                        print(row[0], row[1])
                        print()
    connection.close()

#Main function
if __name__ == '__main__':
    main()
