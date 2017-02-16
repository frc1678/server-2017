import utils
import numpy as np
import CacheModel as cache
import itertools
import TBACommunicator
import Math
import random
import pyrebase
import numpy as np

# Scout Performance Analysis
class ScoutPrecision(object):
	"""docstring for ScoutPerformance"""
	def __init__(self):
		super(ScoutPrecision, self).__init__()
		self.sprs = {}
		self.robotNumToScouts = []
		self.TBAC = TBACommunicator.TBACommunicator()
		#These keys are the names of sections of the tempTIMDs on which scouts will be graded
		self.gradingKeys = [
			'numGearGroundIntakesTele',
			'numGearLoaderIntakesTele',
			'numGearsEjectedTele',
			'numGearsFumbledTele',
			'didLiftoff',
			'didBecomeIncapacitated',
			'didStartDisabled',
			'didReachBaselineAuto',
			'numHoppersOpenedAuto',
			'numHoppersOpenedTele'
		]
		self.gradingDicts = [
			'gearsPlacedByLiftTele',
			'gearsPlacedByLiftAuto'
		]
		self.gradingListsOfDicts = [
			'highShotTimesForBoilerTele',
			'highShotTimesForBoilerAuto',
			'lowShotTimesForBoilerAuto',
			'lowShotTimesForBoilerTele'
		]

	#outputs list of TIMDs that an inputted scout was involved in
	def getTotalTIMDsForScoutName(self, scoutName, tempTIMDs):
		return len(filter(lambda v: v.get('scoutName') == scoutName, tempTIMDs.values()))

	#finds keys that start the same way and groups their values into lists under the keys
	#Used to combine tempTIMDs of the same match by different scouts
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
		#finds scout names in tempTIMDs
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs))
		#finds values (at an inputted key) in tempTIMDs
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		#These 2 lines find the most common value in the list of values, or a random one if they occur in equal frequency
		valueFrequencies = map(values.count, values)
		if len(values) != 0:
			commonValue = values[valueFrequencies.index(max(valueFrequencies))]
			#If less than half of the values agree, the best estimate is the average
			if values.count(commonValue) <= len(values) / 2 and type(commonValue) != str:
				commonValue = np.mean(values)
			#makes a list of the differences from the common value
			differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
			#adds the difference from this tempTIMDs to each scout's previous differences
			self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	#Similar to findOddScoutForDataPoint, but for each data point inside of a dict
	def findOddScoutForDict(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs))
		dicts = filter(lambda k: k!= None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		# This section groups keys of the dicts found earlier
		if len(dicts) != 0:
			consolidationDict = {}
			for key in dicts[0].keys():
				consolidationDict[key] = []
				for aDict in dicts:
					consolidationDict[key] += [aDict[key]]
			#see descriptions in findOddScoutForDataPoint for this section
			for key in consolidationDict.keys():
				values = consolidationDict[key]
				valueFrequencies = map(values.count, values)
				commonValue = values[valueFrequencies.index(max(valueFrequencies))]
				if values.count(commonValue) <= len(values) / 2 and type(commonValue) != str:
					commonValue = np.mean(values)
				differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
				self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	#Similar to findOddScoutForDict, but for lists of several dicts instead of individual dicts
	def findOddScoutForListOfDicts(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs))
		lists = filter(lambda k: k!= None, map(lambda t: t.get(key) if t.get('scoutName') != None else None, tempTIMDs))
		#Finds the most largest of dicts within each list in the larger list (within each scout's observations)
		#(i.e. if there is disagreement over how many shots a robot took)
		if len(lists) > 0:
			largestListLength = max(map(lambda x: len(x), lists))
		else:
			largestListLength = 0
		#If someone missed a dict (for a shot) (that is, they did not include one that another scout did), this makes one with no values
		for aScout in lists:
			if len(aScout) < largestListLength:
				aScout += [{'numShots': 0, 'position': 0, 'time': 0}] * (largestListLength - len(aScout))
		for num in range(largestListLength):
			#comparing dicts that should be the same (e.g. each shot time dict for the same shot) within the tempTIMDs
			#This means comparisons such as the first shot in teleop by a given robot, as recorded by multiple scouts
			#The actual comparison is the same as the other findOddScout functions
			dicts = [lis[num] for lis in lists]
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
					if values.count(commonValue) <= len(values) / 2:
						commonValue = np.mean(values)
					differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
					self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	def calculateScoutPrecisionScores(self, temp, available):
		if temp != None:
			#Put together all tempTIMDs for the same match
			g = self.consolidateTIMDs(temp)
			#Removes any data from previous calculations from sprs
			self.sprs = {}
			#These three grade each scout for each of the values in the grading keys, dicts, and lists of dicts
			#Each scout gets more "points" if they are further off from the consensus on the actual values
			#The grades are stored in sprs
			#see the findOddScout functions for details on how
			[self.findOddScoutForDataPoint(v, k) for v in g.values() for k in self.gradingKeys]
			[self.findOddScoutForDict(v, k) for v in g.values() for k in self.gradingDicts]
			[self.findOddScoutForListOfDicts(v, k) for v in g.values() for k in self.gradingListsOfDicts]
			#divides values for scouts by number of TIMDs the scout has participated in
			self.sprs = {k:((v/float(self.getTotalTIMDsForScoutName(k, temp))) or 0) for (k,v) in self.sprs.items()}
			#any team without and sprs score is set to the average score
			for a in available:
				if a not in self.sprs.keys():
					avgScore = np.mean(self.sprs.values())
					self.sprs[a] = avgScore
		#If there are no tempTIMDs, everyone is set to 1
		else:
			for a in available:
				self.sprs[a] = 1

	#sorts scouts by sprs score
	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	#orders available scouts by spr ranking, then makes a list of how frequently each scout should be selected
	#better (lower scoring) scouts appear more frequently
	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		#It is reversed so the scouts with lower spr are later, causing them to be repeated more
		rankedScouts.reverse()
		#lower sprs, so higher number list index scouts are repeated more frequently, but less if there are more scouts
		func = lambda s: [s] * (rankedScouts.index(s) + 1) * ((100/(len(rankedScouts) + 1)) + 1)
		return utils.extendList(map(func, available))

	def organizeScouts(self, available, currentTeams, scoutSpots):
		#picks a random member of the inputted group
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)]
		#creates list of groupings that the scouts could be in, with as many scouts as are available and have spaces
		grpCombos = utils.sum_to_n(min(len(available), scoutSpots), 6, 3)
		grpCombosList = [combo for combo in grpCombos]
		#picks a random grouping of scouts that, if possible, doesn't have 2 scouts to a robot
		if len(filter(lambda l: 2 not in l, grpCombosList)) > 0:
			scoutsPGrp = groupFunc(filter(lambda l: 2 not in l, grpCombosList))
		else:
			scoutsPGrp = groupFunc(grpCombosList)
		scoutsPGrp.reverse()
		#used to make better scouts more likely to be picked
		freqs = self.getScoutFrequencies(available)
		#Gets the scouts who are alone on a robot
		#Note: This setup makes better scouts more likely to scout alone, since lonely scouts are picked from the list first
		indScouts = self.getIndividualScouts(freqs, scoutsPGrp.count(1))
		unusedScouts = filter(lambda s: s not in indScouts, available)
		nonIndScouts = []
		#gets and groups the scouts who are paired or in threes for a robot
		for c in scoutsPGrp[len(indScouts):]:
			newGroup = self.group(unusedScouts, c)
			nonIndScouts += [newGroup[0]]
			unusedScouts = newGroup[1]
		scouts = indScouts + nonIndScouts
		scoutsList = indScouts + utils.extendList(nonIndScouts)
		#returns the scouts paired to robots, and a list of which scouts are used
		return (self.scoutsToRobotNums(scouts, currentTeams), scoutsList)

	#assigns a list of scouts to a list of robots in order, and returns as a single dict
	def scoutsToRobotNums(self, scouts, currentTeams):
		f = lambda s: {scouts[s] : currentTeams[s]} if type(scouts[s]) != list else self.mapKeysToValue(scouts[s], currentTeams[s])
		scoutAndNums  = map(f, range(len(scouts)))
		return {k : v for l in scoutAndNums for k, v in l.items()}

	#Makes a dict with an inputted key attached to a value
	def mapKeysToValue(self, keys, value):
		return {k : value for k in keys}

	#picks an inputted number of random non-repeating members for a group, and also returns the list of members not picked
	def group(self, availableForGroup, count):
		toReturn = []
		for num in range(count):
			newMember = availableForGroup[random.randint(0, len(availableForGroup) - 1)]
			availableForGroup = filter(lambda m: m != newMember, availableForGroup)
			toReturn += [newMember]
		return (toReturn, availableForGroup)

	#gets a scout from the dict inputted, and a list of scouts not yet picked
	def getRandomIndividuals(self, freqs):
		index = random.randint(0, len(freqs) - 1)
		scout = freqs[index]
		freqs = filter(lambda name: name != scout, freqs)
		return (scout, freqs)

	#Gets the right number of random scouts without repetition
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
		emptyScouts = filter(lambda k: scoutRotatorDict[k].get('currentUser') == None or scoutRotatorDict[k].get ('currentUser') == "", scoutRotatorDict.keys())
		return emptyScouts[0]

	#Updates a dict going to firebase with information about scouts for the next match
	def assignScoutsToRobots(self, available, currentTeams, scoutRotatorDict):
		scoutsWithNames = filter(lambda v: v.get('currentUser') != (None or ''), scoutRotatorDict.values())
		namesOfScouts = map(lambda v: v.get('currentUser'), scoutsWithNames)
		scoutSpots = len(scoutRotatorDict.keys())
		#assigns available scouts to robots, and shows exactly which availabe scouts will be scouting
		calcTeams = self.organizeScouts(available, currentTeams, scoutSpots)
		teams = calcTeams[0]
		available = calcTeams[1]
		#Moves the current user to the previous user spot, assigns a new user if necessary, and assigns a robot to each scout
		for scout in scoutRotatorDict.keys():
			#The current user is now the previous user, as the match has changed
			if scoutRotatorDict[scout].get('currentUser') != None:
				oldName = scoutRotatorDict[scout]['currentUser']
				scoutRotatorDict[scout].update({'mostRecentUser': oldName})
				if oldName not in available:
					#If they are not scouting again, team and current user are deleted, since either that scout spot will be empty this match or someone else will be put there
					scoutRotatorDict[scout].update({'team': None, 'currentUser': None})
		for scout in available:
			#Each available scout is put into the dict to send to firebase, in an appropriate spot and with a team number
			scoutRotatorDict = self.assignScoutToRobot(scout, teams, scoutRotatorDict, available, namesOfScouts)
		return scoutRotatorDict

	#Finds a spot and a robot for an inputted available scout
	def assignScoutToRobot(self, availableScout, teams, scoutRotatorDict, available, names):
		#If the available scout already has a spot on firebase, all that needs to be updated is the robot they scout for
		if availableScout in names:
			scoutNum = self.getScoutNumFromName(availableScout, scoutRotatorDict)
			scoutRotatorDict[scoutNum].update({'team': teams[availableScout], 'currentUser': availableScout})
		else:
			#If they aren't, it needs to find an empty scout spot in firebase and put the available scout there
			newSpace = self.findFirstEmptySpotForScout(scoutRotatorDict, available)
			scoutRotatorDict[newSpace].update({'team': teams[availableScout], 'currentUser': availableScout})
		return scoutRotatorDict
