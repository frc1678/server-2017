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
fb = pyrebase.initialize_app(config)
firebase = fb.database()

class DataChecker(multiprocessing.Process):
	"""Checks data..."""
	def __init__(self):
		super(DataChecker, self).__init__()
		self.consolidationGroups = {}

	def commonValue(self, vals):
		if len(set(map(type, vals))) != 1:
			return self.attempt(vals)
		elif type(vals[0]) == bool:
			return self.joinBools(vals)
		elif type(vals[0]) == unicode:
			return vals
		else:
			return self.joinList(vals)

	#Uses commonValue if at least one value is a bool, on the basis that they should all be the same type, but some are just not written properly as bools
	def attempt(self, vals):
		if map(type, vals).count(bool) > 0:
			return self.commonValue(map(bool, vals))
		else:
			return

	#Gets the most common bool of a list of inputted bools (several times)
	def joinBools(self, bools):
		a = map(bools.count, bools)
		mCV = bools[a.index(max(a))]
		try:
			return bool(mCV) if values.count(mCV) > len(bools) / 2 else True if np.mean(bools) >= 0.5 else False
		except:
			return None

	#Returns the most common or average value out of a list
	def joinList(self, values):
		a = map(values.count, values)
		mCV = values[a.index(max(a))]
		try:
			return mCV if values.count(mCV) > len(values) / 2 else np.mean(values)
		except:
			return None

	def joinValues(self, key):
		returnDict = {}
		for k in self.getAllKeys(map(lambda v: v.keys(), self.consolidationGroups[key])):
			if k in listKeys:
				returnDict.update({k: self.findCommonValuesForKeys(map(lambda tm: (tm.get(k) or []), self.consolidationGroups[key]))})
			elif k in constants:
				returnDict.update({k: self.consolidationGroups[key][0][k]})
			elif k in standardDictKeys:
				returnDict.update({k: self.avgDict(map(lambda c: (c.get(k) or {}), self.consolidationGroups[key]))})
			else:
				returnDict.update({k: self.commonValue(map(lambda tm: tm.get(k) or 0, self.consolidationGroups[key]))})
		return returnDict
		#return {k : self.findCommonValuesForKeys(map(lambda tm: (tm.get(k) or []), self.consolidationGroups[key])) if k in listKeys else self.consolidationGroups[key][0][k] if k in constants else self.avgDict(map(lambda c: (c.get(k) or {}), self.consolidationGroups[key])) if k in standardDictKeys else self.commonValue(map(lambda tm: tm.get(k) or 0, self.consolidationGroups[key])) for k in self.getAllKeys(map(lambda v: v.keys(), self.consolidationGroups[key]))}

	def findCommonValuesForKeys(self, lis):
		#Finds the most common number of dict within each list in the larger list
		listOfLengths = []
		for aScout in lis:
			listOfLengths += [len(aScout)]
		lengthFrequencies = map(listOfLengths.count, listOfLengths)
		mostCommonNum = listOfLengths[lengthFrequencies.index(max(lengthFrequencies))]
		#If someone missed a dict (for a shot) (that is, they did not include one that most of the scouts did), this makes one with no values
		for aScout in lis:
			if len(aScout) < mostCommonNum:
				for x in range(mostCommonNum - len(aScout)):
					aScout += [{'numShots': 0, 'position': 0, 'time': 0}]
		returnList = []
		for num in range(mostCommonNum):
			returnList += [{}]
			#comparing dicts that should be the same (e.g. each shot time dict for the same shot) within the tempTIMDs
			#This means comparisons such as the first shot in teleop by a given robot, as recorded by multiple scouts
			dicts = [scout[num] for scout in lis]
			consolidationDict = {}
			for key in dicts[0].keys():
				consolidationDict[key] = []
				for aDict in dicts:
					consolidationDict[key] += [aDict[key]]
			for key in consolidationDict.keys():
				if key != 'position':
					values = consolidationDict[key]
					valueFrequencies = map(values.count, values)
					commonValue = values[valueFrequencies.index(max(valueFrequencies))]
					if values.count(commonValue) <= len(values) / 2 and type(commonValue) != str:
						commonValue = np.mean(values)
					returnList[num].update({key: commonValue})
			if len(consolidationDict['position']) == 1:
				returnList[num].update({'position': consolidationDict['position']})
			elif len(consolidationDict['position']) == 2:
				if consolidationDict['position'][0].lower() != 'key':
					returnList[num].update({'position': consolidationDict['position'][0]})
				else:
					returnList[num].update({'position': consolidationDict['position'][1]})
			else:
				positionFrequencies = map(consolidationDict['position'].count, consolidationDict['position'])
				commonPosition = consolidationDict['position'][positionFrequencies.index(max(positionFrequencies))]
				returnList[num].update({'position': commonPosition})
		return returnList

	def getAllKeys(self, keyArrays):
		return list(set([v for l in keyArrays for v in l]))

	def avgDict(self, dicts):
		keys = self.getAllKeys(map(lambda d: d.keys(), dicts))
		return {k : self.commonValue(map(lambda v: (v.get(k) or 0), dicts)) for k in keys}

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
			print self.consolidationGroups
			map(lambda key: firebase.child("TeamInMatchDatas").child(key).update(self.joinValues(key)), self.consolidationGroups.keys())
			time.sleep(10)
			print "I completed a cycle"

DataChecker().run()
