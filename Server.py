#By Bryton Moeller (2015-2016)
import sys
import traceback
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
import APNServer

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
comp = DataModel.Competition(PBC)
comp.updateTeamsAndMatchesFromFirebase()
comp.updateTIMDsFromFirebase()
# scheduleUpdater.updateSchedule()
calculator = Math.Calculator(comp)
cycle = 1
shouldSlack = False
consolidator = dataChecker.DataChecker()
# consolidator.start()
# APNServer.startNotiStream()
#Use this if tablets are assigned to scouts by the server, and then given to the correct scouts
#This means at the beginning of a competition day
# scoutRotator.tabletHandoutStream()

#Use this for running the server again (e.g. after a crash) to avoid reassigning scouts
# scoutRotator.alreadyAssignedStream()

#Use this if you are restarting the server and need to reassign scouts but scouts already have tablets
#Also useful for unexpected changes in availability
# scoutRotator.simpleStream()
 
def checkForMissingData():
	with open('missing_data.txt', 'w') as missingDataFile:
		missingDatas = calculator.getMissingDataString()
		if missingDatas:
			print(missingDatas)
		missingDataFile.write(str(missingDatas))

while(True):
	print("\nCalcs Cycle " + str(cycle) + "...")
	if cycle % 5 == 1:
		PBC.cacheFirebase()
	while(True):
		try:
			comp.updateTeamsAndMatchesFromFirebase()
			comp.updateTIMDsFromFirebase()
			break
		except Exception as e:
			print(e)
	checkForMissingData()
	try:
		calculator.doCalculations(PBC)
	except OSError:
		continue
	except:
		if shouldSlack:
			reportServerCrash(traceback.format_exc())
		else:
			print(traceback.format_exc())
		sys.exit(0)
	time.sleep(1)
	cycle += 1
