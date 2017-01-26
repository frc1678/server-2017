import pyrebase
import numpy as np
import utils
import time
import pdb 

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

listKeys = ["highShotTimesForBoilerTele", "highShotTimesForBoilerAuto", "lowShotTimesForBoilerAuto", "lowShotTimesForBoilerTele"]
constants = ['matchNumber', 'teamNumber']
boilerKeys = ['time', 'numShots']
standardDictKeys = ['gearsPlacedByLiftAuto', 'gearsPlacedTele', '']
firebase = pyrebase.initialize_app(config)
firebase = firebase.database()
consolidationGroups = {}

def commonValue(vals):
	if len(set(map(type, vals))) != 1: return
	if list(set(map(type, vals)))[0] == str:
		if ("true" in vals or "false" in vals):
			cv = joinList(map(lambda v: int(utils.convertFirebaseBoolean(v)), vals))
			return False if cv < 0.5 else False
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
	return {k : findCommonValuesForKeys(map(lambda tm: (tm.get(k) or []), consolidationGroups[key])) if k in listKeys else consolidationGroups[key][0][k] if k in constants else avgDict(map(lambda c: (c.get(k) or {}), consolidationGroups[key])) if k in standardDictKeys else commonValue(map(lambda tm: tm.get(k) or 0, consolidationGroups[key])) for k in getAllKeys(map(lambda v: v.keys(), consolidationGroups[key]))}

def findCommonValuesForKeys(lis):
	length = int(commonValue(map(len, lis)))
	valuesList = map(lambda t: t[:length], lis)
	for i in boilerKeys:
		for v in range(len(valuesList[0])):
			cv = commonValue(filter(lambda t: t, map(lambda val: val[v][i] if len(i) > v else None, valuesList)))
			for j in valuesList:
				j[v][i] = cv

def getAllKeys(keyArrays):
	return list(set([v for l in keyArrays for v in l]))

def avgDict(dicts):
	keys = getAllKeys(map(lambda d: d.keys(), dicts))
	return {k : commonValue(map(lambda v: (v.get(k) or 0), dicts)) for k in keys}

def getConsolidationGroups(tempTIMDs):
	actualKeys = list(set([key.split('-')[0] for key in tempTIMDs.keys()]))
	return {key : [v for k, v in tempTIMDs.items() if k.split('-')[0] == key] for key in actualKeys}
consolidated = []
while True:
	tempTIMDs = firebase.child("TempTeamInMatchDatas").get().val()
	if tempTIMDs == None:
		print "No data"
		time.sleep(1)
		continue
	consolidationGroups = getConsolidationGroups(tempTIMDs)
	timdsToProcess = filter(lambda l: l not in consolidated, consolidationGroups.keys())
	map(lambda key: firebase.child("TempTempTeamInMatchDatas").child(key).update(joinValues(key)), timdsToProcess)
	consolidated = consolidationGroups.keys()
	print "consolidated" + str(consolidated)
	time.sleep(3)