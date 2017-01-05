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

def doThing(newMatchNumber):
	currentMatchNum = newMatchNumber["data"]
	blueTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(str(currentMatchNum)).get().val()['redAllianceTeamNumbers']
	print redTeams, blueTeams

fb.child("currentMatchNum").stream(doThing)