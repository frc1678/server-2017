#CSV Exporter, by Bryton 2/10/16
import utils
from collections import OrderedDict
import csv
from DataModel import Team
import Math

def CSVExportScoutZScores(zscores):
	with open('./sprExport.csv', 'w') as f:
		writer = csv.DictWriter(f, fieldnames = ['name', 'spr', 'Z-Score'])
		writer.writeheader()
		for k, v in zscores.items():
			writer.writerow({'name' : k, 'spr' : zscores[k][1], 'Z-Score' : zscores[k][0]})

def CSVExport(comp, name, keys = []):
	calculator = Math.Calculator(comp)
	excluded = ['calculatedData', 'name', 'imageKeys', 'pitAllImageURLs', 'pitSelectedImageName']
	with open('./EXPORT-' + name + '.csv', 'w') as f:
		defaultKeys = [k for k in Team().__dict__.keys() if k not in excluded and k in keys]
		defaultKeys += [k for k in Team().calculatedData.__dict__.keys() if k in keys]
		defaultKeys = sorted(defaultKeys, key = lambda k: (k != "number", k.lower()))
		writer = csv.DictWriter(f, fieldnames = defaultKeys)
		writer.writeheader()
		for team in comp.teams:
			team.numMatchesPlayed = len(calculator.su.getCompletedMatchesForTeam(team))
			tDict = team.__dict__
			tDict.update(team.calculatedData.__dict__)
			keys = sorted(defaultKeys, key = lambda k: (k != "number", k.lower()))
			writer.writerow({k : tDict[k] for k in keys})

def readOPRData():
	teamsDict = {}
	wantedKeys = ['auto Fuel High','auto Scored Gears', 'teleop Scored Gears', 'teleop Takeoff Points']
	with open('./data/LasVegas-Table 1.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		first = True
		keys = []
		for r in reader:
			if first:
				keys = r[None]
				first = False
			else:
				teamsDict[r[None][keys.index('team Number')]] = {}
				for k in wantedKeys:
					teamsDict[r[None][keys.index('team Number')]][k] = r[None][keys.index(k)]
	with open('./filteredLVData.csv', 'w') as f:
		writer = csv.DictWriter(f, fieldnames = ['team Number'] + wantedKeys)
		writer.writeheader()
		for key, value in teamsDict.items():
			writer.writerow({k : teamsDict[key][k] if k != 'team Number' else key for k in ['team Number'] + wantedKeys})

def CSVExportMini(comp, name):
	miniKeys = []
	CSVExport(comp, 'MINI', keys = miniKeys)

def CSVExportAll(comp):
	CSVExport(comp, 'ALL', keys = Team().__dict__.keys() + Team().calculatedData.__dict__.keys())

def CSVExportSAC(comp):
	keys = []
	CSVExport(comp, "SAC", keys = keys)

def CSVExportCVR(comp):
	keys = []
	CSVExport(comp, 'CVR', keys = keys)

def CSVExportCMP(comp):
	keys = []
	CSVExport(comp, "CHAMPS", keys = keys)
