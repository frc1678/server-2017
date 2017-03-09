import utils
import json
import pdb
import datetime
import numpy as np
import pyrebase

class PyrebaseCommunicator(object):
	"""docstring for PyrebaseCommunicator"""
	def __init__(self):
		super(PyrebaseCommunicator, self).__init__()
		self.JSONmatches = []
		self.JSONteams = []
		self.firebase = None
		self.fbStorage = None
		self.url = 'scouting-2017-5f51c'
		# self.url = '1678-scouting-2016'

	def initializeFirebase(self):
		config = {
			"apiKey": "mykey",
			"authDomain": self.url + ".firebaseapp.com",
			"databaseURL": "https://" + self.url + ".firebaseio.com/",
			"storageBucket": self.url + ".appspot.com"
		}
		app = pyrebase.initialize_app(config)
		self.firebase = app.database()
		self.fbStorage = app.storage()

	def updateFirebaseWithTeam(self, team):
		print(str(team.number) + ",",)
		teamDict = utils.makeDictFromTeam(team)
		firebase.child("Teams").child(team.number).set(teamDict)

	def updateFirebaseWithMatch(self, match):
		print(str(match.number) + ",",)
		matchDict = utils.makeDictFromMatch(match)
		matchDict["blueAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["blueAllianceTeamNumbers"])
		matchDict["redAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["redAllianceTeamNumbers"])
		self.firebase.child("Matches").child(match.number).set(matchDict)

	def updateFirebaseWithTIMD(self, timd):
		timdDict = utils.makeDictFromTIMD(timd)
		print(str(timd.teamNumber) + "Q" + str(timd.matchNumber) + "," ,)
		firebase.child("TeamInMatchDatas").child(str(timd.teamNumber) + "Q" + str(timd.matchNumber)).set(timdDict)

	def addCalculatedTeamDataToFirebase(self, team):
		print("Writing team " + str(team.number) + " to Firebase...")
		calculatedTeamDataDict = utils.makeDictFromCalculatedData(team.calculatedData)
		try:
			self.firebase.child("Teams").child(team.number).child("calculatedData").set(calculatedTeamDataDict)
		except:
			pass

	def addCalculatedTIMDataToFirebase(self, timd):
		print("Writing team " + str(timd.teamNumber) + " in match " + str(timd.matchNumber) + " to Firebase...")
		calculatedTIMDataDict = utils.makeDictFromCalculatedData(timd.calculatedData)
		key = str(timd.teamNumber) + "Q" + str(timd.matchNumber)
		try:
			self.firebase.child("TeamInMatchDatas").child(key).child("calculatedData").set(calculatedTIMDataDict)
		except:
			pass

	def addCalculatedMatchDataToFirebase(self, match):
		print("Writing match " + str(match.number) + " to Firebase...")
		calculatedMatchDataDict = utils.makeDictFromCalculatedData(match.calculatedData)
		FBLocation = "/Matches/" + str(match.number)
		try:
			self.firebase.child("Matches").child(match.number).child("calculatedData").set(calculatedMatchDataDict)
		except:
			pass

	def addTeamsToFirebase(self):
		print("\nDoing Teams...")
		map(lambda t: self.updateFirebaseWithTeam(utils.setDataForTeam(t)), self.JSONteams)

	def addMatchesToFirebase(self):
		print("\nDoing Matches...")
		matches = filter(lambda m: m["comp_level"] == 'qm', self.JSONmatches)
		map(lambda m: self.updateFirebaseWithMatch(utils.setDataForMatch(m)), matches)

	def addTIMDsToFirebase(self, matches):
		#gets all team numbers in a given match and updates firebase with the corresponding TIMD
		print("\nDoing TIMDs...")
		timdFunc = lambda t, m: self.updateFirebaseWithTIMD(utils.makeTIMDFromTeamNumberAndMatchNumber(t, m.number))
		addTIMD = lambda m: map(lambda t: timdFunc(t, m), m.redAllianceTeamNumbers + m.blueAllianceTeamNumbers)
		map(addTIMD, matches)

	def cacheFirebase(self):
		try:
			data = dict(self.firebase.get().val())
			now = str(datetime.datetime.now())
			with open("./CachedFirebases/" + now + '.json', 'w+') as f:
				json.dump(data, f)
		except:
			pass

	def addCompInfoToFirebase(self):
		#Doing these keys manually so less clicking in firebase is better and because just easier
		self.firebase.child("code").set("cama")

	def wipeDatabase(self):
		map(utils.printWarningForSeconds, range(10, 0, -1))
		print("\nWARNING: Wiping Firebase...")
		self.firebase.remove()

	def getPythonObjectForFirebaseDataAtLocation(self, location):
		return utils.makeASCIIFromJSON(self.firebase.child(location).get().val())

	def sendExport(self, fileName):
		now = str(datetime.datetime.now())
		filePath = './' + fileName
		self.fbStorage.child("Exports").child(fileName).put(filePath)
		return self.firebase.child(location).get().val()

	def addCurrentMatchToFirebase(self):
		self.firebase.child("currentMatchNum").set(1)
