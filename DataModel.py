import firebaseCommunicator
import utils
#Classes That Reflect Firebase Data Structure

class Competition(object):
	"""docstring for Competition"""
	def __init__(self):
		super(Competition, self).__init__()
		self.code = ""
		self.teams = []
		self.matches = []
		self.TIMDs = []
		self.predictedSeeding = []
		self.actualSeeding = []
		self.currentMatchNum = 0
	
	def updateTeamsAndMatchesFromFirebase(self):
		self.teams = utils.makeTeamsFromDicts(firebaseCommunicator.getPythonObjectForFirebaseDataAtLocation("/Teams"))
		self.matches = utils.makeMatchesFromDicts(firebaseCommunicator.getPythonObjectForFirebaseDataAtLocation("/Matches"))

	def updateTIMDsFromFirebase(self):
		self.TIMDs = utils.makeTIMDsFromDicts(firebaseCommunicator.getPythonObjectForFirebaseDataAtLocation("/TeamInMatchDatas"))

class CalculatedTeamData(object):
	"""The calculatedData for an FRC Team object"""
	def __init__(self, **args):
		super(CalculatedTeamData, self).__init__()
		self.firstPickAbility = None
		self.overallSecondPickAbility = None
		self.disabledPercentage = None
		self.incapacitatedPercentage = None
		self.predictedSeed = None
		self.actualSeed = None
		self.__dict__.update(args)

		
class Team(object):
	"""An FRC Team object"""
	def __init__(self, **args):
		super(Team, self).__init__()
		self.name = None
		self.number = None
		self.calculatedData = CalculatedTeamData()
		self.selectedImageUrl = None
		self.otherImageUrls = {
			 'not0' : None
		}
		self.pitCheesecakeAbility = None
		self.pitNotes = None
		self.pitOrganization = None
		self.pitNumberOfWheels = None
		self.pitProgrammingLanguage = None
		self.__dict__.update(args)


class CalculatedMatchData(object):
	"""docstring for CalculatedMatchData"""
	def __init__(self, **args):
		super(CalculatedMatchData, self).__init__()
		self.predictedRedScore = None
		self.predictedBlueScore = None
		self.sdPredictedRedScore = None
		self.sdPredictedBlueScore = None
		self.redWinChance = None
		self.redBreachChance = None
		self.redCaptureChance = None
		self.blueWinChance = None
		self.blueBreachChance = None
		self.blueCaptureChance = None
		self.predictedBlueRPs = None
		self.actualBlueRPs = None
		self.predictedRedRPs = None
		self.actualRedRPs = None		
		self.__dict__.update(args)


class Match(object):
	"""An FRC Match Object"""
	def __init__(self, **args):
		super(Match, self).__init__()
		self.number = None
		self.calculatedData = CalculatedMatchData()
		self.redAllianceTeamNumbers = None
		self.blueAllianceTeamNumbers = None
		self.redScore = None
		self.blueScore = None
		self.__dict__.update(args)
		
class TeamInMatchData(object):
	"""An FRC TeamInMatchData Object"""
	def __init__(self, **args):
		super(TeamInMatchData, self).__init__()
		
		self.calculatedData = CalculatedTeamInMatchData()
		self.teamNumber = None
		self.matchNumber = None
		self.scoutName = None
		self.superNotes = None
		self.__dict__.update(args)		

class CalculatedTeamInMatchData(object):
	"""docstring for CalculatedTeamInMatchData"""
	def __init__(self, **args):
		super(CalculatedTeamInMatchData, self).__init__()
		self.__dict__.update(args)

