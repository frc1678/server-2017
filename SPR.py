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

	def filterToMultiScoutTIMDs(self):
		return filter(lambda tm: type(tm.scoutName) == list, self.comp.timds)

	def getTotalTIMDsForScoutName(self, scoutName):
		return len(map(lambda v: v["scoutName"] == scoutName, tempTIMDs.values()))

	def consolidateTIMDs(self, temp):
		consolidationGroups = {}
		for k, v in temp.items():
			key = k.split('-')[0]
			if key in consolidationGroups.keys():
				consolidationGroups[key].append(v)
			else:
				consolidationGroups[key] = [v]
		return consolidationGroups

	def findOddScoutForDataPoint(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs))
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0
		if not values.count(commonValue) > len(values) / 2: commonValue = np.mean(values)
		differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
		self.sprs = {scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))}

	def calculateSPRs(self, temp):
		g = self.consolidateTIMDs(temp)
		[self.findOddScoutForDataPoint(v, key) for v in g.values() for key in v.keys() if key in v.keys()]
		for v in g.values():
			for key in v.keys():
				if key in self.keysToPointValues.keys():
					findOddScoutForDataPoint(v, key)

	def calculateScoutPrecisionScores(self, temp, available):
		self.calculateSPRs()
		self.sprs = {k:(v/float(self.cycle)/float(self.getTotalTIMDsForScoutName(k))) for (k,v) in self.sprs.items()}
		for a in available.keys()[:18]:
			if a not in self.sprs.keys() and available.get(a) == 1:
				self.sprs[a] = np.mean(self.sprs.values())

	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		func = lambda s: [s] * rankedScouts.index(i) * (100/(len(rankedScouts) - 1)) + 1
		return self.extendList(map(func, available))

	def organizeScouts(self, available, currentTeams):
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)]
		scoutsPGrp = groupFunc(sum_to_n(len(available)))
		indScouts = self.getIndividualScouts(self.getScoutFrequencies(), len(filter(lambda x: x == 1, scoutsPGrp)))
		scouts = indScouts + map(lambda c: group(filter(lambda n: n in indScouts, available), scoutsPGrp[c]), c[len(indScouts):len(c)])
		return scoutsToRobotNums(scouts, currentTeams)

	def scoutToRobotNums(self, scouts, currentTeams):
		f = lambda s: {scouts[s] : currentTeams[s]} if type(s) != list else self.mapKeysToValue(scouts[s], currentTeams[s])
		scoutAndNums  = map(f, range(len(scouts)))
		return {k : v for l in scoutAndNums for k, v in l.items()}

	def mapKeysToValue(self, keys, value):
		return {k : value for k in keys}

	def group(self, availableForGroup, count):
		return map(lambda n: addTo(availableForGroup, availableForGroup[random.randint(0, len(availableForGroup) - 1)]), range(count))

	def addTo(self, availableForGroup, item):
		availableForGroup = availableForGroup.filter(lambda n: n == item, availableForGroup)
		return item

	def getRandomIndividuals(self, freqs):
		index = random.randint(0, len(freqs), 1)
		scout = freqs[index]
		freqs = filter(lambda name: name == freqs[index], freqs)
		return scout

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

	def assignScoutToRobot(self, scout, available, teams, scoutRotatorDict):
		if scout in filter(lambda v: v.get('mostRecentUser') != "", scoutRotatorDict.values()):
			scoutRotatorDict[self.getScoutNumFromName(scout, scoutRotatorDict)].update({'team' : teams[scout]})
		else:
			num = self.findFirstEmptySpotForScout(scout, scoutRotatorDict, available)
			scoutRotatorDict[num].update({'team' : teams[scout], currentUser : 'scout'})
