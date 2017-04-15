from firebaseCommunicator import PyrebaseCommunicator
import numpy as np
import csv

pbc = PyrebaseCommunicator()
temptimds = pbc.firebase.child("TeamInMatchDatas").get().val()
timds = {k : v for k,v in temptimds.items() if int(k.split('Q')[1].split('-')[0]) > 71}
teamsDict = {}
teamKeys = set(map(lambda k: int(k.split('Q')[0]), temptimds.keys()))
keys =  ['incapacitatedPercentage', 'disabledPercentage', 'liftoffPercentage', 'avgAgility', 'avgSpeed', 'avgGearGroundIntakesTele' , 'avgGearLoaderIntakesTele', 'avgBallControl', 'avgGearControl', 'avgDefense', 'avgKeyShotTime', 'avgHopperShotTime', 'disfunctionalPercentage', 'avgGearsPlacedAuto', 'avgGearsPlacedTele', 'avgHoppersOpenedAuto', 'avgHoppersOpenedTele', 'avgGearsEjectedTele', 'avgLiftoffTime', 'avgGearsFumbledTele']

def setAverages(dic, timds, **args):
	for k, v in args.items():
		vals = [v(t) for t in timds if v(t) != None]
		dic[k] = np.mean(vals) if len(vals) else None

def getBoilerAvg(timds, key):
	values = filter(lambda t: t.get(key) != None, timds)
	shots = lambda v: sum(map(lambda c: c['numShots'], v))
	return np.mean([shots(v[key]) for v in values]) if len(values) else None

def getValForKeys(timds, key):
	values = filter(lambda t: t.get(key) != None, timds)
	gearPlaced = lambda t: sum(t[key].values())
	return np.mean(map(gearPlaced, values)) if len(values) else None

for team in teamKeys:
	teamsDict[team] = {
		'number' : team
	}
	timds = [v for k,v in temptimds.items() if int(k.split('Q')[0]) == team]
	setAverages(teamsDict[team], timds,
        incapacitatedPercentage = lambda tm: tm.get('didBecomeIncapacitated'),
        disabledPercentage = lambda tm: tm.get('didStartDisabled'),
        liftoffPercentage = lambda tm: tm.get('didLiftoff'), 
        avgAgility = lambda tm: tm.get('rankAgility'), 
        avgSpeed = lambda tm: tm.get('rankSpeed'),
        avgGearGroundIntakesTele = lambda tm: tm.get('numGearGroundIntakesTele'), 
        avgGearLoaderIntakesTele = lambda tm: tm.get('numGearLoaderIntakesTele'),
        avgBallControl = lambda tm: tm.get('rankBallControl'), 
        avgGearControl = lambda tm: tm.get('rankGearControl'),
        avgDefense = lambda tm: tm.get('rankDefense') if tm.get('rankDefense') else None, 
        # avgKeyShotTime = lambda tm: tm.calculatedData.avgKeyShotTime,
        # avgHopperShotTime = lambda tm: tm.calculatedData.avgHopperShotTime,
        disfunctionalPercentage = lambda tm: tm.get('didBecomeIncapacitated') * 0.5 + tm.get('didStartDisabled'),
        avgHoppersOpenedAuto = lambda tm: tm.get('numHoppersOpenedAuto'), 
        avgHoppersOpenedTele = lambda tm: tm.get('numHoppersOpenedTele'), 
        avgGearsEjectedTele = lambda tm: tm.get('numGearsEjectedTele'),
        avgLiftoffTime = lambda tm: tm.get('liftoffTime'), 
        avgGearsFumbledTele = lambda tm: tm.get('numGearsFumbledTele'))
	teamsDict[team]['avgHighShotsAuto'] = getBoilerAvg(timds, 'highShotTimesForBoilerAuto')
	teamsDict[team]['avgHighShotsTele'] = getBoilerAvg(timds, 'highShotTimesForBoilerTele')
	teamsDict[team]['avgLowShotsAuto'] = getBoilerAvg(timds, 'lowShotTimesForBoilerAuto')
	teamsDict[team]['avgLowShotsTele'] = getBoilerAvg(timds, 'lowShotTimesForBoilerTele')
	teamsDict[team]['avgGearsPlacedAuto'] = getValForKeys(timds, 'gearsPlacedByLiftAuto')
	teamsDict[team]['avgGearsPlacedTele'] = getValForKeys(timds, 'gearsPlacedByLiftTele')

with open('./preScoutingWorld.csv', 'w') as f:
	default = ['number'] + keys
	w = csv.DictWriter(f, fieldnames = default)
	w.writeheader()
	for team, v in teamsDict.items():
		w.writerow({k : v.get(k) for k in default})











