import utils
import numpy as np
import CacheModel as cache
import itertools
import TBACommunicator
import Math
import random
import pdb
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
			'numGearGroundIntakesTele' : 1,
			'numGearLoaderIntakesTele' : 1,
			'numGearsEjectedTele' : 1,
			'numGearsFumbledTele' : 1,
			'didLiftoff' : 1,
			'didBecomeIncapacitated' : 1,
			'didStartDisabled' : 1,
			'didReachBaselineAuto' : 1
		}

		self.dictsToPointValues = {
			'gearsPlacedByLiftTele' : 1,
			'gearsPlacedByLiftAuto' : 1,
			'hoppersOpenedTele' : 1,
			'hoppersOpenedAuto' : 1
		}
		self.listsOfDictsToPointValues = {
			'highShotTimesForBoilerTele' : 1,
			'highShotTimesForBoilerAuto' : 1,
			'lowShotTimesForBoilerAuto' : 1,
			'lowShotTimesForBoilerTele' : 1
		}

	#outputs list of TIMDs that an inputted scout was involved in
	def getTotalTIMDsForScoutName(self, scoutName, tempTIMDs):
		return len(map(lambda v: v.get('scoutName') == scoutName, tempTIMDs.values()))

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

	def findOddScoutForDict(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs that aren't None
		dicts = filter(lambda k: k!= None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		consolidationDict = {}
		for key in dicts[0].keys():
			consolidationDict[key] = []
			for aDict in dicts:
				consolidationDict[key] += [aDict[key]]
		commonValues = {}
		for key in consolidationDict.keys():
			values = consolidationDict[key]
			commonValues[key] = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0
			if not values.count(commonValues[key]) > len(values) / 2: commonValues[key] = np.mean(values)
			differenceFromCommonValue = map(lambda v: abs(v - commonValues[key]), values)
			self.sprs = {scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))}

	def findOddScoutForListOfDicts(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs that aren't None
		lists = filter(lambda k: k!= None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		for dicts in lists:
			consolidationDict = {}
			for key in dicts[0].keys():
				consolidationDict[key] = []
				for aDict in dicts:
					consolidationDict[key] += [aDict[key]]
			commonValues = {}
			for key in consolidationDict.keys():
				values = consolidationDict[key]
				commonValues[key] = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0
				if not values.count(commonValues[key]) > len(values) / 2: commonValues[key] = np.mean(values)
				differenceFromCommonValue = map(lambda v: abs(v - commonValues[key]), values)
				self.sprs = {scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))}

	def calculateScoutPrecisionScores(self, temp, available):
		if temp != None:
			g = self.consolidateTIMDs(temp)
			[self.findOddScoutForDataPoint(v, k) for v in g.values() for k in self.keysToPointValues.keys()] #Sets sprs
			[self.findOddScoutForDict(v, k) for v in g.values() for k in self.dictsToPointValues.keys()]
			[self.findOddScoutForListOfDicts(v, k) for v in g.values() for k in self.listsOfDictsToPointValues.keys()]
			self.sprs = {k:(v/float(self.getTotalTIMDsForScoutName(k, temp))) for (k,v) in self.sprs.items()} 		#divides values for scouts by cycle, and then by number of TIMDs
			for a in available[:18]: 		#for the first 18 available scouts
				if a not in self.sprs.keys(): 			#If their values are 1 (which I assume is automatic until they are updated) and they are not in use in sprs
					self.sprs[a] = np.mean(self.sprs.values()) 				#They are now set to the average value
		else:
			for a in available:
				self.sprs[a] = 1

	#sorts scouts by sprs score
	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	#orders available scouts by spr ranking, then makes a list of how frequently each scout should be selected (better scouts more frequently)
	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		func = lambda s: [s] * (rankedScouts.index(s) + 1) * ((100/(len(rankedScouts))) + 1)
		return utils.extendList(map(func, available))

	def organizeScouts(self, available, currentTeams):
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)] 		#picks a random member of the inputted group
		grpCombos = utils.sum_to_n(len(available), 6, 3) #creates list of groupings that the scouts could be in
		grpCombosList = [combo for combo in grpCombos]
		if len(filter(lambda l: 2 not in l, grpCombosList)) > 0: #picks a random grouping of scouts that, if possible, doesn't have 2 scouts to a robot
			scoutsPGrp = groupFunc(filter(lambda l: 2 not in l, grpCombosList))
		else:
			scoutsPGrp = groupFunc(grpCombosList)
		scoutsPGrp.reverse()
		freqs = self.getScoutFrequencies(available)
		indScouts = self.getIndividualScouts(freqs, len(filter(lambda x: x == 1, scoutsPGrp)))	#Gets the scouts who are alone on a robot
		unusedScouts = filter(lambda s: s not in indScouts, available)
		nonIndScouts = []
		for c in scoutsPGrp[len(indScouts):]: #gets and groups the scouts who are paired or in threes for a robot
			newGroup = self.group(unusedScouts, c)
			nonIndScouts += [newGroup[0]]
			unusedScouts = newGroup[1]
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
		toReturn = []
		for num in range(count):
			newMember = availableForGroup[random.randint(0, len(availableForGroup) - 1)]
			availableForGroup = filter(lambda m: m != newMember, availableForGroup)
			toReturn += [newMember]
		return (toReturn, availableForGroup)

	#gets a scout from the dict inputted, and then makes them less likely to be picked again
	def getRandomIndividuals(self, freqs):
		index = random.randint(0, len(freqs) - 1)
		scout = freqs[index]
		freqs = filter(lambda name: name != scout, freqs)
		return (scout, freqs)

	#Gets the right number of random scouts
	def getIndividualScouts(self, ind, count):
		scouts = []
		unused = ind
		for num in range(count):
			random = self.getRandomIndividuals(unused)
			unused = random[1]
			scouts += [random[0]]
		return scouts

	def getScoutNumFromName(self, name, scoutsInRotation):
		return filter(lambda k: scoutsInRotation[k].get('mostRecentUser') == name, scoutsInRotation.keys())[0]

	#Returns the first scout key that doesn't have a current user
	def findFirstEmptySpotForScout(self, scoutRotatorDict, available):
		emptyScouts = filter(lambda k: scoutRotatorDict[k].get('currentUser') != None, scoutRotatorDict.keys())
		return emptyScouts[0]

	def assignScoutsToRobots(self, available, currentTeams, scoutRotatorDict):
		scoutsWithNames = filter(lambda v: v.get('currentUser') != None, scoutRotatorDict.values())
		namesOfScouts = map(lambda v: v.get('currentUser'), scoutsWithNames)
		#assigns scout numbers to robots
		teams = self.organizeScouts(available, currentTeams)
		#Moves the current user to the previous user spot, assigns a new user if necessary, and assigns a robot to each scout
		for scout in scoutRotatorDict.keys():
			if scoutRotatorDict[scout].get('currentUser') != None:
				oldName = scoutRotatorDict[scout]['currentUser']
				scoutRotatorDict[scout].update({'mostRecentUser': oldName})
				if oldName not in available:
					scoutRotatorDict[scout].update({'team': None, 'currentUser': None})
		for scout in available:
			scoutRotatorDict = self.assignScoutToRobot(scout, teams, scoutRotatorDict, available, namesOfScouts)
		return scoutRotatorDict

	def assignScoutToRobot(self, availableScout, teams, scoutRotatorDict, available, names):
		if availableScout in names:
			scoutNum = self.getScoutNumFromName(availableScout, scoutRotatorDict)
			scoutRotatorDict[scoutNum].update({'team': teams[availableScout], 'currentUser': availableScout})
		else:
			newSpace = self.findFirstEmptySpotForScout(scoutRotatorDict, available)
			print newSpace
			scoutRotatorDict[newSpace].update({'team': teams[availableScout], 'currentUser': availableScout})
		return scoutRotatorDict
