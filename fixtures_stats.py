"""
	An example program for retrieving fixture's 
	statistics from season 2019
"""

from api.apifootball import APIFootball, Client, CustomEncoder
import json
import os

# Retrieve key and host from terminal
api_key = os.getenv('AF_KEY')
api_host = os.getenv('AF_HOST')

# LaLiga id
league = '140'

cl = Client(api_key, api_host)
# Creates the client to the api with a country and season
af_cl = APIFootball(cl,'ES','2019')
# Retrieving fixture with team and date
matches, response = af_cl.get_fixtures(league, team='529', date='2020-07-11')
match = None
for k, v in matches.items():
	match_id = str(k)
	home_team = str(v.team_home.id)
	away_team = str(v.team_away.id)
	# Gets statistics from a match
	statistics, _ = af_cl.get_statistics(match_id)
	match = v
	match.stats_home = statistics[home_team]
	match.stats_away = statistics[away_team]

# Save final statistics into a json  
json_object = json.dumps(match, indent = 4, cls=CustomEncoder)  
# Saving into file
with open("fixture.json", "w") as outfile: 
    outfile.write(json_object)