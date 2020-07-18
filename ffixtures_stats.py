"""
	Retrieves all fixtures stats and saves them into folder
"""

from api.apifootball import APIFootball, Client, CustomEncoder
from datetime import datetime, date
import json
import os
import sys

if len(sys.argv) > 2:
	# Setting league and season from system arguments
    league = sys.argv[1]
    season = sys.argv[2]
else:
    print("Wrong arguments were given, expected: --league --season")

# Saving directory
dirName = os.getenv('DIR_NAME') + '/' + league + '/' + season

# Retrieve key and host from terminal
api_key = os.getenv('AF_KEY')
api_host = os.getenv('AF_HOST')

cl = Client(api_key, api_host)
# Creates the client to the api with a country and season
af_cl = APIFootball(cl,'ES', season)
# Retrieving all matches in the league
matches, _ = af_cl.get_fixtures(league)
# Future matches dictionary
dct_future = {}
for k, v in matches.items():
	match_id = str(k)
	home_team = str(v.team_home.id)
	away_team = str(v.team_away.id)
	# Directory where to save
	temp_home = dirName + '/' + home_team + '/home'
	temp_away = dirName + '/' + away_team + '/away'
	# Gets statistics from a match
	statistics, _ = af_cl.get_statistics(match_id)
	match = v
	try:
		match.stats_home = statistics[home_team]
		match.stats_away = statistics[away_team]
	except:
		# Dictionary for saving future matches
		dct_future[match_id] = {
			"home_id" = home_team
			"away_id" = away_team
		}
	# Save finish standings into a json  
	json_object = json.dumps(match, indent = 4, cls=CustomEncoder)  
	# Saving into file
	file_home = temp_home + '/' + match_id + ".json"
	file_away = temp_away + '/' + match_id + ".json"
	# Path for saving future games
	file_future = dirName + "next.json"
	with open(file_home, "w") as outfile: 
		outfile.write(json_object)
	with open(file_away, "w") as outfile: 
		outfile.write(json_object)
	# Writting future games into a file
	with open(dirName) as outfile:
		outfile.write(dct_future)