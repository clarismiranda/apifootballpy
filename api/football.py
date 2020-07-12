"""
	Some data structures for identifying football elements
"""

# A class for identifying season's periods
class Season:
	"""
			start: the season start date
			end: the season end date
	"""
	def __init__(self, start, end):
		self.start = start
		self.end = end

	"""
			Prints a season object in string format
	"""
	def __str__(self):
		return "start=%s end=%s" % (self.start, self.end)

# A class for identifying league characteristics
class League:
	"""
			id: the id of the league
			name: the name of the league
			type: the type of league
			seasons: a dictionary of seasons in the league
	"""
	def __init__(self, id_league, name, ty):
		self.id = id_league
		self.name = name
		self.type = ty
		self.seasons = {}
	
	"""
			Maps a Season object to its year in the league
	"""
	def add_season(self, year, season):
		self.seasons[year] = season

	"""
			Prints a league object in string format
	"""
	def __str__(self):
		output = "id=%s name=%s, ty=%s" % (self.id, self.name, self.type)
		# Print seasons
		if len(self.seasons) > 0:
			output += "\n======\n"
			for key, value in self.seasons.items():
				output += str(key) + ": " + str(value) + "\n"
			output += "=======\n"
		return output

# A class for grouping team streaks
class Streaks:
	ks = ["wins", "draws", "loses", "best_win", "best_lose", "best_goals_for",
			"best_goals_against"]
	"""
			wins: continous wins
			draws: continous draws
			loses: continous loses
			best_win: best winner score
			best_lose: worst lose score
			best_goals_for: most goals by the team
			best_goals_against: most goals by the against team
	"""
	def __init__(self, wins=0, draws=0, loses=0, best_win="", best_lose="", 
					best_goals_for=0, best_goals_against=0):
		self.wins = wins
		self.draws = draws
		self.loses = loses
		self.best_win = best_win
		self.best_lose = best_lose
		self.best_goals_for = best_goals_for
		self.best_goals_against = best_goals_against

	"""
			Prints a streak object in string format
	"""
	def __str__(self):
		output = "wins=%s draws=%s loses=%s" % (self.wins, self.draws, self.loses)
		output += "best_win=%s best_lose=%s" % (self.best_win, self.best_lose)
		output += "best_goals_for=%s best_goals_against=%s" % (self.best_goals_for, self.best_goals_against)
		return output

# A class for grouping team statistics
class Stats:
	ks = ["played", "wins", "draws", "lose", "goals_for", "avg_goals_for",
			"goals_against", "avg_goals_against", "clean_sheet", "failed_to_score"]
	"""
			played: the amount of matches played
			wins: the amount of wins
			draws: the amount of draws
			lose: the amount of loses
			goals_for: the number of goals by the team
			avg_goals_for: the average of goals by the team
			goals_against: the number of goals against the team
			avg_goals_against: the average goals by the agains team
			clean_sheet: the amount of matches with no goals
						by the against team
			failed_to_score: the amount of matches with no 
						goals by the team
			streaks: streak of the team
	"""
	def __init__(self, played=0, wins=0, draws=0, lose=0, goals_for=0, avg_goals_for=0,
	 			goals_against=0, avg_goals_against=0, clean_sheet=0, failed_to_score=0,
	 			streaks=None):
		self.played = played
		self.wins = wins
		self.draws = draws
		self.lose = lose
		self.goals_for = goals_for
		self.avg_goals_for = avg_goals_for
		self.goals_against = goals_against
		self.avg_goals_against = avg_goals_against
		self.clean_sheet = clean_sheet
		self.failed_to_score = failed_to_score
		self.streaks = streaks

	"""
			Prints a stat object in string format
	"""
	def __str__(self):
		output = "played=%s wins=%s draws=%s" % (self.played, self.wins, self.draws)
		output += "lose=%s goals_for=%s" % (self.lose, self.goals_for)
		output += "avg_goals_for=%s goals_against=%s" % (self.avg_goals_for, self.goals_against)
		output += "avg_goals_against=%s clean_sheet=%s" % (self.avg_goals_against, self.clean_sheet)
		output += "failed_to_score=%s streaks=%s" % (self.failed_to_score, self.streaks)
		return output


# A class for identifying team characteristics
class Team:
	"""
			id: the id of the team
			name: the name of the team
	"""
	def __init__(self, id_team, name):
		self.id = id_team
		self.name = name

	"""
			Prints a team object in string format
	"""
	def __str__(self):
		return "id=%s name=%s" % (self.id, self.name)

# A class for identifying team standings
class Standings:
	"""
			team: a team object
			rank: the current rank in the league
			points: current points
			goals_diff: current goals difference
			form: last five matches as WWWWW
			description: promotion to champions/europe/second
			stats_home: a stats object from home matches
			stats_away: a stats object from away matches
	"""
	def __init__(self, team=None, rank=0, points=0, goals_diff=0, form="", description="",
				 stats_home=None, stats_away=None):
		self.team = team
		self.rank = rank
		self.points = points
		self.goals_diff = goals_diff
		self.form = form
		self.description = description
		self.stats_home = stats_home
		self.stats_away = stats_away

	"""
			Prints a standing object in string format
	"""
	def __str__(self):
		output = "team=%s rank=%s points=%s" % (self.team, self.rank, self.points)
		output += "goals_diff=%s form=%s" % (self.goals_diff, self.form)
		output += "description=%s stats_home=%s" % (self.description, self.stats_home)
		output += "stats_away=%s " % (self.stats_away)
		return output