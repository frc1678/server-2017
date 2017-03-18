from firebase import firebase as fb
import random
import time
import DataModel

class CalculatedTeamInMatchData(object):
	"""docstring for CalculatedTeamInMatchData"""
	def __init__(self, **args):
		super(CalculatedTeamInMatchData, self).__init__()
		self.numRPs = random.randint(0, 4)
		self.liftoffAbility = random.randint(0, 50)
		self.numHighShotsTele = random.randint(0, 50)
		self.numHighShotsAuto = random.randint(0, 50)
		self.numLowShotsTele = random.randint(0, 50)
		self.numLowShotsAuto = random.randint(0, 50)
		self.numGearsPlacedTele = random.randint(0, 50)
		self.numGearsPlacedAuto = random.randint(0, 50)
		self.wasDisfunctional = bool(random.randint(0, 1))
		self.avgKeyShotTime = random.randint(0, 50)
		self.__dict__.update(args)

class TeamInMatchData(object):
	"""An FRC TeamInMatchData Object"""
	def __init__(self, **args):
		super(TeamInMatchData, self).__init__()
		self.calculatedData = CalculatedTeamInMatchData().__dict__
		self.teamNumber = args['teamNumber']
		self.matchNumber = args['matchNumber']
		self.scoutName = args['scoutName']
		self.numGearGroundIntakesTele = random.randint(0, 3)
		self.numGearLoaderIntakesTele = random.randint(0, 3)
		self.numGearsEjectedTele = random.randint(0, 3)
		self.numGearsFumbledTele = random.randint(0, 3)
		self.didReachBaselineAuto = bool(random.randint(0, 3))
		self.numHoppersOpenedAuto = random.randint(0, 3)
		self.numHoppersOpenedTele = random.randint(0, 3)
		self.didLiftoff = bool(random.randint(0, 3))
		self.didStartDisabled = bool(random.randint(0, 3))
		self.didBecomeIncapacitated = bool(random.randint(0, 3))
		self.rankSpeed = random.randint(0, 3)
		self.rankAgility = random.randint(0, 3)
		self.rankGearControl = random.randint(0, 3)
		self.rankBallControl = random.randint(0, 3)
		self.rankDefense = random.randint(0, 3)
		self.gearsPlacedByLiftAuto = {
			'lift1' : random.randint(0, 3),
			'lift2' : random.randint(0, 3),
			'lift3' : random.randint(0, 3)
		}
		self.gearsPlacedByLiftTele = {
			'lift1' : random.randint(0, 3),
			'lift2' : random.randint(0, 3),
			'lift3' : random.randint(0, 3)
		}
		self.highShotTimesForBoilerAuto = [
			{
				'time' : random.randint(0, 3),
				'numShots' : random.randint(0, 3),
				'position' : 'key'
			},
			{
				'time' : random.randint(0, 3),
				'numShots' : random.randint(0, 3),
				'position' : 'key'
			}
		]
		self.lowShotTimesForBoilerAuto = [
			{
				'time' : random.randint(0, 3),
				'numShots' : random.randint(0, 3),
				'position' : 'key'
			}
		]
		self.highShotTimesForBoilerTele = [
			{
				'time' : random.randint(0, 3),
				'numShots' : random.randint(0, 3),
				'position' : 'key'
			}
		]
		self.lowShotTimesForBoilerTele = [
			{
				'time' : random.randint(0, 3),
				'numShots' : random.randint(0, 3),
				'position' : 'key'
			}
		]
		self.__dict__.update(args)

class Match(object):
	"""An FRC Match Object"""
	def __init__(self, **args):
		super(Match, self).__init__()
		self.number = args['number']
		self.calculatedData = args['calculatedData']
		self.redAllianceTeamNumbers = args['redAllianceTeamNumbers']
		self.blueAllianceTeamNumbers = args['blueAllianceTeamNumbers']
		self.redDidStartAllRotors = bool(random.randint(0, 1))
		self.blueDidStartAllRotors = bool(random.randint(0, 1))
		self.redDidReachFortyKilopascals = bool(random.randint(0, 1))
		self.blueDidReachFortyKilopascals = bool(random.randint(0, 1))
		self.redScore = random.randint(0, 50)
		self.blueScore = random.randint(0, 50)
		self.foulPointsGainedRed = random.randint(0, 50)
		self.foulPointsGainedBlue = random.randint(0, 50)
		self.__dict__.update(args)

class CalculatedMatchData(object):
	"""docstring for CalculatedMatchData"""
	def __init__(self, **args):
		super(CalculatedMatchData, self).__init__()
		self.predictedRedScore = random.randint(0, 50)
		self.predictedBlueScore = random.randint(0, 50)
		self.sdPredictedRedScore = random.randint(0, 50)
		self.sdPredictedBlueScore = random.randint(0, 50)
		self.redWinChance = random.random()
		self.blueWinChance = random.random()
		self.predictedBlueRPs = random.random() * 4
		self.actualBlueRPs = random.random() * 4
		self.predictedRedRPs = random.random() * 4
		self.actualRedRPs =  random.random() * 4
		self.fortyKilopascalChanceRed = random.random()
		self.fortyKilopascalChanceBlue = random.random()
		self.allRotorsTurningChanceRed = random.random()
		self.allRotorsTurningChanceBlue = random.random()
		self.__dict__.update(args)

#(superSecret, url) = ('qVIARBnAD93iykeZSGG8mWOwGegminXUUGF2q0ee', 'https://1678-scouting-2016.firebaseio.com/')
(superSecret, url) = ('93Ybz7MldpSj6HQHW1zb4ddcGGmpCMlNlOBoI9V3', 'https://scouting-2017-5f51c.firebaseio.com/')

auth = fb.FirebaseAuthentication(superSecret, "1678programming@gmail.com", True, True)
testScouts = "a b c d e f g h i j k l m n o p q r".split()
testScouts = zip(testScouts, range(len(testScouts)))
firebase = fb.FirebaseApplication(url, auth)
cm = 1
while(True):
	match = firebase.get('/Matches', cm)
	m = Match(number = cm, redAllianceTeamNumbers = match['redAllianceTeamNumbers'], blueAllianceTeamNumbers = match['blueAllianceTeamNumbers'], calculatedData = CalculatedMatchData().__dict__)
	firebase.put('/Matches/', str(cm), m.__dict__)
	for t in match['redAllianceTeamNumbers'] + match['blueAllianceTeamNumbers']:
		for i in range(3):
			k = str(t) + "Q" + str(cm)
			firebase.put('/TempTeamInMatchDatas/', k + '-' + str(i), TeamInMatchData(teamNumber = t, matchNumber = cm, scoutName = testScouts[i]).__dict__)
	cm += 1
	time.sleep(4)
