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
		self.robotNumToScouts = []
		self.TBAC = TBACommunicator.TBACommunicator()
		#What do these do?
		self.keysToPointValues = {
			'numGearsPlacedTele' : 1,
			'numGearsPlacedAuto' : 1,
			'numHoppersOpenedAuto' : 1,
			'numHoppersOpenedTele' : 1
		}

		self.dictsToPointValues = {
			'highShotTimesForBoilerTele' : 1
		}

	#outputs list of TIMDs that an inputted scout was involved in
	def getTotalTIMDsForScoutName(self, scoutName):
		return len(map(lambda v: v["scoutName"] == scoutName, tempTIMDs.values()))

	#finds keys that start the same way and groups their values into lists under the keys
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
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs that aren't None
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs)) 		#finds values (at an inputted key) that aren't None frome scouts that aren't None in tempTIMDs
		commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0 		#gets the most common value in the list previously generated
		if not values.count(commonValue) > len(values) / 2: commonValue = np.mean(values)		#If less than half of the values agree, the best estimate is the average
		differenceFromCommonValue = map(lambda v: abs(v - commonValue), values) 		#makes a list of the differences from the common value
		self.sprs = {scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))}		#adds the difference from this tempTIMDs to each scout's previous differences

	def calculateScoutPrecisionScores(self, temp, available):
		g = self.consolidateTIMDs(temp)
		[self.findOddScoutForDataPoint(v, k) for v in g.values() for k in self.keysToPointValues.keys()] #Sets sprs
		self.sprs = {k:(v/float(self.getTotalTIMDsForScoutName(k))) for (k,v) in self.sprs.items()} 		#divides values for scouts by cycle, and then by number of TIMDs
		for a in available[:18]: 		#for the first 18 available scouts
			if a not in self.sprs.keys(): 			#If their values are 1 (which I assume is automatic until they are updated) and they are not in use in sprs
				self.sprs[a] = np.mean(self.sprs.values()) 				#They are now set to the average value

	#sorts scouts by sprs score
	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	#orders available scouts by spr ranking, then makes a list of how frequently each scout should be selected (better scouts more frequently)
	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		func = lambda s: [s] * rankedScouts.index(s) * ((100/(len(rankedScouts) - 1)) + 1)
		return utils.extendList(map(func, available))

	def organizeScouts(self, available, currentTeams):
		print available
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)] 		#picks a random member of the inputted group
		grpCombos = utils.sum_to_n(len(available), 6, 3) #creates list of groupings that the scouts could be in
		grpCombosList = [combo for combo in grpCombos]
		if len(filter(lambda l: 2 not in l, grpCombosList)) > 0: #picks a random grouping of scouts that, if possible, doesn't have 2 scouts to a robot
			scoutsPGrp = groupFunc(filter(lambda l: 2 not in l, grpCombosList))
		else:
			scoutsPGrp = groupFunc(grpCombosList)
		indScouts = self.getIndividualScouts(self.getScoutFrequencies(available), len(filter(lambda x: x == 1, scoutsPGrp)))	#Gets the scouts who are alone on a robot
		nonIndScouts = map(lambda c: self.group(filter(lambda n: n not in indScouts, available), scoutsPGrp[c]), scoutsPGrp[len(indScouts):]) #creates a list of scouts who are sharing robots
		scouts = indScouts + nonIndScouts
		return self.scoutsToRobotNums(scouts, currentTeams)

	def scoutsToRobotNums(self, scouts, currentTeams): 	#assigns a list of scouts to a list of robots in order, and returns as a single dict
		f = lambda s: {scouts[s] : currentTeams[s]} if type(scouts[s]) != list else self.mapKeysToValue(scouts[s], currentTeams[s])
		scoutAndNums  = map(f, range(len(scouts)))
		return {k : v for l in scoutAndNums for k, v in l.items()}

	def mapKeysToValue(self, keys, value): 	#Makes a dict with an inputted key attached to a value
		return {k : value for k in keys}

	#picks an inputted number of random members for a group
	def group(self, availableForGroup, count):
		return map(lambda n: self.addTo(availableForGroup, availableForGroup[random.randint(0, len(availableForGroup) - 1)]), range(count))

	#removes an inputted member from the group and returns it
	def addTo(self, availableForGroup, item):
		availableForGroup = filter(lambda n: n == item, availableForGroup)
		return item

	#gets a scout from the dict inputted, and then makes them less likely to be picked again
	def getRandomIndividuals(self, freqs):
		index = random.randint(0, len(freqs))
		scout = freqs[index]
		freqs = filter(lambda name: name != freqs[index], freqs)
		return scout

	#Gets the right number of random scouts
	def getIndividualScouts(self, ind, count):
		return map(lambda k: self.getRandomIndividuals(ind), range(count))

	def getScoutNumFromName(self, name, scoutsInRotation):
		return filter(lambda k: scoutsInRotation[k].get('mostRecentUser') == name, scoutsInRotation.keys())[0]

	#Picks the first scout on both the list and firebase
	def getOutOfRotationSpot(self, scoutRotatorDict, available):
		return filter(lambda k: scoutRotatorDict[k]["mostRecentUser"] in available, scoutRotatorDict.keys())[0]

	#If there are empty scouts in firebase (object, but no user), it gives them, otherwise just the first scout in firebase that is not empty
	def findFirstEmptySpotForScout(self, scout, scoutRotatorDict, available):
		emptyScouts = filter(lambda k: scoutRotatorDict[k]['mostRecentUser'] == '', scoutRotatorDict.keys())
		return emptyScouts if len(emptyScouts) > 0 else self.getOutOfRotationSpot(scoutRotatorDict, available)

	def assignScoutsToRobots(self, scouts, available, currentTeams, scoutRotatorDict):
		teams = self.organizeScouts(available, currentTeams)
		map(lambda s: self.assignScoutToRobot(s, available, teams, scoutRotatorDict), scouts)
		return scoutRotatorDict

	def assignScoutToRobot(self, scout, available, teams, scoutRotatorDict):
		#If the scout is in the existing list of scouts, this updates firebase with the team they were assigned to scout
		if scout in filter(lambda v: v.get('mostRecentUser') != "", scoutRotatorDict.values()):
			scoutRotatorDict[self.getScoutNumFromName(scout, scoutRotatorDict)].update({'team' : teams[scout]})
		#If the scout is not on the list, they are found a spot and added to firebase
		else:
			num = self.findFirstEmptySpotForScout(scout, scoutRotatorDict, available)
			scoutRotatorDict[num].update({'team' : teams[scout], 'currentUser' : scout})
