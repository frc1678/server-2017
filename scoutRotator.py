import pyrebase
import DataModel
import time
from firebase import firebase as fir
import SPR
import multiprocessing
import random

config = {
	"apiKey": "mykey",
	"authDomain": "1678-scouting-2016.firebaseapp.com",
	"databaseURL": "https://1678-scouting-2016.firebaseio.com/",
	"storageBucket": "1678-scouting-2016.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
scouts = []
SPR = SPR.ScoutPrecision()

def doThing(newMatchNumber):
	print newMatchNumber
	if not newMatchNumber.get("data"): return
	currentMatchNum = int(newMatchNumber["data"])
	blueTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['redAllianceTeamNumbers']
	available = [k for k, v in fb.child("available").get().val().items() if v]
	newAssignments = SPR.assignScoutsToRobots(scouts, available, redTeams + blueTeams, fb.child("scouts").get().val())
	fb.child("scouts").update(newAssignments)
	
fb.child("currentMatchNumber").stream(doThing)