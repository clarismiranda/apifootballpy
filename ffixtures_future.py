"""
	Retrieves future fixtures' teams
"""

from api.apifootball import APIFootball, Client
from datetime import datetime, date
import json
import os
import sys

if len(sys.argv) > 3:
	# Setting country, league and season from system arguments
    country = sys.argv[1]
    league = sys.argv[2]
    season = sys.argv[3]
else:
    print("Wrong arguments were given, expected: --country --league --season")

# Retrieve key and host from terminal
api_key = os.getenv('AF_KEY')
api_host = os.getenv('AF_HOST')

# Where to save
dirName = '../PCA/' + country + '/' + league + '/'

cl = Client(api_key, api_host)
# Creates the client to the api with a country and season
af_cl = APIFootball(cl, country, season)
# Getting today's date
today = str(date.today())
# Retrieving all matches in the league
matches, _ = af_cl.get_fixtures(league, frm=today, to='2020-07-26')

# Output array of pair of teams in future matches
future_teams = []
future_matches = {}
for k, v in matches.items():
	match_id = str(k)
	home_team = int(v.team_home.id)
	away_team = int(v.team_away.id)
	future_teams.append([home_team, away_team])
	future_matches[match_id] = [home_team, away_team]

print("Future teams:")
print(future_teams)

# Path for saving future games
file_future = dirName + "next.json"
# Writting future games into a file
with open(file_future) as outfile:
	outfile.write(future_matches)