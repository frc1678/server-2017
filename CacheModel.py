class CachedTeamData(object):
	def __init__(self, teamNumber):
		super(CachedTeamData, self).__init__()
		self.number = teamNumber
		self.completedTIMDs = []

class CachedCompetitionData(object):
	def __init__(self):
		super(CachedCompetitionData, self).__init__()
		self.teamsWithMatchesCompleted = []
		self.speedZScores = {-1 : 0}
		self.agilityZScores = {-1 : 0}
		self.ballControlZScores = {-1 : 0}
		self.gearControlZScores = {-1 : 0}
		self.predictedSeedings = []
		self.actualSeedings = []
		self.TBAMatches = {}
		self.zGearProbabilities = {}
