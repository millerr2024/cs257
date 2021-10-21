CREATE TABLE athlete(id text, name text, sex text, height text, weight text, team text, sport text);
CREATE TABLE country(NOC text, region text, notes text);
CREATE TABLE athletes_and_country_and_year(athlete_id text, NOC text, year text);
CREATE TABLE NOC_and_team(NOC text, team text);
CREATE TABLE get_medal(year text, event text, athlete_id text, medal text);
CREATE TABLE get_city(year text, season text, city text);
CREATE TABLE athlete_and_events(athlete_id text, event text);

