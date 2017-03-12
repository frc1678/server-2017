import CSVExporter
import DataModel
import firebaseCommunicator
import os
import time

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
comp = DataModel.Competition(PBC)

while(True):
	comp.updateTeamsAndMatchesFromFirebase()
	comp.updateTIMDsFromFirebase()
	cmd = raw_input(">>> ").split()
	if cmd[0] == "exp":
		try:
			if cmd[1] == "all":
				CSVExporter.CSVExportAll(comp)
				comp.PBC.sendExport('CSVExport-ALL.csv')
			elif cmd[1] == "min":
				CSVExportMini(comp)
		except Exception as e:
			print e
	elif cmd[0] == "hi":
		pass #Is there supposed to be a break statement here or is it supposed to keep looping after?
	time.sleep(1)				
