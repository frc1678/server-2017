# by Bryton Moeller (2015-2016)

import sys
import traceback

#Our Modules
import DataModel
import firebaseCommunicator
import Math
import time
import CSVExporter
import pdb
from CrashReporter import reportServerCrash
import dataChecker
import scoutRotator
import scheduleUpdater

print "Starting"
comp = DataModel.Competition()
comp.updateTeamsAndMatchesFromFirebase()
comp.updateCurrentMatchNum()
FBC = firebaseCommunicator.FirebaseCommunicator(comp)
# scheduleUpdater.updateSchedule()
CSVExporter.CSVExportAll(comp)
calculator = Math.Calculator(comp)
cycle = 1
shouldEmail = False
consolidator = dataChecker.DataChecker()
consolidator.start()

#Use this if tablets are assigned to scouts by the server, and then given to the correct scouts
#scoutRotator.tabletHandoutStream()

#Use this if scouts sign in on tablets and the rotation starts when they each have one
#scoutRotator.tabletLoginStream()

def checkForMissingData():
	with open('missing_data.txt', 'w') as missingDataFile:
		missingDatas = calculator.getMissingDataString()
		if missingDatas:
			print missingDatas
		missingDataFile.write(str(missingDatas))

while(True):
	print("\nCalcs Cycle " + str(cycle) + "...")
	if cycle % 5 == 1:
		FBC.cacheFirebase()
	while(True):
		try:
			comp.updateTeamsAndMatchesFromFirebase()
			comp.updateTIMDsFromFirebase()
			comp.updateCurrentMatchNum()
			break
		except Exception as e:
			print e
			pass
	checkForMissingData()
	try:
		calculator.doCalculations(FBC)
	except:
		print "SOMETHING BAD KINDA HAPPENED"
		if shouldEmail:
			reportServerCrash(traceback.format_exc())
		else:
			print traceback.format_exc()
		sys.exit(0)
	time.sleep(1)
	cycle += 1
