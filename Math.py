import math
from operator import attrgetter
import pdb

import numpy as np
import scipy as sp
import scipy.stats as stats

import CacheModel as cache
import DataModel
import utils
import time
import TBACommunicator
from teamCalcDataKeysToLambda import *

import multiprocessing
import warnings
from FirstTIMDProcess import FirstTIMDProcess
from FirebaseWriterProcess import FirebaseWriteObjectProcess
from schemaUtils import SchemaUtils

class Calculator(object):
    """docstring for Calculator"""

    def __init__(self, competition):
        super(Calculator, self).__init__()
        warnings.simplefilter('error', RuntimeWarning)
        self.comp = competition
        self.TBAC = TBACommunicator.TBACommunicator()
        self.TBAC.eventCode = self.comp.code
        self.ourTeamNum = 1678
        self.monteCarloIterations = 100
        self.su = SchemaUtils(self.comp, self)
        self.cachedTeamDatas = {}
        self.averageTeam = DataModel.Team()
        self.averageTeam.number = -1
        self.averageTeam.name = 'Average Team'
        self.surrogateTIMDs = []
        self.teleGearIncrements = [0, 2, 6, 12]
        self.autoGearIncrements = [1, 3, 7, 13]
        self.lifts = ['lift1', 'lift2', 'lift3']
        self.hops = ['hop1', 'hop2', 'hop3', 'hop4', 'hop5']
        self.cachedTeamDatas = {}
        self.cachedComp = cache.CachedCompetitionData()
        self.cachedTeamDatas[self.averageTeam.number] = cache.CachedTeamData(**{'teamNumber': self.averageTeam.number})
        for t in self.comp.teams:
            self.cachedTeamDatas[t.number] = cache.CachedTeamData(**{'teamNumber': t.number})

    def getMissingDataString(self):
        print "CURRENT MATCH NUM = " + str(self.comp.currentMatchNum)
        playedTIMDs = [timd for timd in self.comp.TIMDs if timd.matchNumber < self.comp.currentMatchNum]
        incompletePlayedSuperTIMDs = [timd for timd in playedTIMDs if timd.rankAgility == None]
        incompletePlayedScoutTIMDs = filter(lambda timd: timd.didLiftoff == None, playedTIMDs)
        incompletePlayedSuperTIMDStrings = ['Scout: ' + str(timd.teamNumber) + 'Q' + str(timd.matchNumber) for timd in incompletePlayedSuperTIMDs if timd.teamNumber != None]
        incompletePlayedScoutTIMDStrings = ['Super: ' + str(timd.teamNumber) + 'Q' + str(timd.matchNumber) for timd in incompletePlayedScoutTIMDs if timd.teamNumber != None]
        incompletePlayedSuperTIMDStrings.extend(incompletePlayedScoutTIMDStrings)
        return incompletePlayedSuperTIMDStrings

    #Calculated Team Data

    #Hardcore Math

    def getAverageForDataFunctionForTeam(self, team, dataFunction):
        validTIMDs = filter(lambda timd: dataFunction(timd) != None, self.su.getCompletedTIMDsForTeam(team))
        return np.mean(map(dataFunction, validTIMDs)) if validTIMDs else None #return None if validTIMDs has no elements

    def getSumForDataFunctionForTeam(self, team, dataFunction):
        return sum([dataFunction(tm) for tm in self.su.getCompletedTIMDsForTeam(team) if dataFunction(tm) != None])

    def getStandardDeviationForDataFunctionForTeam(self, team, dataFunction):
        validTIMDs = filter(lambda timd: dataFunction(timd) != None, self.su.getCompletedTIMDsForTeam(team))
        return np.std(map(dataFunction, validTIMDs)) if validTIMDs else None

    def getAverageOfDataFunctionAcrossCompetition(self, dataFunction):
        validData = filter(lambda x: x != None, map(dataFunction, self.su.teamsWithCalculatedData()))
        return np.mean(validData) if validData else 0

    def getStandardDeviationOfDataFunctionAcrossCompetition(self, dataFunction):
        return utils.rms(map(dataFunction, self.su.teamsWithCalculatedData()))

    def standardDeviationForRetrievalFunctionForAlliance(self, retrievalFunction, alliance):
        return utils.sumStdDevs(map(retrievalFunction, alliance))

    def monteCarloForMeanForStDevForValueFunction(self, mean, stDev, valueFunction):
        if stDev == 0.0:
            return 0.0
        return np.std([valueFunction(np.random.normal(mean, stDev)) for i in range(self.monteCarloIterations)])

    def probabilityDensity(self, x, mu, sigma):
        if sigma == 0.0:
            return int(x <= mu)
        if None not in [x,mu,sigma]:
            return 1.0 - stats.norm.cdf(x, mu, sigma)

    def welchsTest(self, mean1, mean2, std1, std2, sampleSize1, sampleSize2):
        if std1 == 0.0 or std2 == 0.0 or sampleSize1 <= 0 or sampleSize2 <= 0:
            return float(mean1 > mean2)
        numerator = mean1 - mean2
        denominator = ((std1 ** 2) / sampleSize1 + (std2 ** 2) / sampleSize2) ** 0.5
        return numerator / denominator

    def getAverageForDataFunctionForTIMDValues(self, timds, dataFunction):
        values = [dataFunction(timd) for timd in timds]
        return np.mean(values) if values else None

    def getDF(self, s1, s2, n1, n2):
        if np.nan in [s1, s2, n1, n2] or 0.0 in [n1,n2]:
            return
        try:
            numerator = ((s1**4/n1) + (s2**4/n2)) ** 2
            denominator = (s1**8/((n1**2)*(n1-1))) + (s2**8/((n2**2)*(n2-1)))
        except:
            numerator = 0.0
            denominator = 0.0
        return numerator / denominator if denominator != 0 else 0.0

    #SHOTS DATA

    def fieldsForShots(self, timd):
        return sum([sum(map(lambda v: (v.get('numShots') or 0), timd.highShotTimesForBoilerTele)) / 3.0, sum(map(lambda v: (v.get('numShots') or 0), timd.highShotTimesForBoilerAuto)), sum(map(lambda v: (v.get('numShots') or 0), timd.lowShotTimesForBoilerTele)) / 9.0, sum(map(lambda v: (v.get('numShots') or 0), timd.lowShotTimesForBoilerAuto)) / 3.0])

    def weightFuelShotsForDataPoint(self, timd, match, boilerPoint):
        timds = self.su.getCompletedTIMDsForMatchForAllianceIsRed(match, timd.teamNumber in match.redAllianceTeamNumbers)
        fuelPts = self.getShotPointsForMatchForAlliance(timds, timd.teamNumber in match.redAllianceTeamNumbers, match)
        scoutedFuelPoints = sum(map(self.fieldsForShots, timds))
        weightage = float(fuelPts) / scoutedFuelPoints if None not in [scoutedFuelPoints, fuelPts] and scoutedFuelPoints != 0 else None
        return sum(map(lambda v: (v.get('numShots') or 0), boilerPoint)) * weightage if weightage != None else 0

    def getShotPointsForMatchForAlliance(self, timds, allianceIsRed, match):
        gearPts = self.getGearPtsForAllianceTIMDs(timds)
        baselinePts = 5 * sum(map(lambda t: t.didReachBaselineAuto, timds))
        liftoffPts = 50 * sum(map(lambda t: t.didLiftoff, timds))
        fields = self.su.getFieldsForAllianceForMatch(allianceIsRed, match)
        return fields[0] - fields[3] - gearPts - baselinePts - liftoffPts if None not in [fields[0], fields[3]] else None

    def getTotalAverageShotPointsForTeam(self, team):
        return sum([(team.calculatedData.avgHighShotsTele or 0) / 3.0, (team.calculatedData.avgLowShotsTele or 0) / 9.0, team.calculatedData.avgHighShotsAuto, (team.calculatedData.avgLowShotsAuto or 0) / 3.0])

    def getStandardDevShotPointsForTeam(self, team):
        return utils.sumStdDevs([(team.calculatedData.sdHighShotsTele or 0) / 3.0, (team.calculatedData.sdLowShotsTele or 0) / 9.0, (team.calculatedData.sdHighShotsAuto or 0), (team.calculatedData.sdLowShotsAuto or 0) / 3.0])

    def getAllBoilerFieldsAtKey(self, timd):
        shots = timd.highShotTimesForBoilerTele + timd.highShotTimesForBoilerAuto + timd.lowShotTimesForBoilerAuto + timd.lowShotTimesForBoilerTele
        return filter(lambda v: v.get('position') == 'Key', shots)

    def getAvgKeyShotTimeForTIMD(self, timd):
        return np.mean(map(lambda t: (t.get('time') or 0), self.getAllBoilerFieldsAtKey(timd))) / 1000.0 if len(self.getAllBoilerFieldsAtKey(timd)) > 0 else None

    def getTotalAverageShotPointsForAlliance(self, alliance):
        return sum(map(self.getTotalAverageShotPointsForTeam, alliance))

    def getStandardDevShotPointsForAlliance(self, alliance):
        return self.standardDeviationForRetrievalFunctionForAlliance(self.getStandardDevShotPointsForTeam, alliance)

    def getAutoShootingPositions(self, team):
        timds = self.su.getCompletedTIMDsForTeam(team)
        return list(set([d.get('position') for timd in timds for d in timd.highShotTimesForBoilerAuto + timd.lowShotTimesForBoilerAuto]))

    # GEARS DATA

    def getTotalValueForValueDict(self, valueDict):
        return sum(filter(lambda v: v != None, valueDict.values()))

    def getAvgFuncForKeys(self, team, dic, retrievalFunction, keys):
        timds = self.su.getCompletedTIMDsForTeam(team)
        getAvgForKey = lambda t: np.mean(map(lambda tm: (retrievalFunction(tm).get(t) or 0), timds))
        [utils.setDictionaryValue(dic, l, getAvgForKey(l)) for l in keys]

    def getGearPtsForAllianceTIMDs(self, timds):
        return self.getRotorsTurningForDatasForGearFunc(timds, lambda t: (t.calculatedData.numGearsPlacedTele or 0), lambda t: (t.calculatedData.numGearsPlacedAuto or 0))

    def liftUsedTIMD(self, lift, timd):
        return lift in timd.gearsPlacedByLiftAuto.keys() if timd.gearsPlacedByLiftAuto else False

    def getMostFrequentLift(self, team):
        timds = self.su.getCompletedTIMDsForTeam(team)
        a = [len(filter(lambda t: self.liftUsedTIMD(lift, t), timds)) for lift in self.lifts]
        return self.lifts[a.index(max(a))]

    def getRotorsTurningForDatasForGearFunc(self, datas, gearFuncTele, gearFuncAuto):
        totalAutoGears = sum(map(gearFuncAuto, datas))
        totalTeleGears = sum(map(gearFuncTele, datas))
        rotorsAuto = self.getRotorForGearsForIncrement(totalAutoGears, self.autoGearIncrements)
        rotorsTele = self.getRotorForGearsForIncrement(totalAutoGears + totalTeleGears, self.teleGearIncrements[rotorsAuto:])
        return 60 * rotorsAuto + 40 * rotorsTele

    def getGearScoringPositionsAuto(self, team):
        timds = self.su.getCompletedTIMDsForTeam(team)
        return list(set([k for tm in timds for k in tm.gearsPlacedByLiftAuto.keys() if not tm.gearsPlacedByLiftAuto.get(k)]))

    def gearPlacementAbilityExcludeLift(self, team, eLift):
        return sum([(team.calculatedData.avgGearsPlacedByLiftAuto.get(lift) or 0) for lift in self.lifts if lift != eLift])

    def getAllGearProbabilitiesForTeam(self, team, gearFunc):
        return dict(zip(range(13), map(lambda g: self.probabilityForGearsPlacedForNumberForTeam(team, g, gearFunc), range(13))))

    def getAllGearProbabilitiesForTeams(self, gearFunc):
        dic = {team.number : self.getAllGearProbabilitiesForTeam(team, gearFunc) for team in self.cachedComp.teamsWithMatchesCompleted}
        func = lambda k: map(lambda v: (v.get(k) or 0.0), dic.values())
        dic[self.averageTeam.number] = {k : np.mean(func(k)) if len(func(k)) > 0 else 0 for k in range(13)}
        return dic

    def totalGearsPlacedForTIMD(self, timd):
        return timd.calculatedData.numGearsPlacedAuto + timd.calculatedData.numGearsPlacedTele

    # OVERALL DATA

    def liftoffAbilityForTIMD(self, timd):
        return 50 * timd.didLiftoff

    def rValuesForAverageFunctionForDict(self, averageFunction, d):
        values = map(averageFunction, self.cachedComp.teamsWithMatchesCompleted)
        if len(values) == 0:
            return
        initialValue = values[0]
        impossible = not len(filter(lambda v: v != initialValue, values[1:]))
        if impossible:
            zscores = [0.0 for v in values]
        else:
            zscores = stats.zscore(values)
        for i in range(len(self.cachedComp.teamsWithMatchesCompleted)):
            d[self.cachedComp.teamsWithMatchesCompleted[i].number] = zscores[i]

    def drivingAbility(self, team):
        gCWeight = 0.0
        bCWeight = 0.0
        spWeight = 0.4
        agWeight = 0.4
        dfWeight = 0.0
        return team.calculatedData.avgSpeed * spWeight + team.calculatedData.avgGearControl * gCWeight + team.calculatedData.avgBallControl * bCWeight + team.calculatedData.avgAgility * agWeight + team.calculatedData.avgDefense * dfWeight

    def predictedScoreForAllianceWithNumbers(self, allianceNumbers):
        return self.predictedScoreForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def stdDevPredictedScoreForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        fuelPts = self.getStandardDevShotPointsForAlliance(alliance)
        liftoffPts = utils.sumStdDevs(map(lambda t: t.calculatedData.sdLiftoffAbility, alliance))
        baselinePts = utils.sumStdDevs(map(lambda t: 5 * (t.calculatedData.sdBaselineReachedPercentage or 0), alliance))
        gearPts = self.getStdDevGearPointsForAlliance(alliance)
        return utils.sumStdDevs([fuelPts, liftoffPts, baselinePts, gearPts])

    def stdDevPredictedScoreForAllianceNumbers(self, allianceNumbers):
        return self.stdDevPredictedScoreForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def predictedScoreForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        baselinePts = sum(map(lambda t: (t.calculatedData.baselineReachedPercentage or 0) * 5, alliance))
        fuelPts = self.getTotalAverageShotPointsForAlliance(alliance)
        liftoffPoints = sum(map(lambda t: (t.calculatedData.liftoffAbility or 0), alliance))
        gearPts = self.getRotorsTurningForDatasForGearFunc(alliance, lambda t: t.calculatedData.avgGearsPlacedTele, lambda t: t.calculatedData.avgGearsPlacedAuto)
        return baselinePts + fuelPts + liftoffPoints + gearPts

    def predictedPlayoffScoreForAlliance(self, alliance):
        return 20 * self.get40KilopascalChanceForAlliance(alliance) + self.predictedScoreForAlliance(alliance) + 100 * self.getAllRotorsTurningChanceForAlliance(alliance)

    def firstPickAbility(self, team):
        ourTeam = self.su.getTeamForNumber(self.ourTeamNum)
        if self.predictedScoreForAlliance([ourTeam, team, self.averageTeam]) == None or math.isnan(self.predictedScoreForAlliance([ourTeam, team, self.averageTeam])):
            return
        return self.predictedPlayoffScoreForAlliance([ourTeam, team])

    def firstPickAllRotorsChance(self, team):
        ourTeam = self.su.getTeamForNumber(self.ourTeamNum)
        return self.getAllRotorsTurningChanceForTwoRobotAlliance([ourTeam, team])

    def overallSecondPickAbility(self, team):
        defense = (team.calculatedData.RScoreDefense or 0) * 1.0
        gearControl = (team.calculatedData.RScoreGearControl or 0) * 1.0
        functionalPercentage = (1 - team.calculatedData.disfunctionalPercentage)
        freqLiftOurTeam = self.getMostFrequentLift(self.su.getTeamForNumber(self.ourTeamNum))
        gA = self.gearPlacementAbilityExcludeLift(team, freqLiftOurTeam) #convert to some number of points
        return functionalPercentage * (gA + defense + gearControl + team.calculatedData.liftoffAbility)

    def predictedScoreForMatchForAlliance(self, match, allianceIsRed):
        return match.calculatedData.predictedRedScore if allianceIsRed else match.calculatedData.predictedBlueScore

    def sdPredictedScoreForMatchForAlliance(self, match, allianceIsRed):
        return match.calculatedData.sdPredictedRedScore if allianceIsRed else match.calculatedData.sdPredictedBlueScore

    def getAvgNumCompletedTIMDsForTeamsOnAlliance(self, alliance):
        return sum(map(lambda t: len(self.su.getCompletedTIMDsForTeam(t)), alliance)) # TODO:WATCHOUT!!!

    def getAvgNumCompletedTIMDsForAlliance(self, alliance):
        return self.getAvgNumCompletedTIMDsForTeamsOnAlliance(alliance)

    def sampleSizeForMatchForAlliance(self, alliance):
        return self.getAvgNumCompletedTIMDsForAlliance(alliance)

    def getStdDevGearPointsForAlliance(self, alliance):
        sdGearsAuto = self.standardDeviationForRetrievalFunctionForAlliance(lambda t: t.calculatedData.sdGearsPlacedAuto, alliance)
        sdGearsTele = self.standardDeviationForRetrievalFunctionForAlliance(lambda t: t.calculatedData.sdGearsPlacedTele, alliance)
        autoR = 60 * self.getRotorForGearsForIncrement(sdGearsAuto, self.autoGearIncrements)
        teleR = 40 * self.getRotorForGearsForIncrement(sdGearsTele, self.teleGearIncrements)
        return autoR + teleR

    def getRotorForGearsForIncrement(self, gears, inc):
        incrementsReached = filter(lambda g: gears >= g, inc)
        return inc.index(max(incrementsReached)) + 1 if len(incrementsReached) > 0 else 0

    #PROBABILITIES

    def winChanceForMatchForAllianceIsRed(self, match, allianceIsRed):
        alliance = self.su.getAllianceForMatch(match, allianceIsRed)
        predictedScore  = self.predictedScoreForMatchForAlliance(match, allianceIsRed)
        opposingPredictedScore = self.predictedScoreForMatchForAlliance(match, not allianceIsRed)
        sdPredictedScore = self.sdPredictedScoreForMatchForAlliance(match, allianceIsRed)
        sdOpposingPredictedScore = self.sdPredictedScoreForMatchForAlliance(match, not allianceIsRed)
        sampleSize = self.sampleSizeForMatchForAlliance(alliance)
        opposingSampleSize = self.sampleSizeForMatchForAlliance(alliance)
        tscoreRPs = self.welchsTest(predictedScore,
                                       opposingPredictedScore,
                                       sdPredictedScore,
                                       sdOpposingPredictedScore,
                                       sampleSize,
                                       opposingSampleSize)
        df = self.getDF(sdPredictedScore, opposingPredictedScore, sampleSize, opposingSampleSize)
        winChance = stats.t.cdf(tscoreRPs, df)
        return winChance if not math.isnan(winChance) else 0.0

    def getWinChanceForMatchForAllianceIsRed(self, match, allianceIsRed):
        winChance = match.calculatedData.redWinChance if allianceIsRed else match.calculatedData.blueWinChance
        return winChance if not math.isnan((winChance or 0.0)) or not winChance else None

    def get40KilopascalChanceForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        return self.probabilityDensity(40, self.getTotalAverageShotPointsForAlliance(alliance), self.getStandardDevShotPointsForAlliance(alliance))

    def get40KilopascalChanceForAllianceWithNumbers(self, allianceNumbers):
        self.get40KilopascalChanceForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def totalZProbTeam(self, team, number):
        return self.cachedComp.zGearProbabilities[team.number].get(number) or 0.0

    def getAllRotorsTurningChanceForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        three = (len(alliance) == 3)
        return sum(map(lambda w: sum(map(lambda z: (self.totalZProbTeam(alliance[2], z) if three else 1) * sum(map(lambda y: self.totalZProbTeam(alliance[0], w-y-z) * self.totalZProbTeam(alliance[1], y), range(13))), range(13 if three else 1))), range(12,len(alliance) * 12 + 1)))

    def getAllRotorsTurningChanceForTwoRobotAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        return sum(map(lambda w: sum(map(lambda y: self.totalZProbTeam(alliance[0], w-y) * self.totalZProbTeam(alliance[1], y), range(13))), range(12, 25)))

    def probabilityForGearsPlacedForNumberForTeam(self, team, number, gearFunc):
        gearTimds = map(gearFunc, self.su.getCompletedTIMDsForTeam(team))
        return (gearTimds.count(number)/float(len(gearTimds))) or 0

    def getAllRotorsTurningChanceForAllianceWithNumbers(self, allianceNumbers):
        return self.getAllRotorsTurningChanceForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    # Seeding
    def autoPointsForAlliance(self, team, match):
        timds = self.su.getTIMDsForMatchForAllianceIsRed(match, team.number in match.redAllianceTeamNumbers)
        fuelPts = sum(map(lambda t: t.calculatedData.numHighShotsAuto + t.calculatedData.numLowShotsAuto / 3.0, timds))
        baselinePts = sum(map(lambda t: t.didReachBaselineAuto * 5, timds))
        incsReached = filter(lambda p: sum(map(lambda t: t.calculatedData.numGearsPlacedAuto, timds)) >= p, self.autoGearIncrements)
        gearPts = 60 * (self.autoGearIncrements.index(max(incsReached)) + 1) if len(incsReached) > 0 else 0
        return fuelPts + baselinePts + gearPts

    def predictedAutoPointsForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        fuelPts = sum(map(lambda t: t.calculatedData.avgHighShotsAuto + t.calculatedData.avgLowShotsAuto / 3.0, alliance))
        baselinePts = sum(map(lambda t: t.calculatedData.baselineReachedPercentage * 5, alliance))
        incsReached = filter(lambda p: sum(map(lambda t: t.calculatedData.avgGearsPlacedAuto, alliance)) >= p, self.autoGearIncrements)
        gearPts = 60 * (self.autoGearIncrements.index(max(incsReached)) + 1) if len(incsReached) > 0 else 0
        return fuelPts + baselinePts + gearPts

    def cumulativeAutoPointsForTeam(self, team):
        return sum(map(lambda m: self.autoPointsForAlliance(team, m), self.su.getCompletedMatchesForTeam(team)))

    def cumulativePredictedAutoPointsForTeam(self, team):
        matches = filter(lambda m: not self.su.matchIsCompleted(m), self.su.getMatchesForTeam(team))
        return sum([self.predictedAutoPointsForAlliance(self.su.getAllianceForTeamInMatch(team, match)) for match in matches]) + self.cumulativeAutoPointsForTeam(team)

    def cumulativeMatchPointsForTeam(self, team):
        allMatches = self.su.getCompletedMatchesForTeam(team)
        scoreFunc = lambda m: self.su.getFieldsForAllianceForMatch(team in match.redAllianceTeamNumbers, match)[0]
        return sum([scoreFunc(match) for match in allMatches])

    def cumulativePredictedMatchPointsForTeam(self, team):
        matches = filter(lambda m: not self.su.matchIsCompleted(m), self.su.getMatchesForTeam(team))
        return sum([self.predictedScoreForAlliance(self.su.getAllianceForTeamInMatch(team, match)) for match in matches]) + self.cumulativeMatchPointsForTeam(team)

    def getSeedingFunctions(self):
        return [lambda t: t.calculatedData.actualNumRPs, lambda t: self.cumulativeMatchPointsForTeam(t), lambda t: self.cumulativeAutoPointsForTeam(t)]

    def getPredictedSeedingFunctions(self):
        return [lambda t: self.predictedNumberOfRPs(t), lambda t: self.cumulativePredictedMatchPointsForTeam(t), lambda t: self.cumulativePredictedAutoPointsForTeam(t)]

    def predictedNumberOfRPs(self, team):
        predictedRPsFunction = lambda m: self.predictedRPsForAllianceForMatch(self.su.getTeamAllianceIsRedInMatch(team, m), m)
        predictedRPs = np.mean([predictedRPsFunction(m) for m in self.su.getMatchesForTeam(team) if not self.su.matchIsCompleted(m) and predictedRPsFunction(m) != None])
        return np.mean([predictedRPs, self.actualNumberOfRPs(team)])

    def actualNumberOfRPs(self, team):
        return self.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numRPs)

    def scoreRPsGainedFromMatchWithScores(self, score, opposingScore):
        if score > opposingScore:
            return 2
        elif score == opposingScore:
            return 1
        else:
            return 0

    def RPsGainedFromMatchForAlliance(self, allianceIsRed, match):
        ourFields = self.su.getFieldsForAllianceForMatch(allianceIsRed, match)
        opposingFields = self.su.getFieldsForAllianceForMatch(not allianceIsRed, match)
        numRPs = self.scoreRPsGainedFromMatchWithScores(ourFields[0], opposingFields[0])
        return numRPs + utils.convertFirebaseBoolean(ourFields[1]) + utils.convertFirebaseBoolean(ourFields[2])

    def predictedRPsForAllianceForMatch(self, allianceIsRed, match):
        alliance = map(self.su.replaceWithAverageIfNecessary, self.su.getAllianceForMatch(match, allianceIsRed))
        scoreRPs = 2 * (self.getWinChanceForMatchForAllianceIsRed(match, allianceIsRed) or 0)
        boilerRPs = self.get40KilopascalChanceForAlliance(alliance)
        rotorRPs = self.getAllRotorsTurningChanceForAlliance(alliance)
        RPs = scoreRPs + boilerRPs + rotorRPs
        return RPs if not math.isnan(RPs) else None

    def teamsSortedByRetrievalFunctions(self, retrievalFunctions):
        return sorted(self.cachedComp.teamsWithMatchesCompleted, key=lambda t: (retrievalFunctions[0](t), retrievalFunctions[1](t), retrievalFunctions[2](t)), reverse=True)

    def getTeamSeed(self, team):
        return int(filter(lambda x: int(x[1]) == team.number, self.cachedComp.actualSeedings)[0][0])

    def getTeamRPsFromTBA(self, team):
        return int(float(filter(lambda x: int(x[1]) == team.number, self.cachedComp.actualSeedings)[0][2]))

    #CACHING

    def cacheFirstTeamData(self):
        for team in self.comp.teams:
            self.doCachingForTeam(team)
        self.doCachingForTeam(self.averageTeam)
        self.cachedComp.teamsWithMatchesCompleted = self.su.findTeamsWithMatchesCompleted()

    def rScoreParams(self):
        return [(lambda t: t.calculatedData.avgSpeed, self.cachedComp.speedZScores),
                     (lambda t: t.calculatedData.avgAgility, self.cachedComp.agilityZScores),
                     (lambda t: t.calculatedData.avgBallControl, self.cachedComp.ballControlZScores),
                     (lambda t: t.calculatedData.avgGearControl, self.cachedComp.gearControlZScores),
                     (lambda t: t.calculatedData.avgDefense, self.cachedComp.defenseZScores),
                     (lambda t: t.calculatedData.avgDrivingAbility, self.cachedComp.drivingAbilityZScores)]

    def cacheSecondTeamData(self):
        map(lambda (func, dictionary): self.rValuesForAverageFunctionForDict(func, dictionary), self.rScoreParams())
        map(self.doSecondCachingForTeam, self.comp.teams)
        try:
            self.cachedComp.actualSeedings = self.TBAC.makeEventRankingsRequest()
        except:
            self.cachedComp.actualSeedings = self.teamsSortedByRetrievalFunctions(self.getSeedingFunctions())
        self.cachedComp.zGearProbabilities = self.getAllGearProbabilitiesForTeams(lambda tm: self.totalGearsPlacedForTIMD(tm))
        self.cachedComp.predictedSeedings = self.teamsSortedByRetrievalFunctions(self.getPredictedSeedingFunctions())

    def doCachingForTeam(self, team):
        try:
            cachedData = self.cachedTeamDatas[team.number]
        except:
            self.cachedTeamDatas[team.number] = cache.CachedTeamData(**{'teamNumber': team.number})
            cachedData = self.cachedTeamDatas[team.number]
        cachedData.completedTIMDs = self.su.retrieveCompletedTIMDsForTeam(team)

    def doSecondCachingForTeam(self, team):
        cachedData = self.cachedTeamDatas[team.number]

    #CALCULATIONS

    def getFirstCalculationsForAverageTeam(self):
        averageTeamDict(self)

    def doFirstCalculationsForTeam(self, team):
        if len(self.su.getCompletedTIMDsForTeam(team)) > 0:
            if not self.su.teamCalculatedDataHasValues(team.calculatedData):
                team.calculatedData = DataModel.CalculatedTeamData()
            t = team.calculatedData
            firstCalculationDict(team, self)
            print "Completed first calcs for " + str(team.number)

    def doSecondCalculationsForTeam(self, team):
        if not 0 in [len(self.su.getCompletedTIMDsForTeam(team)), len(self.su.getCompletedMatchesForTeam(team))]:
            secondCalculationDict(team, self)
            print "Completed second calculations for team " + str(team.number)

    def doFirstCalculationsForMatch(self, match): #This entire thing being looped is what takes a while
        matchDict(match, self)
        print "Completed calculations for match " + str(match.number)

    def doFirstTeamCalculations(self):
        map(self.doFirstCalculationsForTeam, self.comp.teams)
        self.getFirstCalculationsForAverageTeam()

    def doSecondTeamCalculations(self):
        map(self.doSecondCalculationsForTeam, self.comp.teams)
        self.doSecondCalculationsForTeam(self.averageTeam)

    def doThirdTeamCalculations(self):
        map(self.doThirdCalculationsForTeam, self.comp.teams)
        self.doThirdCalculationsForTeam(self.averageTeam)

    def doMatchesCalculations(self):
        map(self.doFirstCalculationsForMatch, self.comp.matches)

    def writeCalculationDiagnostic(self, time):
        with open('./diagnostics.txt', 'a') as file:
            file.write('Time: ' + str(time) + '    TIMDs: ' + str(len(self.su.getCompletedTIMDsInCompetition())) + '\n')
            file.close()

    def doCalculations(self, FBC):
        isData = len(self.su.getCompletedTIMDsInCompetition()) > 0
        if isData:
            print "THERE IS DATA"
            startTime = time.time()
            threads = []
            manager = multiprocessing.Manager()
            calculatedTIMDs = manager.list()
            numTIMDsCalculating = 0
            for timd in self.comp.TIMDs:
                thread = FirstTIMDProcess(timd, calculatedTIMDs, self)
                threads.append(thread)
                thread.start()
            map(lambda t: t.join(), threads)
            self.comp.TIMDs = [timd for timd in calculatedTIMDs]
            self.cacheFirstTeamData()
            self.doFirstTeamCalculations()
            self.cacheSecondTeamData()
            self.doMatchesCalculations()
            self.doSecondTeamCalculations()
            map(lambda o: FirebaseWriteObjectProcess(o, FBC).start(), self.cachedComp.teamsWithMatchesCompleted + self.su.getCompletedTIMDsInCompetition() + self.comp.matches)
            FBC.addCompInfoToFirebase()
            endTime = time.time()
            self.writeCalculationDiagnostic(endTime - startTime)
        else:
            print "No Data"
