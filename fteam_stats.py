"""
	Retrieves all team stats and saves them into folder
"""

from api.apifootball import APIFootball, Client, CustomEncoder
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
# Retrieving all teams in the league
dct_teams, _ = af_cl.get_teams(league)
for k, v in dct_teams.items():
	team_id = str(k)
	# Retrieving stats from team with key
	home_stats, away_stats = af_cl.get_teams_stats(team_id, league)
	# Retrieving current standings from a league
	standings, _ = af_cl.get_standings(league)
	# Update team standings
	team = standings[team_id]
	team.stats_home = home_stats
	team.stats_away = away_stats
	# Creates directory if it doesn't exist
	temp = dirName + '/' + team_id
	try:
		# Create target Directory
		os.mkdir(temp)
		print("Directory " , temp ,  " Created ") 
		# Create home team target Directory
		try:
			temp_home = temp + '/home'
			os.mkdir(temp_home)
			print("Directory " , temp_home ,  " Created ") 
		except FileExistsError:
			print("Directory " , temp_home ,  " already exists")
		# Create away team target Directory
		try:
			temp_away = temp + '/away'
			os.mkdir(temp_away)
			print("Directory " , temp_away ,  " Created ") 
		except FileExistsError:
			print("Directory " , temp_away ,  " already exists")
	except FileExistsError:
		print("Directory " , temp ,  " already exists")
	# Save finish standings into a json  
	json_object = json.dumps(team, indent = 4, cls=CustomEncoder)  
	# Saving into file
	file = temp + '/' + team_id + ".json"
	with open(file, "w") as outfile: 
		outfile.write(json_object)
	temp = dirName