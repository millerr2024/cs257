\copy athlete from 'athlete.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy country from 'country.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy athletes_and_country_and_year from 'athlete_and_country_and_year.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy NOC_and_team from 'NOC_and_team.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy get_city from 'get_city.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy get_medal from 'get_medal.csv' DELIMITER ',' CSV NULL AS 'NULL'
\copy athlete_and_events from 'get_event.csv' DELIMITER ',' CSV NULL AS 'NULL'
SELECT NOC FROM country
ORDER BY NOC;
SELECT name FROM athlete
WHERE team = 'Kenya';
SELECT * FROM get_medal WHERE athlete_id in (SELECT ID FROM athlete WHERE name LIKE '%Louganis%') AND medal NOT IN ('NA');
SELECT COUNT(get_medal.medal), NOC
FROM athletes_and_country_and_year, get_medal
WHERE CAST(athletes_and_country_and_year.athlete_id AS text)= CAST(get_medal.athlete_id AS text) AND CAST(athletes_and_country_and_year.year AS text)=CAST(get_medal.year AS text)
AND get_medal.medal IN ('Gold')
GROUP BY NOC
ORDER BY COUNT(get_medal.medal) DESC;

