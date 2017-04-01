import pyrebase
import firebaseCommunicator
import sys

PBC = firebaseCommunicator.PyrebaseCommunicator()
fb = PBC.firebase
def update(data):
	if data['data'] == None:
		latest = 1
	else:
		keys = map(lambda k: int(k.split('Q')[1].split('-')[0]), fb.child("TempTeamInMatchDatas").shallow().get().each())
		latest = sorted(keys, reverse=True)[0] + 1
		fb.child('currentMatchNum').set(latest)

def updateSchedule():
	fb.child('TempTeamInMatchDatas').stream(update)

# updateSchedule()
