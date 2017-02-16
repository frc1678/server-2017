# by Bryton Moeller (2015-2016)

import json
import sys
import traceback

#Our Modules
import DataModel
import firebaseCommunicator
import Math
import unicodedata
import time
import CSVExporter
import utils
import pdb
import CrashReporter
import numpy as np
import dataChecker
import multiprocessing
import firebaseCacher
import scoutRotator

print "starting"
comp = DataModel.Competition()
comp.updateTeamsAndMatchesFromFirebase()
#scoutRotator.emptyTIMDs()
FBC = firebaseCommunicator.FirebaseCommunicator(comp)
#FBC.addTIMDsToFirebase(comp.matches)
comp.updateTIMDsFromFirebase()
CSVExporter.TSVExportAll(comp)
calculator = Math.Calculator(comp)
cycle = 1
shouldEmail = False
emailer = CrashReporter.EmailThread()
consolidator = dataChecker.DataChecker()
consolidator.start()
#firebaseCacher.startFirebaseCacheStream(FBC)
scoutRotator.doThingStream()
#scoutRotator.simpleStream()

def checkForMissingData():
	with open('missing_data.txt', 'w') as missingDataFile:
		missingDatas = calculator.getMissingDataString()
		print missingDatas
		missingDataFile.write(str(missingDatas))

while(True):
	print("\nCalcs Cycle " + str(cycle) + "...")
	comp.updateCurrentMatchNum()
	comp.updateTeamsAndMatchesFromFirebase()
	comp.updateTIMDsFromFirebase()
	checkForMissingData()
	try:
		calculator.doCalculations(FBC)
	except:
		print "SOMETHING BAD KINDA HAPPENED"
		if shouldEmail:
			emailer.reportServerCrash(traceback.format_exc())
		else:
			print traceback.format_exc()
		sys.exit(0)
	time.sleep(1)
	cycle += 1
