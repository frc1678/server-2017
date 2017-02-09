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
# import scoutRotator

print "starting"
comp = DataModel.Competition()
comp.updateTeamsAndMatchesFromFirebase()
comp.updateTIMDsFromFirebase()
CSVExporter.TSVExportAll(comp)
FBC = firebaseCommunicator.FirebaseCommunicator(comp)
calculator = Math.Calculator(comp)
cycle = 1
shouldEmail = False
emailer = CrashReporter.EmailThread()
consolidator = dataChecker.DataChecker()
# consolidator.start()
# firebaseCacher.startFirebaseCacheStream(FBC)
#scoutRotator.resetAvailability()
#scoutRotator.resetScouts()
# scoutRotator.doThingStream()


def checkForMissingData():
	with open('missing_data.txt', 'w') as missingDataFile:
		missingDatas = calculator.getMissingDataString()
		print missingDatas
		missingDataFile.write(str(missingDatas))

while(True):
	print("\nCalcs Cycle " + str(cycle) + "...")
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
