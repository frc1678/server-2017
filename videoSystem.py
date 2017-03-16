import shutil
import sys
import pyrebase
import os

def getSchedule():
	config = {
		"apiKey": "mykey",
		"authDomain": "scouting-2017-5f51c.firebaseapp.com",
		"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
		"storageBucket": "scouting-2017-5f51c'.appspot.com"
	}
	app = pyrebase.initialize_app(config)
	fb = app.database()
	return fb.child('Matches').get().val()

print "Downloading schedule..."
matches = getSchedule()

def getVideoKey(number):
	match = matches[number]
	key = list('Q' + str(match['number']) + '_')
	teams = match['redAllianceTeamNumbers'] + match['blueAllianceTeamNumbers']
	[key.append(str(number) + "_") for number in teams]
	return "".join(key)

def moveVids(folder, dest, startnum=1):
	if not folder or not dest:
		print "Error: Folders not set"
		return
	files = os.listdir(folder)[1:]
	files = sorted(files, key=lambda k: os.stat(folder + k).st_ctime)
	for n in range(len(files)):
		moveVid(getVideoKey(n + 1), folder + files[n], dest)

def replayMatch(folder, dest, filePath):
	moveVid()

def moveVid(key, filePath, dest):
	shutil.copy(filePath, dest + key + ".mov")
	

try:
	videoFolder = sys.argv[1]
	destFolder = sys.argv[2]
except:
	videoFolder = ""
	destFolder = ""
startFromNum = False
print "Video system 2017. Run setdest and setvid to set the correct folders"
while True:
	numberToStartFrom = 1
	cmd = raw_input(">>> ").split()
	if not cmd: continue
	try:
		if cmd[0] == "setdest":
			destFolder = cmd[1]
		elif cmd[0] == "setvid":
			videoFolder = cmd[1]
		elif cmd[0] == "replay":
			numberToReplay = cmd[1]
		elif cmd[0] == "start":
			numberToStartFrom = cmd[1]
			startFromNum = True
	except:
		"Error: Must supply more arguments"
	if cmd[0] == "done":
		if startFromNum:
			moveVids(videoFolder, destFolder)
		else:
			moveVids(videoFolder, destFolder, startnum=numberToStartFrom)
	