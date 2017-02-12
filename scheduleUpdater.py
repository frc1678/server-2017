from firebase import firebase as fb
import time
import datetime
fb = fb.FirebaseApplication('https://scouting-2017-5f51c.firebaseio.com/')
Matches = fb.get('/Matches', None)
def updateSchedule(Matches):
	for num in Matches[1:]:
		if num.get('redScore') == None and num.get('blueScore') == None:
			numberstring = str(num['number'])
			UpdatedMatches = fb.get('/Matches', None)
			matchNum = int(numberstring)
			break 
	fb.put('/', 'currentMatchNumber', matchNum)		
	Matches = UpdatedMatches
	time_now = str(datetime.datetime.now())

def update():
	while True:
		UpdatedMatches = fb.get('/Matches', None)
		if Matches != UpdatedMatches:
			updateSchedule(Matches)
			time.sleep(1)
		else:
			continue



