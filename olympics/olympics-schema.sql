CREATE TABLE athlete(id SERIAL, name text, sex text, height integer, weight integer, team text, sport text);
CREATE TABLE country(NOC text, region text, notes text);
CREATE TABLE athletes_and_country(athlete_id integer, NOC text);
CREATE TABLE NOC_and_team(NOC text, team text);
CREATE TABLE get_medal(year integer, event text, athlete_id integer, medal text);
CREATE TABLE get_city(year integer, season text, city text);
CREATE TABLE athlete_and_events(athlete_id integer, event text);

