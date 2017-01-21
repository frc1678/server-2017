import utils
import numpy as np
import CacheModel as cache
import itertools
import TBACommunicator
import Math
import random

import pyrebase
import numpy as np
import utils

# Scout Performance Analysis
class ScoutPrecision(object):
	"""docstring for ScoutPerformance"""
	def __init__(self):
		super(ScoutPrecision, self).__init__()
		self.sprs = {}
		self.cycle = 0
		self.robotNumToScouts = []
		self.TBAC = TBACommunicator.TBACommunicator()
		self.keysToPointValues = {
			'numGearsPlacedTele' : 1,
			'numGearsPlacedAuto' : 1,
			'numHoppersOpenedAuto' : 1,
			'numHoppersOpenedTele' : 1
		}

		self.dictsToPointValues = {
			'highShotTimesForBoilerTele' : 1
		}

	#outputs list of TIMDs that have multiple scouts
	def filterToMultiScoutTIMDs(self):
		return filter(lambda tm: type(tm.scoutName) == list, self.comp.timds)

	#outputs list of TIMDs that an inputted scout was involved in
	def getTotalTIMDsForScoutName(self, scoutName):
		return len(map(lambda v: v["scoutName"] == scoutName, tempTIMDs.values()))

	#finds keys that start the same way and groups their values
	def consolidateTIMDs(self, temp):
		consolidationGroups = {}
		for k, v in temp.items():
			key = k.split('-')[0]
			if key in consolidationGroups.keys():
				consolidationGroups[key].append(v)
			else:
				consolidationGroups[key] = [v]
		return consolidationGroups

	def findOddScoutForDictionaryPoint(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs that aren't None
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs)) 

	def findOddScoutForDataPoint(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs that aren't None
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs)) 		#finds values (at an inputted key) that aren't None frome scouts that aren't None in tempTIMDs
		commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0 		#gets the most common value in the list previously generated
		if not values.count(commonValue) > len(values) / 2: commonValue = np.mean(values)		#If less than half of the values agree, the best estimate is the average
		differenceFromCommonValue = map(lambda v: abs(v - commonValue), values) 		#makes a list of the differences from the common value
		self.sprs = {scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))}		#adds the difference from this tempTIMDs to each scout's previous differences

	def calculateScoutPrecisionScores(self, temp, available):
		g = self.consolidateTIMDs(temp)
		[self.findOddScoutForDataPoint(v, key) for v in g.values() for key in v.keys() for k in self.keysToPointValues.keys()]
		self.calculateSPRs() 		#puts together tempTIMDs and does difference calculations
		self.sprs = {k:(v/float(self.cycle)/float(self.getTotalTIMDsForScoutName(k))) for (k,v) in self.sprs.items()} 		#divides values for scouts by cycle, and then by number of TIMDs
		for a in available.keys()[:18]: 		#for the first 18 available keys
			if a not in self.sprs.keys() and available.get(a) == 1: 			#If their values in available are 1 and they are not in use in sprs
				self.sprs[a] = np.mean(self.sprs.values()) 				#They are now set to the average value


	#sorts scouts by sprs score
	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	#orders available scouts by spr ranking, then makes a list of how frequently each scout should be selected (better scouts more frequently)
	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		func = lambda s: [s] * rankedScouts.index(s) * (100/(len(rankedScouts) - 1)) + 1
		return utils.extendList(map(func, available))

	#Somehow creates a list of scouts to use in a given match and assigns them to robots
	#I don't understand this function, and I am not sure it works
	def organizeScouts(self, available, currentTeams):
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)] 		#picks a random member of the inputted group
		grpCombos = utils.sum_to_n(len(available), 6, 3)	#sum_to_n should take 2-3 inputs, while here it takes 1
		if len(filter(lambda l: 2 not in l, scoutsPGrp)) > 0:
			scoutsPGrp = groupFunc(filter(lambda l: 2 not in l, scoutsPGrp)) if len(filter(lambda l: 2 not in l, scoutsPGrp)) > 0 else groupFunc(grpCombos)
		else:
			pas
		indScouts = self.getIndividualScouts(self.getScoutFrequencies(), len(filter(lambda x: x == 1, scoutsPGrp)))
		scouts = indScouts + map(lambda c: group(filter(lambda n: n in indScouts, available), scoutsPGrp[c]), c[len(indScouts):len(c)])
		return scoutsToRobotNums(scouts, currentTeams)

	def scoutToRobotNums(self, scouts, currentTeams): 	#assigns a list of scouts to a list of robots in order, and returns as a single dict
		f = lambda s: {scouts[s] : currentTeams[s]} if type(s) != list else self.mapKeysToValue(scouts[s], currentTeams[s])
		scoutAndNums  = map(f, range(len(scouts)))
		return {k : v for l in scoutAndNums for k, v in l.items()}

	def mapKeysToValue(self, keys, value): 	#Makes a dict with an inputted key attached to a value
		return {k : value for k in keys}

	def group(self, availableForGroup, count):
		return map(lambda n: addTo(availableForGroup, availableForGroup[random.randint(0, len(availableForGroup) - 1)]), range(count))

	def addTo(self, availableForGroup, item):
		availableForGroup = filter((lambda n: n == item, availableForGroup))
		return item

	#I don't get this function: one of the parameters is adjusted in the function
	def getRandomIndividuals(self, freqs):
		index = random.randint(0, len(freqs))
		scout = freqs[index]
		freqs = filter(lambda name: name == freqs[index], freqs)
		return scout

	#Gets the right number of random scout numbers
	def getIndividualScouts(self, ind, count):
		return map(lambda k: getRandomIndividuals(ind), range(count))

	def getScoutNumFromName(self, name, scoutsInRotation):
		return filter(lambda k: scoutsInRotation[k].get('mostRecentUser') == name, scoutsInRotation.keys())[0]

	def getOutOfRotationSpot(self, scoutRotatorDict, available):
		return filter(lambda k: scoutRotatorDict[k]["mostRecentUser"] in available, scoutRotatorDict.keys())[0]

	def findFirstEmptySpotForScout(self, scout, scoutRotatorDict, available):
		emptyScouts = filter(lambda k: scoutRotatorDict[k]['mostRecentUser'] == '', scoutRotatorDict.keys())
		return emptyScouts if len(emptyScouts) > 0 else self.getOutOfRotationSpot(scoutRotatorDict, available)

	def assignScoutsToRobots(self, scouts, available, currentTeams, scoutRotatorDict):
		teams = self.organizeScouts(available, currentTeams)
		map(lambda s: self.assignScoutToRobot(s, available, teams, scoutRotatorDict))
		return scoutRotatorDict

	def assignScoutToRobot(self, scout, available, teams, scoutRotatorDict):
		if scout in filter(lambda v: v.get('mostRecentUser') != "", scoutRotatorDict.values()):
			scoutRotatorDict[self.getScoutNumFromName(scout, scoutRotatorDict)].update({'team' : teams[scout]})
		else:
			num = self.findFirstEmptySpotForScout(scout, scoutRotatorDict, available)
			scoutRotatorDict[num].update({'team' : teams[scout], currentUser : 'scout'})
