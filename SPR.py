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
		#These keys are the names of sections of the tempTIMDs on which scouts will be graded
		self.gradingKeys = [
			'numGearGroundIntakesTele',
			'numGearLoaderIntakesTele',
			'numGearsEjectedTele',
			'numGearsFumbledTele',
			'didLiftoff',
			'didBecomeIncapacitated',
			'didStartDisabled',
			'didReachBaselineAuto'
		]

		self.gradingDicts = [
			'gearsPlacedByLiftTele',
			'gearsPlacedByLiftAuto',
			'hoppersOpenedTele',
			'hoppersOpenedAuto'
		]
		self.gradingListsOfDicts = [
			'highShotTimesForBoilerTele',
			'highShotTimesForBoilerAuto',
			'lowShotTimesForBoilerAuto',
			'lowShotTimesForBoilerTele'
		]

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
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs
		values = filter(lambda v: v != None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs)) 		#finds values (at an inputted key) in tempTIMDs
		commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0 		#gets the most common value at the inputted key
		if values.count(commonValue) <= len(values) / 2:
			commonValue = np.mean(values)		#If less than half of the values agree, the best estimate is the average
		differenceFromCommonValue = map(lambda v: abs(v - commonValue), values) 		#makes a list of the differences from the common value
		self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})		#adds the difference from this tempTIMDs to each scout's previous differences

	def findOddScoutForDict(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs)) 		#finds scout names in tempTIMDs
		dicts = filter(lambda k: k!= None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs)) #Finds dicts of an inputted type in the tempTIMDs
		consolidationDict = {} # This section groups keys of the dicts found earlier
		for key in dicts[0].keys():
			consolidationDict[key] = []
			for aDict in dicts:
				consolidationDict[key] += [aDict[key]]
		for key in consolidationDict.keys():
			values = consolidationDict[key] #see descriptions in findOddScoutForDataPoint for the math that this section does
			commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0
			if values.count(commonValue) <= len(values) / 2:
				commonValue = np.mean(values)
			differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
			self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	#Exactly the same as findOddScoutForDict, but for each dict in a list of dicts
	def findOddScoutForListOfDicts(self, tempTIMDs, key):
		scouts = filter(lambda v: v != None, map(lambda k: k.get('scoutName'), tempTIMDs))
		lists = filter(lambda k: k!= None, map(lambda t: t[key] if t.get('scoutName') != None else None, tempTIMDs))
		for num in range(len(lists[0])):
			#comparing dicts that should be the same (e.g. each shot time dict for the same shot) within the tempTIMDs
			#This means comparisons such as the first shot in teleop by a given robot, as recorded by multiple scouts
			dicts = [lis[num] for lis in lists]
			consolidationDict = {}
			for key in dicts[0].keys():
				consolidationDict[key] = []
				for aDict in dicts:
					consolidationDict[key] += [aDict[key]]
			for key in consolidationDict.keys():
				values = consolidationDict[key]
				commonValue = max(map(lambda v: values.count(v), values)) if len(map(lambda v: values.count(v), values)) != 0 else 0
				if values.count(commonValue) <= len(values) / 2 and type(commonValue) != str:
					commonValue = np.mean(values)
				differenceFromCommonValue = map(lambda v: abs(v - commonValue), values)
				self.sprs.update({scouts[c] : (self.sprs.get(scouts[c]) or 0) + differenceFromCommonValue[c] for c in range(len(differenceFromCommonValue))})

	def calculateScoutPrecisionScores(self, temp, available):
		if temp != None:
			#Put together all tempTIMDs for the same match
			g = self.consolidateTIMDs(temp)
			#These three grade each scout for each of the values in the grading keys, dicts, and lists of dicts
			#Each scout gets more "points" if they are further off from the consensus on the actual values
			#The grades are stored in sprs
			#see the findOddScout functions for details on how
			[self.findOddScoutForDataPoint(v, k) for v in g.values() for k in self.gradingKeys]
			[self.findOddScoutForDict(v, k) for v in g.values() for k in self.gradingDicts]
			[self.findOddScoutForListOfDicts(v, k) for v in g.values() for k in self.gradingListsOfDicts]
			self.sprs = {k:(v/float(self.getTotalTIMDsForScoutName(k, temp))) for (k,v) in self.sprs.items()} 		#divides values for scouts by number of TIMDs the scout has participated in
			for a in available: 		#any team without and sprs score is set to the average score
				if a not in self.sprs.keys():
					self.sprs[a] = np.mean(self.sprs.values())
		#If there are no tempTIMDs, everyone is set to 1
		else:
			for a in available:
				self.sprs[a] = 1

	#sorts scouts by sprs score
	def rankScouts(self, available):
		return sorted(self.sprs.keys(), key=lambda k: self.sprs[k])

	#orders available scouts by spr ranking, then makes a list of how frequently each scout should be selected
	#(better (lower scoring) scouts more frequently)
	def getScoutFrequencies(self, available):
		rankedScouts = self.rankScouts(available)
		#It is reversed so the scouts with lower spr are later, causing them to be repeated more
		rankedScouts.reverse()
		func = lambda s: [s] * (rankedScouts.index(s) + 1) * ((100/(len(rankedScouts))) + 1)
		return utils.extendList(map(func, available))

	def organizeScouts(self, available, currentTeams, scoutSpots):
		groupFunc = lambda l: l[random.randint(0, len(l) - 1)] 		#picks a random member of the inputted group
		grpCombos = utils.sum_to_n(min(len(available), scoutSpots), 6, 3) #creates list of groupings that the scouts could be in, with as many scouts as are available and have spaces
		grpCombosList = [combo for combo in grpCombos]
		if len(filter(lambda l: 2 not in l, grpCombosList)) > 0: #picks a random grouping of scouts that, if possible, doesn't have 2 scouts to a robot
			scoutsPGrp = groupFunc(filter(lambda l: 2 not in l, grpCombosList))
		else:
			scoutsPGrp = groupFunc(grpCombosList)
		scoutsPGrp.reverse()
		freqs = self.getScoutFrequencies(available) #used to make better scouts more likely to be picked
		indScouts = self.getIndividualScouts(freqs, len(filter(lambda x: x == 1, scoutsPGrp)))	#Gets the scouts who are alone on a robot
		unusedScouts = filter(lambda s: s not in indScouts, available)
		nonIndScouts = []
		for c in scoutsPGrp[len(indScouts):]: #gets and groups the scouts who are paired or in threes for a robot
			newGroup = self.group(unusedScouts, c)
			nonIndScouts += [newGroup[0]]
			unusedScouts = newGroup[1]
		scouts = indScouts + nonIndScouts
		scoutsList = indScouts + utils.extendList(nonIndScouts)
		return (self.scoutsToRobotNums(scouts, currentTeams), scoutsList) #returns the scouts paired to robots, and which scouts are used

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

	#gets a scout from the dict inputted, and then makes them unable to be picked again
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

	def assignScoutsToRobots(self, available, currentTeams, scoutRotatorDict):
		scoutsWithNames = filter(lambda v: v.get('currentUser') != None, scoutRotatorDict.values())
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
