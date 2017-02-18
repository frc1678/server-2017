import pyrebase
import DataModel
import SPR
import multiprocessing

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
testScouts = "scout1 scout10 scout11 scout12 scout13 scout14 scout15 scout16 scout17 scout18 scout2 scout3".split()
scouts = "janet justin alex wesley kyle mx aiden westley katie jesse jack sage jon ayush sam evan mingyo zoe gemma carter".split()
SPR = SPR.ScoutPrecision()
#creates list of availability values in firebase for each scout
def resetAvailability():
	availability = {name: 1 for name in testScouts}
						#Note: change testScouts to scouts for actual use
	fb.child('availability').set(availability)

#creates firebase objects for 18 scouts
def resetScouts():
	scouts = {'scout' + str(num) : {'currentUser': ''} for num in range(1,13)}
	fb.child('scouts').set(scouts)

def doSPRsAndAssignments(newMatchNumber):
	print 'Setting scouts for match ' + str(fb.child('currentMatchNum').get().val())
	newMatchNumber = str(fb.child('currentMatchNum').get().val())
	scoutDict = fb.child("scouts").get().val()
	#gets the teams we need to scout for
	blueTeams = fb.child("Matches").child(newMatchNumber).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(newMatchNumber).get().val()['redAllianceTeamNumbers']
	#These next lines find and assign available scouts
	available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
	#Each scout is assigned to a robot in the next 2 lines
	SPR.calculateScoutPrecisionScores(fb.child("TempTeamInMatchDatas").get().val(), available)
	# print SPR.sprs
	newAssignments = SPR.assignScoutsToRobots(available, redTeams + blueTeams, fb.child("scouts").get().val())
	#and it is put on firebase
	fb.child("scouts").update(newAssignments)

def assignmentStream():
	#resetScouts()
	#resetAvailability()
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)
