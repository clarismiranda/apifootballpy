from datetime import datetime
from . import football
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
		Private method for setting attributes from a list
		to an object
	"""
	def _set_to_object(self, lst_obj, lst_key, obj):
		for i in range(0,len(lst_obj)):
			setattr(obj, lst_key[i], lst_obj[i])
	
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
		
		# List of leagues objects
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
			season = self.season
		# Uses the default client season if not changed
		endpoint = "/teams?league=" + league + "&season=" + season
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		data = res.read()
		teams = json.loads(data)
		
		# Dictionary of teams
		dct = {}
		for team in teams["response"]:
			team = team["team"]
			# The id of the team
			id_t = str(team["id"])
			# The object team
			t = football.Team(team["id"], team["name"])
			dct[id_t] = t
		return dct, teams["response"]

	"""
		Public method for getting a teams statistics in a league season
		league: the id of a league
		season: the YYYY format of the season to search
		team: the id of the team
		to: the YYYY-MM-DD to limit date
		Returns stats when home, stats when away
	"""
	def get_teams_stats(self, team, league, season=None, to=None):
		if season == None:
			season = self.season
		endpoint = "/teams/statistics?league=" + league + "&season=" + season + "&team=" + team
		if to != None:
			endpoint = endpoint + "&to=" + to
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		data = res.read()
		stats = json.loads(data)
		# Processing statistics
		lst_home = []
		lst_away = []
		stats = stats["response"]
		for key, value in stats["fixtures"].items():
			lst_home.append(value["home"])
			lst_away.append(value["away"])
		for key, value in stats["goals"].items():
			for k, v in value.items():
				# Everything from home matches
				lst_home.append(float(v["home"]))
				# Everything from away matches
				lst_away.append(float(v["away"]))
		lst_home.append(stats["clean_sheet"]["home"])
		lst_away.append(stats["clean_sheet"]["away"])
		lst_home.append(stats["failed_to_score"]["home"])
		lst_away.append(stats["failed_to_score"]["away"])
		# Creating empty variable
		stats_home = football.Stats()
		stats_away = football.Stats()
		# Keys for stats
		lst_keys = stats_home.ks
		# Setting stats
		self._set_to_object(lst_home, lst_keys, stats_home)
		self._set_to_object(lst_away, lst_keys, stats_away)
		
		lst_home = []
		lst_away = []
		# Defining streaks
		streak = stats["biggest"]
		for key, value in streak["streak"].items():
			lst_home.append(value)
			lst_away.append(value)
		lst_home.append(streak["wins"]["home"])
		lst_away.append(streak["wins"]["away"])
		lst_home.append(streak["loses"]["home"])
		lst_away.append(streak["wins"]["away"])
		for key, value in streak["goals"].items():
			# Everything from home matches
			lst_home.append(value["home"])
			# Everything from away matches
			lst_away.append(value["away"])
		# Creating empty variables
		streaks_home = football.Streaks()
		streaks_away = football.Streaks()
		# Keys for stats
		lst_keys = streaks_home.ks
		# Setting stats
		self._set_to_object(lst_home, lst_keys, streaks_home)
		self._set_to_object(lst_away, lst_keys, streaks_away)
		# Finishing stats
		stats_home.streaks = streaks_home
		stats_away.streaks = streaks_away
		
		return stats_home, stats_away

	"""
		Public method for getting the standings in a given league and season
		league: the id of a league
		season: the YYYY format of the season to search
		Returns the ids, name of the team, and its standings
	"""
	def get_standings(self, league, season=None):
		if season == None:
			season = self.season
		# Uses the default client season if not changed
		endpoint = "/standings?league=" + league + "&season=" + season
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		data = res.read()
		standings = json.loads(data)
		
		# Dictionary of teams with rank
		dct = {}
		for team in standings["response"][0]["league"]["standings"][0]:
			id_t = str(team["team"]["id"])
			t = football.Team(id_t, team["team"]["name"])
			stand = football.Standings(t, team["rank"], team["points"], 
					team["goalsDiff"], team["form"], team["description"])
			dct[id_t] = stand

		return dct, standings["response"][0]

	"""
		Public method for getting the matches in a given league and season
		league: the id of a league
		season: the YYYY format of the season to search
		team: the id of a team
		last: the last N fixtures
		nxt: the next N fixtures
		date: the exact date as YYYY-MM-DD
		frm: starting date as YYYY-MM-DD
		to: ending date as YYYY-MM-DD
		Returns the ids, name of the team and against team and its fixtures
	"""
	def get_fixtures(self, league, season=None, team=None, last=None,
					nxt=None, date=None, frm=None, to=None):
		if season == None:
			season = self.season
		# Uses the default client season if not changed
		endpoint = "/fixtures?league=" + league + "&season=" + season
		if team != None:
			endpoint = endpoint + "&team=" + team
		if date != None:
			endpoint = endpoint + "&date=" + date
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
		data = res.read()
		fixtures = json.loads(data)
		# List of id_fixtrure: id_home, id_against, name_home, name_against
		dct = {}
		for match in fixtures["response"]:
			id_f = match["fixture"]["id"]
			team = match["teams"]
			team_home = football.Team(team["home"]["id"], team["home"]["name"])
			team_away = football.Team(team["away"]["id"], team["away"]["name"])
			goals = match["goals"]
			dct[id_f] = football.Fixture(team_home, team_away, goals["home"], goals["away"])
		return dct, fixtures["response"]

	"""
		Public method for getting the statistics in a given fixture
		fixture: the id of the fixture
		team: the id of the team
		Returns the ids of the theam and its statistics
	"""
	def get_statistics(self, fixture, team=None):
		endpoint = "/fixtures/statistics?fixture=" + fixture
		if team != None:
			endpoint = endpoint + "&team=" + team
		# Request to the API
		self.Client.conn.request("GET", endpoint, headers=self.Client.headers)
		res = self.Client.conn.getresponse()
		data = res.read()
		statistics = json.loads(data)
		# Dictionary of id_team : fixture object with statistics
		dct = {}
		for team in statistics["response"]:
			id_t = str(team["team"]["id"])
			lst_stats = []
			for stat in team["statistics"]:
				lst_stats.append(stat["value"])
			# Keys for stats
			stats = football.StatsFixture()
			lst_keys = stats.ks
			# Setting stats
			self._set_to_object(lst_stats, lst_keys, stats)
			dct[id_t] = stats
		return dct, statistics["response"]

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

# Custom JSONEncoder
class CustomEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__