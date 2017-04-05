import DataModel
from firebaseCommunicator import PyrebaseCommunicator
import csv
from Math import Calculator


pbc = PyrebaseCommunicator()
 
comp = DataModel.Competition(pbc)
comp.updateTeamsAndMatchesFromFirebase()
comp.updateTIMDsFromFirebase()
calculator = Calculator(comp)

with open('./disfunctionalData-SAC.csv', 'w') as f:
		keys = ['number'] + range(9)
		writer = csv.DictWriter(f, fieldnames = keys)
		writer.writeheader()
		for t in comp.teams:
			timds = calculator.su.getCompletedTIMDsForTeam(t)
			timds = sorted(timds, key=lambda t: t.matchNumber)
			dic = {}
			for key in keys:
				if key != 'number':
					dic[key] = timds[key - 1].calculatedData.wasDisfunctional
				else:
					dic[key] = t.number
			writer.writerow(dic)

