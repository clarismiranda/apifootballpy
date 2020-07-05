"""
	An example program using API-Football Client
"""

from api.apifootball import APIFootball, Client
import os

# Retrieve key and host from terminal
api_key = os.getenv('AF_KEY')
api_host = os.getenv('AF_HOST')

cl = Client(api_key, api_host)
# Creates the client to the api with a country and season
af_cl = APIFootball(cl,'ES','2019')
# Gets league from an specific client country
lst, _ = af_cl.get_league()

for e in lst:
	print(e)
