#By Bryton Moeller (2015-2016)
import DataModel
import firebaseCommunicator
import Math
import pdb
import csv

pbc = firebaseCommunicator.PyrebaseCommunicator()
comp = DataModel.Competition(pbc)
comp.updateTeamsAndMatchesFromFirebase()
comp.updateTIMDsFromFirebase()
calc = Math.Calculator(comp)

with open('./gearRegress.csv', 'w') as f:
	writer = csv.DictWriter(f, fieldnames = ['avgTotalGears', 'rotorPts/GearOPR'])
	print calc.rotorPointsPerGearForTeams()

