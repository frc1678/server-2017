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
		self.wasDisfunctional = random.randint(0, 50)
		self.avgKeyShotTime = random.randint(0, 50)
		self.__dict__.update(args)

class TeamInMatchData(object):
	"""An FRC TeamInMatchData Object"""
	def __init__(self, **args):
		super(TeamInMatchData, self).__init__()
		# self.calculatedData = DataModel.CalculatedTeamInMatchData()
		self.teamNumber = args['teamNumber']
		self.matchNumber = args['matchNumber']
		self.scoutName = 'sammy'	
		self.numHoppersOpenedTele = random.randint(0,5)
		self.numGearGroundIntakesTele = random.randint(0,5)
		self.numGearLoaderIntakesTele = random.randint(0,5)
		self.numGearsEjectedAuto = random.randint(0,5)
		self.numGearsEjectedTele = random.randint(0,5)
		self.numGearsFumbledAuto = random.randint(0,5)
		self.numGearsFumbledTele = random.randint(0,5)
		self.didReachBaselineAuto = bool(random.randint(0,5))
		self.didPotentiallyConflictingAuto = bool(random.randint(0,5))
		self.numHoppersOpenedAuto = random.randint(0,5)
		self.didLiftoff = bool(random.randint(0,5))
		self.didStartDisabled = bool(random.randint(0,5))
		self.didBecomeIncapacitated = bool(random.randint(0,5))
		self.rankSpeed = random.randint(0,4)
		self.rankAgility = random.randint(0,4)
		self.rankGearControl = random.randint(0,4)
		self.rankBallControl = random.randint(0,4)
		self.rankDefense = random.randint(0,4)
		self.gearsPlacedByLiftAuto = {
			'lift1' : random.randint(0,5),
			'lift2' : random.randint(0,5),
			'lift3' : random.randint(0,5) 
		}
		self.gearsPlacedByLiftTele = {
			'lift1' : random.randint(0,5),
			'lift2' : random.randint(0,5),
			'lift3' : random.randint(0,5) 
		}	
		self.highShotTimesForBoilerAuto = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : random.randint(0,5)
			}
		]
		self.lowShotTimesForBoilerAuto = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : random.randint(0,5)
			}
		]
		self.highShotTimesForBoilerTele = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : random.randint(0,5)
			}
		]
		self.lowShotTimesForBoilerTele = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : random.randint(0,5)
			}
		]
		self.__dict__.update(args)

class Match(object):
	"""An FRC Match Object"""
	def __init__(self, **args):
		super(Match, self).__init__()
		self.number = args['number']
		# self.calculatedData = CalculatedMatchData()
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


(superSecret, url) = ('93Ybz7MldpSj6HQHW1zb4ddcGGmpCMlNlOBoI9V3', 'https://scouting-2017-5f51c.firebaseio.com/')

auth = fb.FirebaseAuthentication(superSecret, "1678programming@gmail.com", True, True)

firebase = fb.FirebaseApplication(url, auth)
cm = 18
while True:
	match = firebase.get('/Matches', cm)
	m = Match(number=cm,redAllianceTeamNumbers=match['redAllianceTeamNumbers'],blueAllianceTeamNumbers=match['blueAllianceTeamNumbers'])
	firebase.put('/Matches/', str(cm), m.__dict__)
	# for t in match['redAllianceTeamNumbers'] + match['blueAllianceTeamNumbers']:
		# k = str(t) + "Q" + str(cm)
		# firebase.put('/TeamInMatchDatas', k, TeamInMatchData(teamNumber=t, matchNumber=cm).__dict__)
		# firebase.put('/TeamInMatchDatas/' + k, 'calculatedData', CalculatedTeamInMatchData().__dict__)
	cm += 1
	time.sleep(7)






