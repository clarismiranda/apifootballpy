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
