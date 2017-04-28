import shutil
import sys
import os
import TBACommunicator

#Gets a list of matches to make a list of names
def getSchedule():
	tbac = TBACommunicator.TBACommunicator()
	return filter(lambda v: v['comp_level'] == 'qm', tbac.makeEventMatchesRequest())

#Creates a name for a video based on recording order, with the match number and team numbers
def getVideoKey(number):
	match = filter(lambda m: m['match_number'] == number + 1, matches)[0]
	print(matches[number]['match_number'])
	key = list('Q' + str(match['match_number']) + '_')
	teams = match['alliances']['red']['teams'] + match['alliances']['blue']['teams']
	[key.append(str(number) + "_") for number in teams]
	return "".join(key)

#Moves all videos from the start folder to destination folder
def moveVids(folder, dest):
	if not folder or not dest:
		print("Error: Folders not set")
		return
	files = os.listdir(folder)
	destFiles = os.listdir(dest)[1:]
	files = sorted(files, key = lambda k: os.stat(folder + k).st_ctime)
	if destFiles:
		matchToStartFrom = len(destFiles)
		files = files[matchToStartFrom:]
		matchesToFiles = zip(range(matchToStartFrom, len(files) + matchToStartFrom), files)
		[moveVid(getVideoKey(k), folder + fileName, dest) for k, fileName in matchesToFiles]
		return
	map(lambda n: moveVid(getVideoKey(n), folder + files[n], dest), range(len(files)))

#Deletes the most recent match for a replay
def replayLastMatch(folder):
	if not folder:
		print("ERROR: Folders not set")
		return
	if not len(os.listdir(folder)):
		print("ERROR: No match to replay")
		return
	files = os.listdir(folder)
	files = sorted(files, key = lambda k: os.stat(folder + k).st_ctime)
	fileToDelete = files[-1]
	print(folder + fileToDelete)
	os.remove(folder + fileToDelete)

def moveVid(key, filePath, dest):
	print(key)
	print(filePath)
	shutil.copy(filePath, dest + key + ".mov")

print("Downloading schedule...")
matches = getSchedule()
try:
	videoFolder = sys.argv[1]
	destFolder = sys.argv[2]
except:
	videoFolder = ""
	destFolder = ""
print("Video system 2017. Type help for details.")

while(True):
	cmd = raw_input(">>> ").split()
	if not cmd: continue
	try:
		if cmd[0] == "setdest":
			destFolder = cmd[1]
	except:
		print("Error: Must supply more arguments")
	try:
		if cmd[0] == "setvid":
			videoFolder = cmd[1]
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
