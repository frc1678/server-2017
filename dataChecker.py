import pyrebase
import numpy as np
import utils
import time

config = {
	"apiKey": "mykey",
	"authDomain": "1678-scouting-2016.firebaseapp.com",
	"databaseURL": "https://1678-scouting-2016.firebaseio.com",
	"storageBucket": "1678-scouting-2016.appspot.com"
}

listKeys = ["highShotTimesForBoilerTele", "highShotTimesForBoilerAuto", "lowShotTimesForBoilerAuto", "lowShotTimesForBoilerTele"]
constants = ['matchNumber', 'teamNumber']
boilerKeys = ['time', 'numShots']
firebase = pyrebase.initialize_app(config)
firebase = firebase.database()
consolidationGroups = {}

def commonValue(vals):
	if len(set(map(type, vals))) != 1: return
	if list(set(map(type, vals)))[0] == str:
		if (vals[0] == "true" or vals[0] == "false"):
			return bool(joinList(map(lambda v: int(utils.convertFirebaseBoolean(v)), vals)))
		else: return vals
	else:
		return joinList(vals)
	
def joinList(values):
	a = map(values.count, values)
	mCV = values[a.index(max(a))]
	try:
		return mCV if values.count(mCV) > len(values) / 2 else np.mean(values)
	except:
		return None

def joinValues(key):
	return {k : findCommonValuesForKeys(map(lambda tm: tm.get(k), consolidationGroups[key])) if k in listKeys else consolidationGroups[key][0][k] if k in constants else commonValue(map(lambda tm: tm.get(k), consolidationGroups[key])) for k in consolidationGroups[key][0].keys()}	

def findCommonValuesForKeys(lis):
	length = int(commonValue(map(len, lis)))
	valuesList = map(lambda t: t[:length], lis)
	for i in boilerKeys:
		for v in range(valuesList[0]):
			cv = commonValue(filter(lambda t: t, map(lambda i: i[v][i] if len(i) > v else None, valuesList)))
			for i in valuesList:
				i[v][i] = cv

def avgDict(dicts):
	dicts = filter(lambda d: d != None, dicts)
	return {d : map(np.mean, zip(*map(lambda tm: tm.get(d) if tm.get(d) != None else [0], dicts))) for d in extendList(map(lambda x: x.keys(), dicts))}

def getConsolidationGroups(tempTIMDs):
	actualKeys = list(set([key.split('-')[0] for key in tempTIMDs.keys()]))
	return {key : [v for k, v in tempTIMDs.items() if k.split('-')[0] == key] for key in actualKeys}

while True:
	tempTIMDs = firebase.child("TempTeamInMatchDatas").get().val()
	if tempTIMDs == None:
		print "No data"
		time.sleep(1)
		continue
	consolidationGroups = getConsolidationGroups(tempTIMDs)
	map(lambda key: firebase.child("TeamInMatchDatas").child(key).update(joinValues(key)), consolidationGroups.keys())
	time.sleep(1)




