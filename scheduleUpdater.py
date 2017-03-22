import pyrebase
import firebaseCommunicator
import sys

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
fb = PBC.firebase

def update(data):
	if data['data'] == None:
		fb.child('currentMatchNum').set(1)
		return
	matches = fb.child('Matches').get().val()
	incomplete = filter(lambda k: not matches[k].get('redScore') and not matches[k].get('blueScore'), range(1, len(matches)))
	if incomplete:
		fb.child('currentMatchNum').set(min(incomplete))
	else:
		sys.exit(0)

def updateSchedule():
	fb.child('Matches').stream(update)
