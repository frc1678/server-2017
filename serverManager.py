#Last Updated: 8/26/17
import CSVExporter
import DataModel
import firebaseCommunicator
import os
import time
import traceback

PBC = firebaseCommunicator.PyrebaseCommunicator()
 
comp = DataModel.Competition(PBC)

while(True):
	comp.updateTeamsAndMatchesFromFirebase()
	cmd = raw_input('>>> ').split()
	if cmd[0] == 'exp':
		try:
			if cmd[1] == 'all':
				CSVExporter.CSVExportAll(comp)
				comp.PBC.sendExport('EXPORT-ALL.csv')
			elif cmd[1] == 'min':
				CSVExportMini(comp)
		except Exception as e:
			print(traceback.format_exc())
	elif cmd[0] == 'hi':
		pass
	time.sleep(1)				
