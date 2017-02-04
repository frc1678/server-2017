import pyrebase
import numpy as np
import utils
import time
import pdb 
import multiprocessing

config = {
	"apiKey": "mykey",
	"authDomain": "scouting-2017-5f51c.firebaseapp.com",
	"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
	"storageBucket": "scouting-2017-5f51c.appspot.com"
}

listKeys = ["highShotTimesForBoilerTele", "highShotTimesForBoilerAuto", "lowShotTimesForBoilerAuto", "lowShotTimesForBoilerTele"]
constants = ['matchNumber', 'teamNumber']
boilerKeys = ['time', 'numShots']
standardDictKeys = ['gearsPlacedByLiftAuto', 'gearsPlacedByLiftTele']
firebase = pyrebase.initialize_app(config)
firebase = firebase.database()

class DataChecker(multiprocessing.Process):
	"""Checks data..."""
	def __init__(self):
		super(DataChecker, self).__init__()
		self.consolidationGroups = {}

	def commonValue(self, vals, key):
		if len(set(map(type, vals))) != 1: 
			return self.attempt(vals)
		if map(type, vals).count(bool) == len(map(type, vals)):
			return bool(self.joinBools(vals))
		elif list(set(map(type, vals)))[0] == unicode:
			return vals
		else:
			return self.joinList(vals)

	def attempt(self, vals):
		if map(type, vals).count(bool) > 0:
			return self.commonValue(map(bool, vals), 'none')
		else: return

	def joinBools(self, bools):
		a = map(bools.count, bools)
		mCV = bools[a.index(max(a))]
		try:
			return bool(mCV) if values.count(mCV) > len(bools) / 2 else True if np.mean(bools) >= 0.5 else False
		except:
			return None 
		
	def joinList(self, values):
		a = map(values.count, values)
		mCV = values[a.index(max(a))]
		try:
			return mCV if values.count(mCV) > len(values) / 2 else np.mean(values)
		except:
			return None

	def joinValues(self, key):
		return {k : self.findCommonValuesForKeys(map(lambda tm: (tm.get(k) or []), self.consolidationGroups[key])) if k in listKeys else self.consolidationGroups[key][0][k] if k in constants else self.avgDict(map(lambda c: (c.get(k) or {}), self.consolidationGroups[key])) if k in standardDictKeys else self.commonValue(map(lambda tm: tm.get(k) or 0, self.consolidationGroups[key]), k) for k in self.getAllKeys(map(lambda v: v.keys(), self.consolidationGroups[key]))}

	def findCommonValuesForKeys(self, lis):
		length = int(self.commonValue(map(len, lis), 'none'))
		valuesList = map(lambda t: t[:length], lis)
		for i in boilerKeys:
			for v in range(len(valuesList[0])):
				cv = self.commonValue(filter(lambda t: t!=None, map(lambda val: val[v][i] if len(i) > v else None, valuesList)), 'none')
				for j in valuesList:
					j[v][i] = cv

	def getAllKeys(self, keyArrays):
		return list(set([v for l in keyArrays for v in l]))

	def avgDict(self, dicts):
		keys = self.getAllKeys(map(lambda d: d.keys(), dicts))
		return {k : self.commonValue(map(lambda v: (v.get(k) or 0), dicts), k) for k in keys}

	def getConsolidationGroups(self, tempTIMDs):
		actualKeys = list(set([key.split('-')[0] for key in tempTIMDs.keys()]))
		return {key : [v for k, v in tempTIMDs.items() if k.split('-')[0] == key] for key in actualKeys}

	def run(self):
		while True:
			tempTIMDs = firebase.child("TempTeamInMatchDatas").get().val()
			if tempTIMDs == None:
				print "No data"
				continue
			self.consolidationGroups = self.getConsolidationGroups(tempTIMDs)
			map(lambda key: firebase.child("TeamInMatchDatas").child(key).update(self.joinValues(key)), self.consolidationGroups.keys())
			time.sleep(10) 

DataChecker().run()
