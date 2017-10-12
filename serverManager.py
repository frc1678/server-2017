#Last Updated: 10/11/17
import CSVExporter
import DataModel
import firebaseCommunicator
import os
import time
import traceback

PBC = firebaseCommunicator.PyrebaseCommunicator()

fb = PBC.firebase
comp = DataModel.Competition(PBC)

while(True):
	comp.updateTeamsAndMatchesFromFirebase()
	cmd = raw_input('>>> ').split()
	if cmd[0] == 'exp':
		try:
			if cmd[1] == 'all':
				CSVExporter.CSVExportGeneral(comp, "ALL")
				comp.PBC.sendExport('EXPORT-ALL.csv')
			elif cmd[1] == 'min':
				CSVExportMini(comp)
		except Exception as e:
			print(traceback.format_exc())
	elif cmd[0] == 'sns':
		scoutSentData = []
		scoutNotSentData = []
		tempTIMDs = fb.child('TempTeamInMatchDatas').get().val()
		for TIMD in tempTIMDs:
			name = fb.child('TempTeamInMatchDatas').child(TIMD).get().key()
			scout = name[-2:]
			if '-' in scout:
				scout = scout[1:]
			match = name.split('-')[0]
			match = match[-2:]
			if 'Q' in match:
				match = match[-1:]
			curMatch = str(fb.child('currentMatchNum').get().val())
			if str(match) == curMatch:
				scoutSentData.append(scout)
		control = [str(x) for x in range(1, 19)]
		for item in control:
			if item not in scoutSentData:
				scoutNotSentData.append(item)
		scoutNotSent = ''
		for item in scoutNotSentData: 
			scoutNotSent = scoutNotSent + item + " "
		print("Scouts that have not inputted data - " + scoutNotSent) 
	elif cmd[0] == 'hi':
		pass
	time.sleep(1)
