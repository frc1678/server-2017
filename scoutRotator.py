import pyrebase
import DataModel
import SPR
import firebaseCommunicator

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
fb = PBC.firebase

#Note: The names of test scouts are based on testing, and change frequently
testScouts = "nathan ben berin kenny ryan peter".split()
scouts = "janet justin alex wesley kyle mx aiden westley katie jesse jack sage jon ayush sam evan mingyo zoe gemma carter".split()
SPR = SPR.ScoutPrecision()

#creates list of availability values in firebase for each scout
def resetAvailability():
	availability = {name: 1 for name in scouts}
	fb.child('availability').set(availability)

#creates firebase objects for 18 scouts
def resetScouts():
	scouts = {'scout' + str(num) : {'currentUser': '', 'scoutStatus': ''} for num in range(1,19)}
	fb.child('scouts').set(scouts)

def doSPRsAndAssignments(newMatchNumber):
	if newMatchNumber.get('data') == None: return
	print('Setting scouts for match ' + str(fb.child('currentMatchNum').get().val()))
	#updates information from firebase
	newMatchNumber = str(fb.child('currentMatchNum').get().val())
	scoutDict = fb.child("scouts").get().val()
	#gets the teams we need to scout for
	blueTeams = fb.child("Matches").child(newMatchNumber).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(newMatchNumber).get().val()['redAllianceTeamNumbers']
	#Finds which scouts are available
	available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
	#Checks accuracy of scouts based on previous scouting
	SPR.calculateScoutPrecisionScores(fb.child("TempTeamInMatchDatas").get().val(), available)
	#Exports scout accuracy data for review
	SPR.sprZScores()
	#Assigns scouts to robots
	newAssignments = SPR.assignScoutsToRobots(available, redTeams + blueTeams, fb.child("scouts").get().val())
	#Puts assignments on firebase
	fb.child("scouts").update(newAssignments)

#Use this if tablets are assigned to scouts by the server, and then given to the correct scouts
def tabletHandoutStream():
	#makes new directories of scouts and availability in firebase, then starts assigning scouts
	resetScouts()
	resetAvailability()
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)

#Use this for running the server again (e.g. after a crash) to avoid reassigning scouts
def alreadyAssignedStream():
	#Starts asssigning scouts after the current match is over
	#This way, people don't get reassigned in the middle of a match or when assignments are otherwise fine
	startMatchNum = fb.child("currentMatchNum").get().val()
	newMatchNum = startMatchNum + 1
	while True:
		currentMatchNum = fb.child("currentMatchNum").get().val()
		if currentMatchNum == newMatchNum:
			break
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)

#Use this if you are restarting the server and need to reassign scouts but scouts already have tablets
def simpleStream():
	#starts assigning scouts, but leaves availability and tablet assignments intact
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)
