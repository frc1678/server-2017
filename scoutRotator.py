import pyrebase
import DataModel
import time
import SPR
import multiprocessing
import time

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
testScouts = "a b c d e f g h i j k l m n o p q r".split()
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

def doThing(newMatchNumber, update):
	print 'Setting scouts for match ' + str(fb.child('currentMatchNumber').get().val())
	if newMatchNumber.get("data") == None or not update: return
	currentMatchNum = int(newMatchNumber["data"])
	scoutDict = fb.child("scouts").get().val()
	[scoutDict[k].update({'mostRecentUser' : scoutDict[k].get('currentUser')}) for k in scoutDict.keys()]
	fb.child("scouts").update(scoutDict)
	#gets the teams we need to scout for
	blueTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['redAllianceTeamNumbers']
	#These next lines find and assign available scouts
	available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
	#Each scout is assigned to a robot in the next 2 lines
	SPR.calculateScoutPrecisionScores(fb.child("TempTeamInMatchDatas").get().val(), available)
	newAssignments = SPR.assignScoutsToRobots(available, redTeams + blueTeams, fb.child("scouts").get().val())	
	#and it is put on firebase
	fb.child("scouts").update(newAssignments)
	[fb.child("scouts").child("scout" + str(n)).update({'scoutStatus' : 'requested'}) for n in range(1,19)]

def emptyTIMDs():
	fb.child('TeamInMatchDatas').set({})

def simpleStream(update):
	# resetScouts()
	# resetAvailability()
	fb.child("currentMatchNumber").stream(lambda d: doThing(d, True))

