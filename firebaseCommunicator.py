import DataModel
import utils
import json
from firebase import firebase as fb
import unicodedata
import requests
from os import listdir
import pdb
import math
import datetime


# (superSecret, url) = ('j1r2wo3RUPMeUZosxwvVSFEFVcrXuuMAGjk6uPOc', 'https://1678-dev-2016.firebaseio.com/')
#(superSecret, url) = ('hL8fStivTbHUXM8A0KXBYPg2cMsl80EcD7vgwJ1u', 'https://1678-dev2-2016.firebaseio.com/')
#(superSecret, url) = ('AEduO6VFlZKD4v10eW81u9j3ZNopr5h2R32SPpeq', 'https://1678-dev3-2016.firebaseio.com/')
#(superSecret, url) = ('IMXOxXD3FjOOUoMGJlkAK5pAtn89mGIWAEnaKJhP', 'https://1678-strat-dev-2016.firebaseio.com/')
# (superSecret, url) = ('lGufYCifprPw8p1fiVOs7rqYV3fswHHr9YLwiUWh', 'https://1678-extreme-testing.firebaseio.com/') 
(superSecret, url) = ('qVIARBnAD93iykeZSGG8mWOwGegminXUUGF2q0ee', 'https://1678-scouting-2016.firebaseio.com/') 


auth = fb.FirebaseAuthentication(superSecret, "1678programming@gmail.com", True, True)

firebase = fb.FirebaseApplication(url, auth)

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
		FBLocation = "/Teams"
		result = firebase.put(FBLocation, team.number, teamDict)

	def updateFirebaseWithMatch(self, match):
		print str(match.number) + ",",
		matchDict = utils.makeDictFromMatch(match)
		FBLocation = "/Matches"
		matchDict["blueAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["blueAllianceTeamNumbers"])
		matchDict["redAllianceTeamNumbers"] = map(lambda n: int(n.replace('frc', '')), matchDict["redAllianceTeamNumbers"])
		result = firebase.put(FBLocation, match.number, matchDict)

	def updateFirebaseWithTIMD(self, timd):
		timdDict = utils.makeDictFromTIMD(timd)
		FBLocation = "/TeamInMatchDatas"
		print(str(timd.teamNumber) + "Q" + str(timd.matchNumber)) + "," ,
		result = firebase.put(FBLocation, str(timd.teamNumber) + "Q" + str(timd.matchNumber), timdDict)

	def addCalculatedTeamDataToFirebase(self, team):
		print "Writing team " + str(team.number) + " to Firebase..."
		calculatedTeamDataDict = utils.makeDictFromCalculatedData(team.calculatedData)
		FBLocation = "/Teams/" + str(team.number) 
		try: firebase.put(FBLocation, 'calculatedData', calculatedTeamDataDict)
		except requests.exceptions.RequestException as e: print e

	def addCalculatedTIMDataToFirebase(self, timd):
		print "Writing team " + str(timd.teamNumber) + " in match " + str(timd.matchNumber) + " to Firebase..."
		calculatedTIMDataDict = utils.makeDictFromCalculatedData(timd.calculatedData)
		FBLocation = "/TeamInMatchDatas/" + str(timd.teamNumber) + "Q" + str(timd.matchNumber)
		try: firebase.put(FBLocation, 'calculatedData', calculatedTIMDataDict)
		except requests.exceptions.RequestException as e: print e
	
	def addCalculatedMatchDataToFirebase(self, match):
		print "Writing match " + str(match.number) + " to Firebase..."
		calculatedMatchDataDict = utils.makeDictFromCalculatedData(match.calculatedData)
		FBLocation = "/Matches/" + str(match.number)
		try: firebase.put(FBLocation, 'calculatedData', calculatedMatchDataDict)
		except requests.exceptions.RequestException as e: print e

	def addTeamsToFirebase(self): 
		print "\nDoing Teams..."
		map(lambda t: self.updateFirebaseWithTeam(utils.setDataForTeam(t)), self.JSONteams)
		
	def addMatchesToFirebase(self):
		print "\nDoing Matches..."
		matches = filter(lambda m: m["comp_level"] == 'qm', self.JSONmatches)
		map(lambda m: self.updateFirebaseWithMatch(utils.setDataForMatch(m)), matches)

	def addScorelessMatchesToFirebase(self):
		print "\nDoing Matches..."
		matches = filter(lambda m: m["comp_level"] == 'qm', self.JSONmatches)
		map(lambda m: self.updateFirebaseWithMatch(utils.setDataForMatch(m, True)), matches)
		

	def addTIMDsToFirebase(self, matches): #addTIMD function get all team numbers in a given match and updates firebase with the 
		print "\nDoing TIMDs..."																				#corresponding TIMD
		timdFunc = lambda t, m: self.updateFirebaseWithTIMD(utils.makeTIMDFromTeamNumberAndMatchNumber(t, m.number))
		addTIMD = lambda m: map(lambda t: timdFunc(t, m), m.redAllianceTeamNumbers + m.blueAllianceTeamNumbers)
		map(addTIMD, matches)


	def addCompInfoToFirebase(self): #Doing these keys manually so less clicking in firebase is better and because just easier
		FBLocation = "/"
		result = firebase.put(FBLocation, 'code', self.competition.code)
		result = firebase.put(FBLocation, 'currentMatchNum', self.competition.currentMatchNum)

	def wipeDatabase(self):
		map(utils.printWarningForSeconds, range(10, 0, -1))
		print "\nWARNING: Wiping Firebase..."
		FBLocation = "/"
		firebase.delete(FBLocation, None)

	def cacheFirebase(self):
		while True:
			try:
				data = json.dumps(firebase.get("/", None))
				now = str(datetime.datetime.now())
				with open("./CachedFirebases/" + now + '.json', 'w') as f:
					f.write(data)
					f.close()
					break
			except: pass

	

def getPythonObjectForFirebaseDataAtLocation(location):
	return utils.makeASCIIFromJSON((firebase.get(location, None)))



