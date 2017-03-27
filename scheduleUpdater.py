import pyrebase
import firebaseCommunicator
import sys

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
fb = PBC.firebase

def update(data):
	print data
	if data['data'] == None:
		fb.child('currentMatchNum').set(1)
		return
	matches = fb.child('Matches').get().val()
	incomplete = filter(lambda k: matches[k].get('redScore') != None and matches[k].get('blueScore') != None, range(1, len(matches)))
	if incomplete:
		fb.child('currentMatchNum').set(min(incomplete))
	else:
		sys.exit(0)

def updateSchedule():
	fb.child('Matches').stream(update)
