import pyrebase
import numpy as np
import utils
import time
import multiprocessing
import pdb
import firebaseCommunicator

#These are the keys that have lists of dicts
#Lists may have different numbers of dicts, but the keys in the dicts should be the same
listKeys = ["highShotTimesForBoilerTele", "highShotTimesForBoilerAuto", "lowShotTimesForBoilerAuto", "lowShotTimesForBoilerTele"]
#These ought to be the same across all tempTIMDs for the same TIMD
#(TIMD -> TeamInMatchData, so for a specific team in a specific match)
constants = ['matchNumber', 'teamNumber']
#These are the keys within each dict from the listKeys
boilerKeys = ['time', 'numShots', 'position']
#These are the keys that have dicts with consistent keys
standardDictKeys = ['gearsPlacedByLiftAuto', 'gearsPlacedByLiftTele']

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
firebase = PBC.firebase

class DataChecker(multiprocessing.Process):
	"""Combines data from tempTIMDs into TIMDs..."""
	def __init__(self):
		super(DataChecker, self).__init__()
		self.consolidationGroups = {}

	#Gets a common value for a list depending on the data type
	def commonValue(self, vals):
		#If there are several types, they are probably misformatted bools, so attempt tries turning them into bools and trying again
		if len(set(map(type, vals))) != 1:
			return self.attempt(vals)
		#If the values are bools, it goes to a function for bools
		elif type(vals[0]) == bool:
			return self.joinBools(vals)
		#Text does not need to be joined
		elif type(vals[0]) == str or type(vals[0]) == unicode:
			return vals
		#otherwise, if it is something like ints or floats, it goes to a general purpose function
		else:
			return self.joinList(vals)

	#Uses commonValue if at least one value is a bool, on the basis that they should all be bools, but some are just not written properly
	def attempt(self, vals):
		if map(type, vals).count(bool) > 0:
			return self.commonValue(map(bool, vals))
		else:
			return

	#Gets the most common bool of a list of inputted bools
	def joinBools(self, bools):
		return False if bools.count(False) > len(bools) / 2 else True

	#Returns the most common value in a list, or the average if no value is more than half the list
	def joinList(self, values):
		if values:
			a = map(values.count, values)
			mCV = values[a.index(max(a))]
			try:
				return mCV if values.count(mCV) > len(values) / 2 else np.mean(values)
			except:
				return
		else:
			return

	#This is the common value function for lists of dicts
	#It consolidates the data on shots from scouts, by comparing each shot to other scouts' info on the same shot
	#The nth dict on each list should be the same
	def findCommonValuesForKeys(self, lis):
		#Finds the largest number of dicts within each list (within each scout's observations)
		#(e.g. if there is disagreement over how many shots a robot took in a particular match)
		if lis:
			largestListLength = max(map(len, lis))
		else:
			largestListLength = 0
		#If someone missed a dict (for a shot, that is, they did not include one that another scout did, this makes one with no values)
		for aScout in lis:
			if len(aScout) < largestListLength:
				aScout += [{'numShots': 0, 'position': 'Other  ', 'time': 0}] * (largestListLength - len(aScout))
		returnList = []
		for num in range(largestListLength):
			returnList += [{}]
			#Finds dicts that should be the same (e.g. each shot time dict for the same shot) within the tempTIMDs
			#This means comparisons such as the first shot in teleop by a given robot, as recorded by multiple scouts
			dicts = [scout[num] for scout in lis]
			consolidationDict = {}
			#Combines dicts that should be the same into a consolidation dict
			for key in dicts[0].keys():
				consolidationDict[key] = []
				for aDict in dicts:
					consolidationDict[key] += [aDict[key]]
				#The time and number of shots can be compared to get a common value
				if key != 'position':
					returnList[num].update({key: self.commonValue(consolidationDict[key])})
			#If there is only one scout, their statement about position is accepted as right
			if len(consolidationDict['position']) == 1:
				returnList[num].update({'position': consolidationDict['position'][0]})
			#If there are 2 scouts, pick position that isn't the key unless they are both in agreement
			elif len(consolidationDict['position']) % 2 == 0:
				if consolidationDict['position'][0].lower() != 'key':
					returnList[num].update({'position': consolidationDict['position'][0]})
				else:
					returnList[num].update({'position': consolidationDict['position'][1]})
			#If there are 3 scouts (or more, but that shouldn't happen), the position value is the most common position value
			else:
				positionFrequencies = map(consolidationDict['position'].count, consolidationDict['position'])
				commonPosition = consolidationDict['position'][positionFrequencies.index(max(positionFrequencies))]
				returnList[num].update({'position': commonPosition})
		return returnList

	#Combines data from whole TIMDs
	def joinValues(self, key):
		returnDict = {}
		#Flattens the list of lists of keys into a list of keys
		for k in self.getAllKeys(map(lambda v: v.keys(), self.consolidationGroups[key])):
			if k in listKeys:
				#Gets a common value for lists of dicts (for boiler/ball values) and puts it into the combined TIMD
				returnDict.update({k: self.findCommonValuesForKeys(map(lambda tm: (tm.get(k) or []), self.consolidationGroups[key]))})
			elif k in constants:
				#Constants should be the same across all tempTIMDs, so the common value is just the value in one of them
				#Puts the value into the combined TIMD
				returnDict.update({k: self.consolidationGroups[key][0][k]})
			elif k in standardDictKeys:
				#Gets a common value for dicts (placed gears) and puts it into the combined TIMD
				returnDict.update({k: self.avgDict(map(lambda c: (c.get(k) or {}), self.consolidationGroups[key]))})
			else:
				#Gets a common value across any kind of list of values and puts it into the combined TIMD
				if type(self.consolidationGroups[key][0]) == bool:
					returnDict.update({k: self.commonValue(map(lambda tm: tm.get(k) or False, self.consolidationGroups[key]))})
				else:
					returnDict.update({k: self.commonValue(map(lambda tm: tm.get(k) or 0, self.consolidationGroups[key]))})
		return returnDict
		#The line below is supposed to do the same thing as this 'joinvalues' function, and may or may not work
		#return {k : self.findCommonValuesForKeys(map(lambda tm: (tm.get(k) or []), self.consolidationGroups[key])) if k in listKeys else self.consolidationGroups[key][0][k] if k in constants else self.avgDict(map(lambda c: (c.get(k) or {}), self.consolidationGroups[key])) if k in standardDictKeys else self.commonValue(map(lambda tm: tm.get(k) or 0, self.consolidationGroups[key])) for k in self.getAllKeys(map(lambda v: v.keys(), self.consolidationGroups[key]))}

	#Flattens the list of lists of keys into a list of keys
	def getAllKeys(self, keyArrays):
		return list(set([v for l in keyArrays for v in l]))

	#Gets common values for values in each of a list of dicts
	def avgDict(self, dicts):
		keys = self.getAllKeys(map(lambda d: d.keys(), dicts))
		return {k : self.commonValue(map(lambda v: (v.get(k) or 0), dicts)) for k in keys}

	#Consolidates tempTIMDs for the same team and match
	def getConsolidationGroups(self, tempTIMDs):
		actualKeys = list(set([key.split('-')[0] for key in tempTIMDs.keys()]))
		return {key : [v for k, v in tempTIMDs.items() if k.split('-')[0] == key] for key in actualKeys}

	#Retrieves and consolidates tempTIMDs from firebase and combines their data, putting the result back onto firebase as TIMDs
	def run(self):
		while(True):
			tempTIMDs = firebase.child("TempTeamInMatchDatas").get().val()
			if tempTIMDs == None:
				time.sleep(5)
				continue
			self.consolidationGroups = self.getConsolidationGroups(tempTIMDs)
			map(lambda key: firebase.child("TeamInMatchDatas").child(key).update(self.joinValues(key)), self.consolidationGroups.keys())
			time.sleep(10)
