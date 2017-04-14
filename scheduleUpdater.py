import pyrebase
import firebaseCommunicator
import sys

PBC = firebaseCommunicator.PyrebaseCommunicator()
fb = PBC.firebase
def update(data):
	print (data)
	if data['data'] == None:
		latest = 1
	else:
		if data['data'] == 1:
			keys = map(lambda k: int(k.split('Q')[1].split('-')[0]), fb.child("TempTeamInMatchDatas").shallow().get().each())
			latest = sorted(keys, reverse=True)[0] + 1
			fb.child('matchFinished').set(0)
		else:
			return
		fb.child('currentMatchNum').set(latest)

def scheduleListener():
	fb.child('matchFinished').stream(update)

