import utils
import CacheModel as cache
import Math
import random
import numpy as np
import scipy.stats as stats
import CSVExporter

# Scout Performance Analysis
class ScoutPrecision(object):
	"""docstring for ScoutPerformance"""
	def __init__(self):
		super(ScoutPrecision, self).__init__()
		self.sprs = {}
		self.robotNumToScouts = []
		#These keys are the names of sections of the tempTIMDs on which scouts will be graded
		self.gradingKeys = {
			'numGearGroundIntakesTele': 1.0,
			'numGearLoaderIntakesTele': 1.0,
			'numGearsEjectedTele': 1.0,
			'numGearsFumbledTele': 1.0,
			'didLiftoff': 3.0,
			'didBecomeIncapacitated': 2.0,
			'didStartDisabled': 2.0,
			'didReachBaselineAuto': 1.5,
			'numHoppersOpenedAuto': 1.5,
			'numHoppersOpenedTele': 1.5
		}
		self.gradingDicts = {
			'gearsPlacedByLiftTele': 1.2,
			'gearsPlacedByLiftAuto': 1.3
		}
		self.gradingListsOfDicts = {
			'highShotTimesForBoilerTele': 0.2,
			'highShotTimesForBoilerAuto': 0.2,
			'lowShotTimesForBoilerAuto': 0.1,
			'lowShotTimesForBoilerTele': 0.1
		}

	#SPR
	#Scout precision ranking: checks accuracy of scouts by comparing their previous TIMDs to the consensus

	#outputs list of TIMDs that an inputted scout was involved in
	def getTotalTIMDsForScoutName(self, scoutName, tempTIMDs):
		return len(filter(lambda v: v.get('scoutName') == scoutName, tempTIMDs.values()))

	#finds keys that start the same way and groups their values into lists under the keys
	#Used to combine tempTIMDs for the same match by different scouts
	def consolidateTIMDs(self, temp):
		consolidationGroups = {}
		for k, v in temp.items():
			key = k.split('-')[0]
			if key in consolidationGroups.keys():
				consolidationGroups[key].append(v)
			else:
				consolidationGroups[key] = [v]
		return consolidationGroups

	#Note: the next 3 functions compare data in tempTIMDs to find scout accuracy
	#The actual comparison to determine correct values is done in dataChecker

	def findOddScoutForDataPoint(self, tempTIMDs, key):
		weight = self.gradingKeys[key]
		#finds scout names in tempTIMDs
		scouts = filter(lambda v: v, map(lambda k: k.get('scoutName'), tempTIMDs))
		#finds values (at an inputted key) in tempTIMDs
		values = filter(lambda v: v, map(lambda t: t[key] if t.get('scoutName') else None, tempTIMDs))
		#These 2 lines find the most common value in the list of values, or a random one if they occur in equal frequency
		valueFrequencies = map(values.count, values)
		if values:
			commonValue = values[valueFrequencies.index(max(valueFrequencies))]
			#If less than half of the values agree, the best estimate is the average
			if values.count(commonValue) <= len(values) / 2 and type(commonValue) != str:
				commonValue = np.mean(values)
			#makes a list of the differences from the common value
			differenceFromCommonValue = map(lambda v: abs(v - commonValue) * weight, values)
			#adds the difference from this tempTIMD for this value to each scout's previous differences (spr score)
			self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	#Similar to findOddScoutForDataPoint, but for each data point inside of a dict
	def findOddScoutForDict(self, tempTIMDs, key):
		weight = self.gradingDicts[key]
		scouts = filter(lambda v: v, map(lambda k: k.get('scoutName'), tempTIMDs))
		dicts = filter(lambda k: k, map(lambda t: t[key] if t.get('scoutName') else None, tempTIMDs))
		#This section groups keys of the dicts found earlier
		if dicts:
			consolidationDict = {}
			for key in dicts[0].keys():
				consolidationDict[key] = []
				for aDict in dicts:
					consolidationDict[key] += [aDict[key]]
			#see descriptions in findOddScoutForDataPoint for this section (comparing data on each key)
			for key in consolidationDict.keys():
				values = consolidationDict[key]
				valueFrequencies = map(values.count, values)
				commonValue = values[valueFrequencies.index(max(valueFrequencies))]
				if values.count(commonValue) <= len(values) / 2 and type(commonValue) != str:
					commonValue = np.mean(values)
				differenceFromCommonValue = map(lambda v: abs(v - commonValue) * weight, values)
				self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	#Similar to findOddScoutForDict, but for lists of several dicts instead of individual dicts
	#The nth dict on each list should be the same
	def findOddScoutForListOfDicts(self, tempTIMDs, key):
		weight = self.gradingListsOfDicts[key]
		scouts = filter(lambda v: v, map(lambda k: k.get('scoutName'), tempTIMDs))
		lists = filter(lambda k: k, map(lambda t: t.get(key) if t.get('scoutName') else None, tempTIMDs))
		#Finds the most largest of dicts within each list in the larger list (within each scout's observations)
		#(i.e. if there is disagreement over how many shots a robot took)
		if lists:
			largestListLength = max(map(lambda x: len(x), lists))
			#If someone missed a dict (for a shot) (that is, they did not include one that another scout did), this makes one with no values
			for aScout in lists:
				if len(aScout) < largestListLength:
					aScout += [{'numShots': 0, 'position': 'Other', 'time': 0}] * (largestListLength - len(aScout))
			for num in range(largestListLength):
				#comparing dicts that should be the same (e.g. each shot time dict for the same shot) within the tempTIMDs
				#This means the nth shot by a given robot, as recorded by multiple scouts
				#The comparison itself is the same as the other findOddScout functions
				dicts = [lis[num] for lis in lists]
				consolidationDict = {}
				for key in dicts[0].keys():
					consolidationDict[key] = []
					for aDict in dicts:
						consolidationDict[key] += [aDict[key]]
				for key in consolidationDict.keys():
					#position is a string, so should not be compared, due to the averaging later
					#without averaging, one person could be declared correct for no reason
					if key != 'position':
						values = consolidationDict[key]
						valueFrequencies = map(values.count, values)
						commonValue = values[valueFrequencies.index(max(valueFrequencies))]
						if values.count(commonValue) <= len(values) / 2:
							commonValue = np.mean(values)
						differenceFromCommonValue = map(lambda v: abs(v - commonValue) * weight, values) 
						self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	def calculateScoutPrecisionScores(self, temp, available):
		if temp:
			#Combines all tempTIMDs for the same match
			g = self.consolidateTIMDs(temp)
			#Removes any data from previous calculations from sprs
			self.sprs = {}
			#These three grade each scout for each of the values in the grading keys, dicts, and lists of dicts
			#Each scout gets more "points" if they are further off from the consensus on the actual values
			#The grades are stored by scout name in sprs
			#see the findOddScout functions for details on how
			[self.findOddScoutForDataPoint(v, k) for v in g.values() for k in self.gradingKeys.keys()]
			[self.findOddScoutForDict(v, k) for v in g.values() for k in self.gradingDicts.keys()]
			[self.findOddScoutForListOfDicts(v, k) for v in g.values() for k in self.gradingListsOfDicts.keys()]
			#divides values for scouts by number of TIMDs the scout has participated in
			#if a scout is in more matches, they will likely have more disagreements, but the same number per match if they are equally accurate
			self.sprs = {k:((v/float(self.getTotalTIMDsForScoutName(k, temp))) or 0) for (k,v) in self.sprs.items()}
			#any team without and sprs score is set to the average score
			for a in available:
				if a not in self.sprs.keys():
					avgScore = np.mean(self.sprs.values()) if self.sprs else 1
					self.sprs[a] = avgScore
		#If there are no tempTIMDs, everyone is set to 1
		else:
			for a in available:
				self.sprs[a] = 1

	#Scout Assignment

	#sorts scouts by spr score
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
		#creates list of groupings that the scouts could be in, with as many scouts as are available and have spaces, for 6 robots with a max group size of 3
		grpCombos = utils.sum_to_n(min(len(available), scoutSpots), 6, 3)
		grpCombosList = [combo for combo in grpCombos]
		#picks a random grouping of scouts that, if possible, doesn't have 2 scouts to a robot
		singleTripleCombos = filter(lambda l: 2 not in l, grpCombosList)
		if len(singleTripleCombos) > 0:
			scoutsPGrp = groupFunc(singleTripleCombos)
		else:
			scoutsPGrp = groupFunc(grpCombosList)
		#Since scout groups are reversed, smaller groups come first, so are picked first, so tend to have better scouts
		scoutsPGrp.reverse()
		#used to make better scouts more likely to be picked
		freqs = self.getScoutFrequencies(available)
		scouts = []
		#Chooses the correct number of nonrepeating scouts for each group of scouts (of size 1, 2, or 3)
		for c in scoutsPGrp:
			newGroup = self.group(freqs, c)
			scouts += [newGroup[0]]
			freqs = newGroup[1]
		#returns the scouts grouped and paired to robots
		return self.scoutsToRobotNums(scouts, currentTeams)

	#assigns a list of scouts to a list of robots in order, and returns as a single dict
	def scoutsToRobotNums(self, scouts, currentTeams):
		f = lambda s: {scouts[s] : currentTeams[s]} if type(scouts[s]) != list else self.mapKeysToValue(scouts[s], currentTeams[s])
		scoutAndNums = map(f, range(len(scouts)))
		return {k : v for l in scoutAndNums for k, v in l.items()}

	#Makes a dict with the same value attached to each inputted key
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

	#picks a random member of a group, and also returns a list of mambers not picked
	def getRandomIndividuals(self, freqs):
		index = random.randint(0, len(freqs) - 1)
		scout = freqs[index]
		freqs = filter(lambda name: name != scout, freqs)
		return (scout, freqs)

	def getScoutNumFromName(self, name, scoutsInRotation):
		return filter(lambda k: scoutsInRotation[k].get('mostRecentUser') == name, scoutsInRotation.keys())[0]

	#Returns the first scout key that doesn't have a current user
	def findFirstEmptySpotForScout(self, scoutRotatorDict, available):
		emptyScouts = filter(lambda k: scoutRotatorDict[k].get('currentUser') == None or scoutRotatorDict[k].get('currentUser') == "" or scoutRotatorDict[k].get('currentUser') not in available, scoutRotatorDict.keys())
		return emptyScouts

	#Updates a dict going to firebase with information about scouts for the next match
	def assignScoutsToRobots(self, available, currentTeams, scoutRotatorDict):
		scoutsWithNames = filter(lambda v: v.get('currentUser') != (None or ''), scoutRotatorDict.values())
		namesOfScouts = map(lambda v: v.get('currentUser'), scoutsWithNames)
		scoutSpots = len(scoutRotatorDict.keys())
		#assigns available scouts to robots, and shows exactly which availabe scouts will be scouting
		teams = self.organizeScouts(available, currentTeams, scoutSpots)
		available = utils.extendListWithStrings(teams)
		#Moves the current user to the previous user spot, assigns a new user if necessary, and assigns a robot to each scout
		for scout in scoutRotatorDict.keys():
			#The current user is now the previous user, as the match has changed
			if scoutRotatorDict[scout].get('currentUser'):
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
			scoutRotatorDict[scoutNum].update({'team': teams[availableScout], 'currentUser': availableScout, 'scoutStatus': 'requested'})
		#If they don't, it needs to find an empty scout spot in firebase and put the available scout there (if there is an empty spot, which there always should be)
		elif self.findFirstEmptySpotForScout(scoutRotatorDict, available):
			newSpace = self.findFirstEmptySpotForScout(scoutRotatorDict, available)[0]
			scoutRotatorDict[newSpace].update({'team': teams[availableScout], 'currentUser': availableScout, 'scoutStatus': 'requested'})
		return scoutRotatorDict

	def sprZScores(self):
		zscores = {k : (0.0, self.sprs[k]) for k in self.sprs.keys()} if len(set(self.sprs.values())) == 1 else {k : (zscore, self.sprs[k]) for (k, zscore) in zip(self.sprs.keys(), stats.zscore(self.sprs.values()))}
		CSVExporter.CSVExportScoutZScores(zscores)
