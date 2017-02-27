# CSV Exporter, by Bryton 2/10/16
import utils
from collections import OrderedDict
import pdb
import csv
from DataModel import Team

def CSVExportScoutZScores(zscores):
	with open('./SPRExport.csv', 'w') as f:
		writer = csv.DictWriter(f, fieldnames=['name', 'SPR', 'Z-Score'])
		writer.writeheader()
		for k,v in zscores.items():
			writer.writerow({'name' : k, 'SPR' : zscores[k][1], 'Z-Score' : zscores[k][0]})

def CSVExport(comp, name, keys=[]):
	excluded = ['calculatedData', 'name', 'imageKeys']
	with open('./CSVExport-' + name + '.csv', 'w') as f:
		defaultKeys = [k for k in Team().__dict__.keys() if k not in excluded and k in keys]
		defaultKeys += Team().calculatedData.__dict__.keys()
		defaultKeys = sorted(defaultKeys, key=lambda k: (k != "number", k.lower()))
		writer = csv.DictWriter(f, fieldnames=defaultKeys)
		writer.writeheader()
		for team in comp.teams:
			tDict = team.__dict__
			tDict.update(team.calculatedData.__dict__)
			keys = sorted(defaultKeys,key=lambda k: (k != "number", k.lower()))
			writer.writerow({k : tDict[k] for k in keys})

def CSVExportMini(comp, name):
	miniKeys = []
	CSVExport(comp, 'MINI', keys=miniKeys)

def CSVExportAll(comp):
	CSVExport(comp, 'ALL')

def CSVExportSAC(comp):
	keys = []
	CSVExport(comp, "SAC", keys=keys)

def CSVExportCVR(comp):
	keys = []
	CSVExport(comp, 'CVR', keys=keys)

def CSVExportCMP(comp):
	keys = []
	CSVExport(comp, "CHAMPS", keys=keys)

