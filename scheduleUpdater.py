import time
import datetime
import pyrebase
import firebaseCommunicator

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
fb = PBC.firebase

def update(data):
	if data['data'] == None: return
	matches = fb.child('Matches').get().val()
	cm = min(filter(lambda k: None in [matches[k].get('redScore'), matches[k].get('blueScore')], range(1, len(matches))))
	fb.child('currentMatchNum').set(cm)
def updateSchedule():
	fb.child('Matches').stream(update)
