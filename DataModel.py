import firebaseCommunicator
import utils

#creates classes with keys which correspond to the data points collected and calculated by our scouting

class Competition(object):
	'''docstring for Competition'''
	def __init__(self, PBC):
		super(Competition, self).__init__()
		self.code = ''
		self.teams = []
		self.matches = []
		self.TIMDs = []
		self.PBC = PBC
		self.currentMatchNum = 0
	def updateTeamsAndMatchesFromFirebase(self):
		self.teams = utils.makeTeamsFromDicts(self.PBC.getPythonObjectForFirebaseDataAtLocation('Teams'))
		self.matches = utils.makeMatchesFromDicts(self.PBC.getPythonObjectForFirebaseDataAtLocation('Matches'))
		self.teams = utils.makeTeamsFromDicts(self.PBC.getPythonObjectForFirebaseDataAtLocation('Teams'))
		self.matches = utils.makeMatchesFromDicts(self.PBC.getPythonObjectForFirebaseDataAtLocation('Matches'))

	def updateTIMDsFromFirebase(self):
		self.TIMDs = utils.makeTIMDsFromDicts(self.PBC.getPythonObjectForFirebaseDataAtLocation('TeamInMatchDatas'))

class CalculatedTeamData(object):
	'''c'''
	def __init__(self, **args):
		#initializes actual calculated team data
		super(CalculatedTeamData, self).__init__()
		self.firstPickAbility = None
		self.disabledPercentage = None
		self.incapacitatedPercentage = None
		self.predictedSeed = None
		self.actualSeed = None
		self.predictedNumRPs = None
		self.actualNumRPs = None
		self.avgHighShotsTele = None
		self.avgLowShotsTele = None
		self.avgHighShotsAuto = None
		self.avgLowShotsAuto = None
		self.avgGearsPlacedAuto = None
		self.avgGearsPlacedTele = None
		self.avgGearsEjectedTele = None
		self.avgGearsFumbledTele = None
		self.avgGearLoaderIntakesTele = None
		self.avgGearGroundIntakesTele = None
		self.avgGearsPlacedByLiftAuto =  {
			'allianceWall' : None,
			'hpStation' : None,
			'boiler' : None
		}
		self.avgGearsPlacedByLiftTele =  {
			'allianceWall' : None,
			'hpStation' : None,
			'boiler' : None
		}
		self.avgHoppersOpenedAuto = None
		self.avgHoppersOpenedTele = None
		self.avgLiftoffTime = None
		self.sdGearsPlacedTele = None
		self.sdGearsPlacedAuto = None
		self.sdHighShotsAuto = None
		self.sdHighShotsTele = None
		self.sdLowShotsAuto = None
		self.sdLowShotsTele = None
		self.avgKeyShotTime = None
		self.avgHopperShotTime = None
		self.avgAgility = None
		self.avgSpeed = None
		self.avgBallControl = None
		self.avgGearControl = None
		self.avgDefense = None
		self.avgDrivingAbility = None
		self.liftoffAbility = None
		self.sdLiftoffAbility = None
		self.liftoffPercentage = None
		self.disfunctionalPercentage = None
		self.firstPickRotorBonusChance = None
		self.autoShootingPositions = None
		self.gearScoringPositionsAuto = None
		self.gearAbility = None
		self.RScoreAgility = None
		self.RScoreDefense = None
		self.RScoreSpeed = None
		self.RScoreBallControl = None
		self.RScoreGearControl = None
		self.RScoreDrivingAbility = None
		self.allRotorsAbility = None
		self.lfmDisabledPercentage = None
		self.lfmIncapacitatedPercentage = None
	  	self.lmfAvgGearsPlacedAuto = None
	  	self.lfmAvgHighShotsAuto = None
	  	self.lfmAvgLowShotsAuto = None
	  	self.lfmBaselineReachedPercentage = None
	  	self.lfmAvgGearsPlacedTele = None
	  	self.lfmAvgGearLoaderIntakesTele = None
	  	self.lfmAvgHighShotsTele = None
	  	self.lfmAvgLowShotsTele = None
	  	self.lfmAvgKeyShotTime = None
	  	self.lfmAvgLiftoffTime = None
	  	self.lfmLiftoffPercentage = None
	  	self.lfmAvgAgility = None
	  	self.lfmAvgSpeed = None
	  	self.lfmAvgBallControl = None
	  	self.lfmAvgGearControl = None
	  	self.lfmAvgDefense = None
		self.__dict__.update(args) #DON'T DELETE THIS FOR ANY CLASS

class Team(object):
	'''FRC Team Object'''
	def __init__(self, **args):
		#initializes variables for each team
		super(Team, self).__init__()
		self.name = None
		self.number = None
		self.calculatedData = CalculatedTeamData()
		self.numMatchesPlayed = None
		self.pitSelectedImageName = None
		self.pitAllImageURLs = {}
		self.pitAvailableWeight = None
		self.pitDriveTrain = None
		self.pitCheesecake = None
		self.pitProgrammingLanguage = None
		self.__dict__.update(args)

class CalculatedMatchData(object):
	'''docstring for CalculatedMatchData'''
	def __init__(self, **args):
		#initializes actual calculated match data
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
	'''An FRC Match Object'''
	def __init__(self, **args):
		#initializes match object
		super(Match, self).__init__()
		self.number = None
		self.calculatedData = CalculatedMatchData()
		self.redAllianceTeamNumbers = None
		self.blueAllianceTeamNumbers = None
		self.numRotorsSpinningRedAuto = None
		self.numRotorsSpinningRedTele = None
		self.numRotorsSpinningBlueAuto = None
		self.numRotorsSpinningBlueTele = None
		self.blueDidStartAllRotors = None
		self.redDidReachFortyKilopascals = None
		self.blueDidReachFortyKilopascals = None
		self.redScore = None
		self.blueScore = None
		self.foulPointsGainedRed = None
		self.foulPointsGainedBlue = None
		self.__dict__.update(args)

class CalculatedTeamInMatchData(object):
	'''docstring for CalculatedTeamInMatchData'''
	def __init__(self, **args):
		#initializes actual CalculatedTIMDs
		super(CalculatedTeamInMatchData, self).__init__()
		self.numRPs = None
		self.liftoffAbility = None
		self.numHighShotsTele = None
		self.numHighShotsAuto = None
		self.numLowShotsTele = None
		self.numLowShotsAuto = None
		self.numGearsPlacedTele = None
		self.numGearsPlacedAuto = None
		self.wasDisfunctional = None
		self.avgKeyShotTime = None
		self.avgHopperShotTime = None
		self.drivingAbility = None
		self.gearAbility = None
		self.disfunctionalPercentage = None
		self.__dict__.update(args)

class TeamInMatchData(object):
	'''An FRC TeamInMatchData Object'''
	def __init__(self, **args):
		#initializes actual TIMDs
		super(TeamInMatchData, self).__init__()
		self.calculatedData = CalculatedTeamInMatchData()
		self.teamNumber = None
		self.matchNumber = None
		self.scoutName = None
		self.superNotes = None
		self.numHoppersOpenedTele = None
		self.numGearGroundIntakesTele = None
		self.numGearLoaderIntakesTele = None
		self.numGearsEjectedTele = None
		self.numGearsFumbledTele = None
		self.numHoppersOpenedAuto = None
		self.didLiftoff = None
		self.liftoffTime = None
		self.didStartDisabled = None
		self.didBecomeIncapacitated = None
		self.rankSpeed = None
		self.rankAgility = None
		self.rankGearControl = None
		self.rankBallControl = None
		self.rankDefense = None
		self.gearsPlacedByLiftAuto = {
			'allianceWall' : None,
			'hpStation' : None,
			'boiler' : None
		}
		self.gearsPlacedByLiftTele = {
			'allianceWall' : None,
			'hpStation' : None,
			'boiler' : None
		}
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
