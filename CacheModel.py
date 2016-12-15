class CachedTeamData(object):
	def __init__(self, teamNumber):
		super(CachedTeamData, self).__init__()
		self.number = teamNumber
		self.alphas = {}
		self.betas = {}
		self.defensesFaced = []
		self.completedTIMDs = []

class CachedCompetitionData(object):
	def __init__(self):
		super(CachedCompetitionData, self).__init__()
		self.defenseSightings = None
		self.teamsWithMatchesCompleted = []
		self.speedZScores = {-1 : 0}
		self.torqueZScores = {-1 : 0}
		self.agilityZScores = {-1 : 0}
		self.ballControlZScores = {-1 : 0}
		self.defenseZScores = {-1 : 0}
		self.drivingAbilityZScores = {-1 : 0}
		self.predictedSeedings = []
		self.actualSeedings = []
		self.SARs = []
		self.TBAMatches = {}
