import pyrebase
import DataModel
import time
from firebase import firebase as fir
import SPR
import multiprocessing
import random

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
testScouts = "arman Sam so asdf abhi fgh aScout anotherScout aThirdScout".split()
scouts = "Westley MX Tim Jesse Sage Alex Janet Livy Gemma Justin Berin Aiden Rolland Rachel Zoe Ayush Jona Angela Kyle Wesley".split()
SPR = SPR.ScoutPrecision()
resetAvailability = False
if resetAvailability:
	availability = {name: 1 for name in testScouts}
	fb.child('availability').set(availability)

def doThing(newMatchNumber):
	print newMatchNumber
	if not newMatchNumber.get("data"): return
	currentMatchNum = int(newMatchNumber["data"])
	blueTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['redAllianceTeamNumbers']
	available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
	SPR.calculateScoutPrecisionScores(fb.child("TempTeamInMatchDatas").get().val(), available)
	newAssignments = SPR.assignScoutsToRobots(available, redTeams + blueTeams, fb.child("scouts").get().val())
	fb.child("scouts").update(newAssignments)

fb.child("currentMatchNumber").stream(doThing)
