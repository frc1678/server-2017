#CSV Exporter, by Bryton 2/10/16
import utils
from collections import OrderedDict
from TBACommunicator import TBACommunicator
import csv
from DataModel import *
import Math

def CSVExportScoutZScores(zscores):
	with open('./scoutRankExport.csv', 'w') as f:
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
	wantedKeys = ['auto Fuel High','auto Scored Gears', 'teleop Scored Gears', 'teleop Takeoff Points', 'auto Fuel Low', 'teleop Fuel Low', 'teleop Fuel High', 'auto Mobility Points']
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
	return teamsDict

def predict():
	print 'reading...'
	teamsDict = readOPRData()
	# comp.updateTeamsAndMatchesFromFirebase()
	teamsList = []
	print 'creating teams...'
	for team, value in teamsDict.items()[1:]:
		calcData = CalculatedTeamData(avgHighShotsTele=float(value['teleop Fuel High']), avgHighShotsAuto=float(value['auto Fuel High']), avgLowShotsAuto=float(value['auto Fuel Low']), avgLowShotsTele=float(value['teleop Fuel Low']), liftoffAbility=float(value['teleop Takeoff Points']), avgGearsPlacedAuto=float(value['auto Scored Gears']), avgGearsPlacedTele=float(value['teleop Scored Gears']), baselineReachedPercentage=float(value['auto Mobility Points']))
	# 	writer = csv.DictWriter(f, fieldnames = ['team Number'] + wantedKeys)
	# 	writer.writeheader()
	# 	for key, value in teamsDict.items():
	# 		writer.writerow({k : teamsDict[key][k] if k != 'team Number' else key for k in ['team Number'] + wantedKeys})'])
		teamOb = Team(number = int(team), calculatedData=calcData)
		teamsList.append(teamOb)
	while True:
		inp = raw_input('>>> ').split()
		nums = map(lambda t: filter(lambda n: n.number == int(t), teamsList)[0], inp)
		r1, r2, r3, b1, b2, b3 = nums[0],nums[1],nums[2],nums[3],nums[4],nums[5]
		print "liftoff : " + str(sum(map(lambda t: t.calculatedData.liftoffAbility, [r1, r2, r3])))
		print str((sum(map(lambda t: t.calculatedData.liftoffAbility, [b1, b2, b3]))))
		print "gears : " + str(sum(map(lambda t: t.calculatedData.avgGearsPlacedAuto + t.calculatedData.avgGearsPlacedTele, [r1, r2, r3])))
		print str((sum(map(lambda t: t.calculatedData.avgGearsPlacedAuto + t.calculatedData.avgGearsPlacedTele, [b1, b2, b3]))))

#predict()

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
