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

comp = DataModel.Competition()
CSVExporter.TSVExportCMP(comp)
FBC = firebaseCommunicator.FirebaseCommunicator(comp)
calculator = Math.Calculator(comp)
cycle = 1
shouldEmail = False
emailer = CrashReporter.EmailThread()



def checkForMissingData():
	with open('missing_data.txt', 'w') as missingDataFile:
		missingDatas = calculator.getMissingDataString()
		print missingDatas
		missingDataFile.write(str(missingDatas))

while(True):
	print("\nCalcs Cycle " + str(cycle) + "...")
	FBC.cacheFirebase()
	comp.updateTeamsAndMatchesFromFirebase()
	comp.updateTIMDsFromFirebase()
	checkForMissingData()
	try:
		calculator.doCalculations(FBC)
	except:
		if shouldEmail:
			emailer.reportServerCrash(traceback.format_exc())
			sys.exit(0)
	time.sleep(1)
	cycle += 1