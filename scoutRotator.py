import pyrebase
import DataModel
import SPR
import firebaseCommunicator
import time

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
fb = PBC.firebase
# testScouts = "calvin ethan nathan wentao janet carter kenny ryan nate astha astha gemma livy ben".split()
scouts = "janet justin alex wesley kyle mx aidan westley katie jesse jack sage jon ayush sam evan mingyo zoe gemma carter calvin rachel".split()
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
	while True:
		try:
			availabilityUpdated = fb.child("availabilityUpdated").get().val()
		except:
			availabilityUpdated = 0
		if availabilityUpdated: break
		time.sleep(2)
	fb.child("availabilityUpdated").set(0)
	if newMatchNumber.get('data') == None: return
	print('Setting scouts for match ' + str(fb.child('currentMatchNum').get().val()))
	newMatchNumber = str(fb.child('currentMatchNum').get().val())
	scoutDict = fb.child("scouts").get().val()
	#gets the teams we need to scout for
	blueTeams = fb.child("Matches").child(newMatchNumber).get().val()['blueAllianceTeamNumbers']
	redTeams = fb.child("Matches").child(newMatchNumber).get().val()['redAllianceTeamNumbers']
	#These next lines find and assign available scouts
	available = [k for (k, v) in fb.child("availability").get().val().items() if v == 1]
	#Each scout is assigned to a robot in the next 2 lines
	SPR.calculateScoutPrecisionScores(fb.child("TempTeamInMatchDatas").get().val(), available)
	SPR.sprZScores(PBC)
	newAssignments = SPR.assignScoutsToRobots(available, redTeams + blueTeams, fb.child("scouts").get().val())
	#and it is put on firebase
	fb.child("scouts").update(newAssignments)

#Use this if tablets are assigned to scouts by the server, and then given to the correct scouts
def tabletHandoutStream():
	# resetScouts()
	# resetAvailability()
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)

#Use this for running the server again (e.g. after a crash) to avoid reassigning scouts
def alreadyAssignedStream():
	while True:
		startMatchNum = fb.child("currentMatchNum").get().val()
		newMatchNum = startMatchNum + 1
		time.sleep(1)
	

def startStreamAfterAssignment(newNum, newerNum):
	if newNum.get("data") == None: return
	if newNum["data"] == newerNum:
		doSPRsAndAssignments(newNum)

#Use this if you are restarting the server and need to reassign scouts but scouts already have tablets
#Also useful for unexpected changes in availability
def simpleStream():
	fb.child("currentMatchNum").stream(doSPRsAndAssignments)

