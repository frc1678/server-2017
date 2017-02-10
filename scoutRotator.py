import pyrebase
import DataModel
import time
import SPR
import multiprocessing
import random
import time

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
testScouts = "ethan ben calvin kenny ryan peter shane".split()
scouts = "westley mx tim jesse sage alex janet livy gemma justin berin aiden rolland rachel zoe ayush jona angela kyle wesley".split()
SPR = SPR.ScoutPrecision()
#Note: set to true when starting to run and everyone is available, or the list of scouts on this file has been updated
#	   set to false when maintaining availability already in firebase, or leaving in scouts on firebase but not the list here
def resetAvailability():
	availability = {name: 1 for name in testScouts}
						#Note: change testScouts to scouts for actual use
	fb.child('availability').set(availability)

#If reset scouts is true, this makes firebase objects for 11 scouts (change 11 to 18 for actual use)
#Set to true if scouts in firebase do not exist, or there are the wrong number
#otherwise, set to false
def resetScouts():
	scouts = {'scout' + str(num) : {'currentUser': ''} for num in range(1,19)}
	fb.child('scouts').set(scouts)

def doThing(newMatchNumber):
	print 'Setting scouts for match ' + str(fb.child('currentMatchNum').get().val())
	if not newMatchNumber.get("data"): return
	currentMatchNum = int(newMatchNumber["data"])
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

def doThingStream():
	resetScouts()
	resetAvailability()
	#Once all of the scouts have logged onto tablets, it starts assignments and things
	while True:
		available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
		scoutRotatorDict = fb.child("scouts").get().val()
		scoutsWithNames = filter(lambda v: v.get('currentUser') != (None or ''), scoutRotatorDict.values())
		namesOfScouts = map(lambda v: v.get('currentUser'), scoutsWithNames)
		print available
		print namesOfScouts
		nameIsIn = True
		for name in namesOfScouts:
			nameIsIn = nameIsIn and (name in available)
		if nameIsIn:
			break
		time.sleep(1)
	fb.child("currentMatchNum").stream(doThing)

