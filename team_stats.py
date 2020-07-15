"""
	An example program for retrieving full statistics
	of an specific team
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
# Retrieving teams in league with key '140'
dct_teams, _ = af_cl.get_teams(league)
#for k, v in dct_teams.items():
    #print(k, v)
# Retrieving stats from team with key '529'
home_barca, away_barca = af_cl.get_teams_stats('529', league)
# Retrieving current standings from a league
standings, _ = af_cl.get_standings(league)
print(standings.items())
# Update team standings
barca = standings['529']
barca.stats_home = home_barca
barca.stats_away = away_barca

# Save final standings into a json  
json_object = json.dumps(barca, indent = 4, cls=CustomEncoder)  
# Saving into file
with open("barca.json", "w") as outfile: 
    outfile.write(json_object)
