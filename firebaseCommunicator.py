import utils
import json
import datetime
import numpy as np
import pyrebase

class PyrebaseCommunicator(object):
	"""docstring for PyrebaseCommunicator"""
	def __init__(self):
		super(PyrebaseCommunicator, self).__init__()
		self.JSONmatches = []
		self.JSONteams = []
		# self.url = 'scouting-2017-5f51c'
		# self.url = 'jesus-is-bread'
		self.url = '1678-scouting-2016'
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
		self.firebase.child("Teams").child(team.number).set(teamDict)

	def updateFirebaseWithMatch(self, match):
		print(str(match.number) + ",",)
		matchDict = utils.makeDictFromMatch(match)
		matchDict["blueAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["blueAllianceTeamNumbers"])
		matchDict["redAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["redAllianceTeamNumbers"])
		self.firebase.child("Matches").child(match.number).set(matchDict)

	def updateFirebaseWithTIMD(self, timd):
		timdDict = utils.makeDictFromTIMD(timd)
		print(str(timd.teamNumber) + "Q" + str(timd.matchNumber) + "," ,)
		self.firebase.child("TeamInMatchDatas").child(str(timd.teamNumber) + "Q" + str(timd.matchNumber)).set(timdDict)

	def addCalculatedTeamDataToFirebase(self, team):
		calculatedTeamDataDict = utils.makeDictFromCalculatedData(team.calculatedData)
		FBLocation = str(team.number) + '/calculatedData/'
		return {FBLocation : calculatedTeamDataDict}

	def addCalculatedTIMDataToFirebase(self, timd):
		calculatedTIMDataDict = utils.makeDictFromCalculatedData(timd.calculatedData)
		FBLocation = str(timd.teamNumber) + "Q" + str(timd.matchNumber) + '/calculatedData/'
		return {FBLocation : calculatedTIMDataDict}

	def addCalculatedMatchDataToFirebase(self, match):
		calculatedMatchDataDict = utils.makeDictFromCalculatedData(match.calculatedData)
		FBLocation = str(match.number) + '/calculatedData/'
		return {FBLocation : calculatedMatchDataDict}

	def addCalculatedTeamDatasToFirebase(self, teams):
		firebaseDict = {}
		[firebaseDict.update(self.addCalculatedTeamDataToFirebase(team)) for team in teams]
		print("Uploading Teams to Firebase...")
		self.firebase.child('Teams').update(firebaseDict)		

	def addCalculatedMatchDatasToFirebase(self, matches):
		firebaseDict = {}
		[firebaseDict.update(self.addCalculatedMatchDataToFirebase(match)) for match in matches]
		print("Uploading Matches to Firebase...")
		self.firebase.child('Matches').update(firebaseDict)

	def addCalculatedTIMDatasToFirebase(self, timds):
		firebaseDict = {}
		[firebaseDict.update(self.addCalculatedTIMDataToFirebase(timd)) for timd in timds]
		print("Uploading TIMDs to Firebase...")
		self.firebase.child('TeamInMatchDatas').update(firebaseDict)

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

	def addCurrentMatchToFirebase(self):
		self.firebase.child("currentMatchNum").set(1)


