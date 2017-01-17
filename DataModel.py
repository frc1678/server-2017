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
		self.avgHighShotsTele = None
		self.avgLowShotsTele = None
		self.avgHighShotsAuto = None
		self.avgLowShotsAuto = None
		self.avgGearsPlacedAuto = None
		self.avgGearsPlacedTele = None
		self.sdGearsPlacedTele = None
		self.sdGearsPlacedAuto = None
		self.sdHighShotsAuto = None
		self.sdHighShotsTele = None
		self.sdLowShotsAuto = None
		self.sdLowShotsTele = None
		self.avgKeyShotTime = None
		self.avgAgility = None
		self.avgSpeed = None
		self.avgBallControl = None
		self.avgGearControl = None
		self.avgDefense = None
		self.liftoffAbility = None
		self.sdLiftoffAbility = None
		self.liftoffPercentage = None
		self.baselineReachedPercentage = None
		self.__dict__.update(args)

class Team(object):
	"""An FRC Team object"""
	def __init__(self, **args):
		super(Team, self).__init__()
		self.name = None
		self.number = None
		self.calculatedData = CalculatedTeamData()
		self.pitSelectedImageUrl = None
		self.pitOtherImageUrls = {
			 'not0' : None
		}
		self.pitAvailableWeight = None
		self.pitNotes = None
		self.pitOrganization = None
		self.pitDidTankTread = None
		self.pitCheesecake = None
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
		self.blueWinChance = None
		self.predictedBlueRPs = None
		self.actualBlueRPs = None
		self.predictedRedRPs = None
		self.actualRedRPs = None
		self.fortyKilopascalChanceRed = None
		self.fortyKilopascalChanceBlue = None
		self.allRotorsTurningChanceRed = None
		self.allRotorsTurningChanceBlue = None
		self.__dict__.update(args)


class Match(object):
	"""An FRC Match Object"""
	def __init__(self, **args):
		super(Match, self).__init__()
		self.number = None
		self.calculatedData = CalculatedMatchData()
		self.redAllianceTeamNumbers = None
		self.blueAllianceTeamNumbers = None
		self.redDidStartAllRotors = None
		self.blueDidStartAllRotors = None
		self.redDidReachFortyKilopascals = None
		self.blueDidReachFortyKilopascals = None
		self.redScore = None
		self.blueScore = None
		self.foulPointsGainedRed = None
		self.foulPointsGainedBlue = None
		self.__dict__.update(args)

class TeamInMatchData(object):
	"""An FRC TeamInMatchData Object"""
	def __init__(self, **args):
		super(TeamInMatchData, self).__init__()
		self.calculatedData = CalculatedTeamInMatchData()
		self.teamNumber = None
		self.matchNumber = None
		self.scoutName = None
		self.numGearsPlacedAuto = None
		self.didReachBaselineAuto = None
		self.didPotentiallyConflictingAuto = None
		self.numHoppersOpenedAuto = None
		self.numGearsPlacedTele = None
		self.numHoppersOpenedTele = None
		self.numGearGroundIntakesTele = None
		self.numGearLoaderIntakesTele = None
		self.numGearsEjectedAuto = None
		self.numGearsEjectedTele = None
		self.numGearsFumbledAuto = None
		self.numGearsFumbledTele = None
		self.didLiftoff = None
		self.didStartDisabled = None
		self.didBecomeIncapacitated = None
		self.rankSpeed = None
		self.rankAgility = None
		self.rankGearControl = None
		self.rankBallControl = None
		self.rankDefense = None
		self.highShotTimesForBoilerAuto = [
			{
				'time' : None,
				'numShots' : None,
				'position' : None
			}
		]
		self.lowShotTimesForBoilerAuto = [
			{
				'time' : None,
				'numShots' : None,
				'position' : None
			}
		]
		self.highShotTimesForBoilerTele = [
			{
				'time' : None,
				'numShots' : None,
				'position' : None
			}
		]
		self.lowShotTimesForBoilerTele = [
			{
				'time' : None,
				'numShots' : None,
				'position' : None
			}
		]
		self.__dict__.update(args)

class CalculatedTeamInMatchData(object):
	"""docstring for CalculatedTeamInMatchData"""
	def __init__(self, **args):
		super(CalculatedTeamInMatchData, self).__init__()
		self.liftoffAbility = None
		self.numHighShotsTele = None
		self.numHighShotsAuto = None
		self.numLowShotsTele = None
		self.numLowShotsAuto = None
		self.__dict__.update(args)


