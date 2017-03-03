from firebase import firebase as fb
import time
import datetime
import pyrebase
config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyrebase.initialize_app(config)
fb = f.database()
def update(data):
	if data['data'] == None: 
		fb.child('currentMatchNum').set(1)
		return
	matches = fb.child('Matches').get().val()
	cm = min(filter(lambda k: None in [matches[k].get('redScore'), matches[k].get('blueScore')], range(1, len(matches))))
	fb.child('currentMatchNum').set(cm)
def updateSchedule():
	fb.child('Matches').stream(update)
