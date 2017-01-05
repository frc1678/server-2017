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
		self.robotNumToScouts = {}
		self.TBAC = TBACommunicator.TBACommunicator()
		self.keysToPointValues = {
			"numHighShotsMadeAuto" : 1,
			"numLowShotsMadeAuto" : 1,
			"numHighShotsMadeTele" : 1,
			"numLowShotsMadeTele" : 1,
		}
		self.k = ["timesSuccessfulCrossedDefensesTele", 'timesSuccessfulCrossedDefensesAuto', 'timesFailedCrossedDefensesTele', 'timesFailedCrossedDefensesAuto']

	def filterToMultiScoutTIMDs(self):
		return filter(lambda tm: type(tm.scoutName) == list, self.comp.timds)

	def getAllScoutNames(self):
		return list(set([scout for array in map(lambda t: t.scoutName, filterToMultiScoutTIMDs()) for scout in array]))

	def getTotalTIMDsForScoutName(self, scoutName):
		return len(map(lambda v: v["scoutName"] == scoutName, tempTIMDs.values()))

	def findOddScoutForDataPoint(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs))
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0
		if not values.count(commonValue) > len(values) / 2: commonValue = np.mean(values)
		differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
		self.sprs = {scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))}

	def calculateScoutPrecisionScores(self, temp, available):
		self.sprs = {k:(v/float(self.cycle)/float(self.getTotalTIMDsForScoutName(k))) for (k,v) in self.sprs.items()}
		for a in available.keys()[:16]:
			if a not in self.sprs.keys() and available.get(a) == 1:
				self.sprs[a] = np.mean(self.sprs.values())

	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		func = lambda s: [s] * rankedScouts.index(i) * (100/(len(rankedScouts) - 1)) + 1
		return self.extendList(map(func, available))

	def organizeScouts(self, available, currentTeams, scoutsInRotation):
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)]
		scoutsPGrp = groupFunc(sum_to_n(len(available)))
		indScouts = self.getIndividualScouts(self.getScoutFrequencies(), len(filter(lambda x: x == 1, scoutsPGrp)))
		scouts = indScouts + map(lambda c: group(filter(lambda n: n in indScouts, available), scoutsPGrp[c]), c[len(indScouts):len(c)])
		scoutsToRobotNums(scouts, currentTeams)

	def scoutToRobotNums(self, scouts, currentTeams):
		f = lambda s: {scouts[s] : currentTeams[s]} if type(s) != list else mapKeysToValue(s, currentTeams[s])
		scoutAndNums  = map(f, range(len(scouts)))

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

	def assignScoutToRobot(self, scout, scoutRotatorDict):
		if scout in filter(lambda v: v.get('currentUser') != "", scoutRotatorDict.values()):
			scoutsInRotation[getScoutNumFromName(scout, scoutRotatorDict)].update({'team' : 1})
