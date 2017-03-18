import shutil
import sys
import os
import TBACommunicator

def getSchedule():
	tbac = TBACommunicator.TBACommunicator()
	print(tbac.makeEventRankingsRequest())
	return filter(lambda v: v['comp_level'] == 'qf', tbac.makeEventMatchesRequest())

def getVideoKey(number):
	match = matches[number]
	key = list('Q' + str(match['match_number']) + '_')
	teams = match['alliances']['red']['teams'] + match['alliances']['blue']['teams']
	[key.append(str(number) + "_") for number in teams]
	return "".join(key)

def moveVids(folder, dest, startnum = 1):
	if not folder or not dest:
		print("Error: Folders not set")
		return
	files = os.listdir(folder)
	print len(files)
	destFiles = os.listdir(dest)[1:]
	if destFiles:
		matchToStartFrom = len(destFiles)
		files = files[matchToStartFrom:]
		files = sorted(files, key = lambda k: os.stat(folder + k).st_ctime)
		matchesToFiles = dict(zip(range(matchToStartFrom, len(files) + matchToStartFrom), files))
		[moveVid(getVideoKey(k), folder + fileName, dest) for k, fileName in matchesToFiles.items()]
		return
	files = sorted(files, key = lambda k: os.stat(folder + k).st_ctime)
	map(lambda n: moveVid(getVideoKey(n), folder + files[n], dest), range(len(files)))

def replayLastMatch(folder):
	if not folder:
		print("ERROR: Folders not set")
		return
	files = os.listdir(folder)[1:]
	files = sorted(files, key = lambda k: os.stat(folder + k).st_ctime)
	fileToDelete = files[-1]
	print folder + fileToDelete
	os.remove(folder + fileToDelete)	

def moveVid(key, filePath, dest):
	shutil.copy(filePath, dest + key + ".mov")

print("Downloading schedule...")
matches = getSchedule()

try:
	videoFolder = sys.argv[1]
	destFolder = sys.argv[2]
except:
	videoFolder = ""
	destFolder = ""
startFromNum = False
print("Video system 2017. Type help for details.")

while(True):
	numberToStartFrom = 1
	cmd = raw_input(">>> ").split()
	if not cmd: continue
	try:
		if cmd[0] == "setdest":
			destFolder = cmd[1]
	except:
		print("Error: Must supply more arguments")
	try:
		if cmd[0] == "setvid":
			cmdWithSpaces = map(lambda n: n + " ", cmd)
			new = "".join(cmdWithSpaces[1:])[:]
	except:
		print("Error: Must supply more arguments")
	if cmd[0] == "replay":
		replayLastMatch(videoFolder)
	elif cmd[0] == "done":
		moveVids(videoFolder, destFolder)
	elif cmd[0] == "help":
		print("setdest [FILEPATH] - Reset the file path to which you want to videos to be moved")
		print("setvid [FILEPATH] - Reset the file path at which the unnamed videos will be stored")
		print("replay - Deletes last recording (RUN THIS BEFORE YOU RECORD ANYTHING ELSE)")
		print("done - Run the video mover and organize all of the video files by match (run at the end of the day)")
	
