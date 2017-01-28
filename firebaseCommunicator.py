import DataModel
import utils
import json
import unicodedata
import requests
from os import listdir
import pdb
import math
import datetime
import pyrebase

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

firebase = pyrebase.initialize_app(config)
firebase = firebase.database()

class FirebaseCommunicator(object):
	"""docstring for FirebaseCommunicator"""
	def __init__(self, competition):
		super(FirebaseCommunicator, self).__init__()
		self.JSONmatches = []
		self.JSONteams = []
		self.competition = competition

	def updateFirebaseWithTeam(self, team):
		print str(team.number) + ",",
		teamDict = utils.makeDictFromTeam(team)
		FBLocation = "Teams"
		result = firebase.child(FBLocation).set(teamDict)

	def updateFirebaseWithMatch(self, match):
		print str(match.number) + ",",
		matchDict = utils.makeDictFromMatch(match)
		FBLocation = "Matches"
		matchDict["blueAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["blueAllianceTeamNumbers"])
		matchDict["redAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["redAllianceTeamNumbers"])
		result = firebase.child(FBLocation).set(matchDict)

	def updateFirebaseWithTIMD(self, timd):
		timdDict = utils.makeDictFromTIMD(timd)
		FBLocation = "TeamInMatchDatas"
		print(str(timd.teamNumber) + "Q" + str(timd.matchNumber)) + "," ,
		result = firebase.child(FBLocation).child(str(timd.teamNumber) + "Q" + str(timd.matchNumber)).set(timdDict)

	def addCalculatedTeamDataToFirebase(self, team):
		print "Writing team " + str(team.number) + " to Firebase..."
		calculatedTeamDataDict = utils.makeDictFromCalculatedData(team.calculatedData)
		FBLocation = "/Teams/" + str(team.number)
		calculatedDataDict = {'calculatedData', calculatedTeamDataDict}
		try: firebase.child(FBLocation).set(calculatedDataDict)
		except requests.exceptions.RequestException as e: print e

	def addCalculatedTIMDataToFirebase(self, timd):
		print "Writing team " + str(timd.teamNumber) + " in match " + str(timd.matchNumber) + " to Firebase..."
		calculatedTIMDataDict = utils.makeDictFromCalculatedData(timd.calculatedData)
		FBLocation = "/TeamInMatchDatas/" + str(timd.teamNumber) + "Q" + str(timd.matchNumber)
		calcDict = {'calculatedData', calculatedTIMDataDict}
		try: firebase.child(FBLocation).set(calcDict)
		except requests.exceptions.RequestException as e: print e

	def addCalculatedMatchDataToFirebase(self, match):
		print "Writing match " + str(match.number) + " to Firebase..."
		calculatedMatchDataDict = utils.makeDictFromCalculatedData(match.calculatedData)
		FBLocation = "/Matches/" + str(match.number)
		dataCalc = {'calculatedData', calculatedMatchDataDict}
		try: firebase.child(FBLocation).set(dataCalc)
		except requests.exceptions.RequestException as e: print e

	def addTeamsToFirebase(self):
		print "\nDoing Teams..."
		map(lambda t: self.updateFirebaseWithTeam(utils.setDataForTeam(t)), self.JSONteams)

	def addMatchesToFirebase(self):
		print "\nDoing Matches..."
		matches = filter(lambda m: m["comp_level"] == 'qm', self.JSONmatches)
		map(lambda m: self.updateFirebaseWithMatch(utils.setDataForMatch(m)), matches)

	def addTIMDsToFirebase(self, matches): #addTIMD function get all team numbers in a given match and updates firebase with the
		print "\nDoing TIMDs..."																				#corresponding TIMD
		timdFunc = lambda t, m: self.updateFirebaseWithTIMD(utils.makeTIMDFromTeamNumberAndMatchNumber(t, m.number))
		addTIMD = lambda m: map(lambda t: timdFunc(t, m), m.redAllianceTeamNumbers + m.blueAllianceTeamNumbers)
		map(addTIMD, matches)


	def addCompInfoToFirebase(self): #Doing these keys manually so less clicking in firebase is better and because just easier
		FBLocation = "/"
		code = {'code', self.competition.code}
		currentMatchNum = {'currentMatchNum', self.competition.currentMatchNum}
		result = firebase.child(FBLocation).set(code)
		result = firebase.child(FBLocation).set(currentMatchNum)

	def wipeDatabase(self):
		map(utils.printWarningForSeconds, range(10, 0, -1))
		print "\nWARNING: Wiping Firebase..."
		FBLocation = "/"
		firebase.child(FBLocation).remove()

	def cacheFirebase(self):
		while True:
			try:
				data = json.dumps(firebase.child("/").get().val())
				now = str(datetime.datetime.now())
				with open("./CachedFirebases/" + now + '.json', 'w') as f:
					f.write(data)
					f.close()
					break
			except: pass

def getPythonObjectForFirebaseDataAtLocation(location):
	return utils.makeASCIIFromJSON((firebase.child(location).get().val()))