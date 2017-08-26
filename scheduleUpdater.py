#Last Updated: 8/26/17
import pyrebase
import firebaseCommunicator
import sys

PBC = firebaseCommunicator.PyrebaseCommunicator()
fb = PBC.firebase

def update(data):
	print(data)
	#prints and updates schedule on firebase based on the data
	if data['data'] == None:
		latest = 1
	elif data['data'] == 1:
		keys = map(lambda k: int(k.split('Q')[1].split('-')[0]), fb.child('TempTeamInMatchDatas').shallow().get().each())
		#makes a list of keys by sorting through every TempTIMD on firebase
		latest = sorted(keys, reverse = True)[0] + 1
		#sorts the keys to find the latest
		fb.child('matchFinished').set(0)
	else:
		fb.child('currentMatchNum').set(latest)
		#sets currentMatchNum on firebase

def scheduleListener():
	#call after update(), starts an update stream on firebase
	fb.child('matchFinished').stream(update)
