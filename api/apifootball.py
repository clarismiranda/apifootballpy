from datetime import datetime
import football
import http.client
import json

# A custom client for API-Football
class APIFootball:
	"""
			Client: the HTTP Client to the API
			country: the Alpha2code of the country
			league: the type of the league, is it a tournament or cup
			season: the YYYY of the season league
	"""
	
	def __init__(self, Client, country, season=None, league=None):
		self.Client = Client
		self.country = country
		self.season = self._get_season(season)
		self.league = league

	"""
		Private method for setting season to query
	"""
	def _get_season(self, season):
		if season == None:
			return str(datetime.now().year-1)
		else:
			return season
	
	"""
		Public method for getting the leagues of the clients country
		ty: the type of league as tournament or cup
		Returns the id, name, type and last season of the league in the country
	"""
	def get_league(self, ty=None):
		# Endpoint with no type
		endpoint = "/leagues?code=" + self.country
		if ty != None:
			endpoint = endpoint + "&type=" + type
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		data = res.read()
		leagues = json.loads(data)
		
		# List of id, name, type, last season start and end date
		lst = []
		for league in leagues["response"]:
			l = league["league"]
			lea = football.League(l["id"], l["name"], l["type"])
			# Retrieving seasons
			for season in league["seasons"]:
				sea = football.Season(season["start"], season["end"])
				lea.add_season(season["year"], sea)
			lst.append(lea)
		return lst, leagues["response"]


	"""
		Public method for getting the teams in a given league
		league: the id of a league
		season: the YYYY format of the season to search
		Returns the ids and the name of the team in a league
	"""
	def get_teams(self, league, season=None):
		if season == None:
			season = self.Client.season
		# Uses the default client season if not changed
		endpoint = "/teams?league=" + league + "&season=" + season
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		teams = res.json
		# List of id, name
		lst = []
		for team in teams["response"]:
			lst.append([team["id"],team["name"]])

		return lst, teams["response"]

	"""
		Public method for getting the standings in a given league and season
		league: the id of a league
		season: the YYYY format of the season to search
		Returns the ids, name of the team, and its standings
	"""
	def get_standings(self, league, season=None):
		if season == None:
			season = self.Client.season
		# Uses the default client season if not changed
		endpoint = "/standings?league=" + league + "&season=" + season
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		teams = res.json
		# List of id, name
		lst = []
		for team in teams:
			lst.append(list(team["id"],team["name"]))

		return lst

	"""
		Public method for getting the matches in a given league and season
		league: the id of a league
		season: the YYYY format of the season to search
		team: the id of a team
		last: the last N fixtures
		nxt: the next N fixtures
		frm: starting date as YYYY-MM-DD
		to: endind date as YYYY-MM-DD
		Returns the ids, name of the team and against team and its fixtures
	"""
	def get_fixtures(self, league, season=None, team=None, last=None, nxt=None, frm=None, to=None):
		if season == None:
			season = self.Client.season
		# Uses the default client season if not changed
		endpoint = "/fixtures?league=" + league + "&season=" + season
		if team != None:
			endpoint = endpoint + "&team=" + team
		if last != None:
			endpoint = endpoint + "&last=" + last
		if nxt != None:
			endpoint = endpoint + "&next=" + nxt
		if frm != None:
			endpoint = endpoint + "&from=" + frm
		if to != None:
			endpoint = endpoint + "&to=" + to
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		teams = res.json
		# List of id, name
		lst = []
		for team in teams:
			lst.append(list(team["id"],team["name"]))

		return lst

	"""
		Public method for getting the statistics in a given fixture
		fixture: the id of the fixture
		team: the id of the team
		Returns the ids of the theam and its statistics
	"""
	def get_statistics(self, fixture, team=None):
		endpoint = "fixtures/statistics?fixture=" + fixture
		if team != None:
			endpoint = endpoint + "&team=" + team
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		teams = res.json
		# List of id, name
		lst = []
		for team in teams:
			lst.append(list(team["id"],team["name"]))

		return lst

# A client for API-Football
class Client:
	"""
			key: the rapidapi key
			host: the endpoint version to the API
			conn: the HTTP connection with host
			headers: the Headers with key and host
	"""
	def __init__(self, key, host, conn=None, headers=None):
		self.key = key
		self.host = host
		self.conn = http.client.HTTPSConnection(host)
		self.headers = {
    		'x-rapidapi-host': host,
    		'x-rapidapi-key': key
    	}