import pyrebase
import DataModel
import SPR

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
testScouts = "a b c d e f g h i j k l".split()
scouts = "janet justin alex wesley kyle mx aiden westley katie jesse jack sage jon ayush sam evan mingyo zoe gemma carter".split()
SPR = SPR.ScoutPrecision()

#creates list of availability values in firebase for each scout
def resetAvailability():
	availability = {name: 1 for name in testScouts}
						#Note: change testScouts to scouts for actual use
	fb.child('availability').set(availability)

#creates firebase objects for 18 scouts
def resetScouts():
	scouts = {'scout' + str(num) : {'currentUser': '', 'scoutStatus': ''} for num in range(1,13)}
	fb.child('scouts').set(scouts)

def doSPRsAndAssignments(newMatchNumber):
	if newMatchNumber.get('data') == None: return
	print('Setting scouts for match ' + str(fb.child('currentMatchNum').get().val()))
	newMatchNumber = str(fb.child('currentMatchNum').get().val())
	scoutDict = fb.child("scouts").get().val()
	#gets the teams we need to scout for
	blueTeams = fb.child("Matches").child(newMatchNumber).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(newMatchNumber).get().val()['redAllianceTeamNumbers']
	#These next lines find and assign available scouts
	available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
	#Each scout is assigned to a robot in the next 2 lines
	SPR.calculateScoutPrecisionScores(fb.child("TempTeamInMatchDatas").get().val(), available)
	SPR.sprZScores()
	newAssignments = SPR.assignScoutsToRobots(available, redTeams + blueTeams, fb.child("scouts").get().val())
	#and it is put on firebase
	fb.child("scouts").update(newAssignments)

#Use this if tablets are assigned to scouts by the server, and then given to the correct scouts
def tabletHandoutStream():
	resetScouts()
	resetAvailability()
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)

#Use this if scouts sign in on tablets and the rotation starts when they each have one
def tabletLoginStream():
	resetScouts()
	resetAvailability()
	while True:
		scoutsAreIn = True
		available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
		scoutRotatorDict = fb.child("scouts").get().val()
		scoutsWithNames = filter(lambda v: v.get('currentUser') != (None or ''), scoutRotatorDict.values())
		namesOfScouts = map(lambda v: v.get('currentUser'), scoutsWithNames)
		for name in available:
			if name not in namesOfScouts:
				scoutsAreIn = False
		if scoutsAreIn:
			break
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)
