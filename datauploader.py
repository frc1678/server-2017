from firebase import firebase as fb
import random
import time
class TeamInMatchData(object):
	"""An FRC TeamInMatchData Object"""
	def __init__(self, **args):
		super(TeamInMatchData, self).__init__()
		self.calculatedData = None
		self.teamNumber = None
		self.matchNumber = None
		self.scoutName = 'sammy'
		self.numGearsPlacedAuto = random.randint(0,5)
		self.didReachBaselineAuto = [True, False][random.randint(0, 1)]
		self.didPotentiallyConflictingAuto = [True, False][random.randint(0, 1)]
		self.numHoppersOpenedAuto = random.randint(0,5)
		self.numGearsPlacedTele = random.randint(0,5)
		self.numHoppersOpenedTele = random.randint(0,5)
		self.numGearGroundIntakesTele = random.randint(0,5)
		self.numGearLoaderIntakesTele = random.randint(0,5)
		self.didLiftoff = [True, False][random.randint(0, 1)]
		self.didStartDisabled = [True, False][random.randint(0, 1)]
		self.didBecomeIncapacitated = [True, False][random.randint(0, 1)]
		self.rankSpeed = random.randint(0,5)
		self.rankAgility = random.randint(0,5)
		self.rankGearControl = random.randint(0,5)
		self.rankBallControl = random.randint(0,5)
		self.rankDefense = random.randint(0,5)
		self.highShotTimesForBoilerAuto = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : 'key'
			}
		]
		self.lowShotTimesForBoilerAuto = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : 'key'
			}
		]
		self.highShotTimesForBoilerTele = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : 'key'
			}
		]
		self.lowShotTimesForBoilerTele = [
			{
				'time' : random.randint(0,5),
				'numShots' : random.randint(0,5),
				'position' : 'key'
			}
		]
		self.__dict__.update(args)

(superSecret, url) = ('93Ybz7MldpSj6HQHW1zb4ddcGGmpCMlNlOBoI9V3', 'https://scouting-2017-5f51c.firebaseio.com/')

auth = fb.FirebaseAuthentication(superSecret, "1678programming@gmail.com", True, True)

firebase = fb.FirebaseApplication(url, auth)
cm = 1
while True:
	match = firebase.get('/Matches', cm)
	for t in match["redAllianceTeamNumbers"] + match["blueAllianceTeamNumbers"]:
		timd = TeamInMatchData(teamNumber=t, matchNumber=cm)
		timdKey = str(t) + "Q" + str(cm)
		firebase.put('/TeamInMatchDatas', timdKey, timd.__dict__)
	cm += 1
	time.sleep(10)






