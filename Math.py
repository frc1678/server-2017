import math
from operator import attrgetter
import re
import pdb
import time

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
import copy
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
        self.su = SchemaUtils(self.comp)
        self.cachedTeamDatas = {}
        self.averageTeam = DataModel.Team()
        self.averageTeam.number = -1
        self.averageTeam.name = 'Average Team'
        self.surrogateTIMDs = []
        self.cachedComp = cache.CachedCompetitionData()
        self.cachedTeamDatas[self.averageTeam.number] = cache.CachedTeamData(**{'teamNumber': self.averageTeam.number})
        [utils.setDictionaryValue(self.cachedTeamDatas, team.number,
                                  cache.CachedTeamData(**{'teamNumber': team.number})) for team in self.comp.teams]

    def getMissingDataString(self):
        print "CURRENT MATCH NUM = " + str(self.comp.currentMatchNum)
        playedTIMDs = [timd for timd in self.comp.TIMDs if timd.matchNumber < self.comp.currentMatchNum]
        incompletePlayedSuperTIMDs = [timd for timd in playedTIMDs if timd.rankTorque == None]
        incompletePlayedScoutTIMDs = filter(lambda timd: timd.numHighShotsMadeTele == None, playedTIMDs)
        incompletePlayedSuperTIMDStrings = ['Scout: ' + str(timd.teamNumber) + 'Q' + str(timd.matchNumber) for timd in incompletePlayedSuperTIMDs]
        incompletePlayedScoutTIMDStrings = ['Super: ' + str(timd.teamNumber) + 'Q' + str(timd.matchNumber) for timd in incompletePlayedScoutTIMDs]
        incompletePlayedSuperTIMDStrings.extend(incompletePlayedScoutTIMDStrings)
        return incompletePlayedSuperTIMDStrings


    #Calculated Team Data

    #Hardcore Math

    def getAverageForDataFunctionForTeam(self, team, dataFunction):
        validTIMDs = filter(lambda timd: dataFunction(timd) != None, self.su.getCompletedTIMDsForTeam(team))
        return np.mean(map(dataFunction, validTIMDs)) if len(validTIMDs) > 0 else None

    def getSumForDataFunctionForTeam(self, team, dataFunction):
        return sum([dataFunction(tm) for tm in self.su.getCompletedTIMDsForTeam(team) if dataFunction(tm) != None])

    def getStandardDeviationForDataFunctionForTeam(self, team, dataFunction):
        validTIMDs = filter(lambda timd: dataFunction(timd) != None, self.su.getCompletedTIMDsForTeam(team))
        return np.std(map(dataFunction, validTIMDs)) if len(validTIMDs) > 0 else None

    def getAverageOfDataFunctionAcrossCompetition(self, dataFunction):
        validData = filter(lambda x: x != None, map(dataFunction, self.su.teamsWithCalculatedData()))
        return np.mean(validData) if len(validData) > 0 else None

    def getStandardDeviationOfDataFunctionAcrossCompetition(self, dataFunction):
        return utils.rms(map(dataFunction, self.su.teamsWithCalculatedData()))

    def standardDeviationForRetrievalFunctionForAlliance(self, retrievalFunction, alliance):
        return utils.sumStdDevs(map(retrievalFunction, alliance))

    def monteCarloForMeanForStDevForValueFunction(self, mean, stDev, valueFunction):
        if stDev == 0.0: return 0.0
        return np.std([valueFunction(np.random.normal(mean, stDev)) for i in range(self.monteCarloIterations)])

    def probabilityDensity(self, x, mu, sigma):
        if sigma == 0.0:
            return int(x >= mu)
        if None not in [x,mu,sigma]: return 1.0 - stats.norm.cdf(x, mu, sigma)

    def welchsTest(self, mean1, mean2, std1, std2, sampleSize1, sampleSize2):
        if std1 == 0.0 or std2 == 0.0 or sampleSize1 <= 0 or sampleSize2 <= 0: return float(mean1 > mean2)
        numerator = mean1 - mean2
        denominator = ((std1 ** 2) / sampleSize1 + (std2 ** 2) / sampleSize2) ** 0.5
        return numerator / denominator

    def getAverageForDataFunctionForTIMDValues(self, timds, dataFunction):
        values = [dataFunction(timd) for timd in timds]
        return np.mean(values) if len(values) > 0 else None

    # OVERALL DATA

    def rValuesForAverageFunctionForDict(self, averageFunction, d):
        impossible = True
        values = map(averageFunction, self.cachedComp.teamsWithMatchesCompleted)
        if len(values) == 0:
            return None
        initialValue = values[0]
        for value in values[1:]:
            if value != initialValue: impossible = False
        if impossible:
            zscores = [0.0 for v in values]
        else:
            zscores = stats.zscore(values)
        for i in range(len(self.cachedComp.teamsWithMatchesCompleted)):
            d[self.cachedComp.teamsWithMatchesCompleted[i].number] = zscores[i]

    def drivingAbility(self, team):
        return

    def predictedScoreForAllianceWithNumbers(self, allianceNumbers):
        return self.predictedScoreForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def stdDevPredictedScoreForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)

        return utils.sumStdDevs([])

    def stdDevPredictedScoreForAllianceNumbers(self, allianceNumbers):
        return self.stdDevPredictedScoreForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def predictedScoreForAlliance(self, alliance):
        return None

    def predictedPlayoffPointScoreForAlliance(self, alliance):
        return 20 * self.get40kPAChanceForAlliance(alliance) + self.predictedScoreForAlliance(alliance) + 100 * self.getAllRotorsTurningChanceForAlliance(alliance)

    def firstPickAbility(self, team):
        ourTeam = self.su.getTeamForNumber(self.ourTeamNum)
        if self.predictedScoreForAlliance([ourTeam, team]) == None or math.isnan(self.predictedScoreForAlliance([ourTeam, team])): return
        return self.predictedPlayoffPointScoreForAlliance([ourTeam, team])

    def overallSecondPickAbility(self, team):
        return

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

    def getTotalAverageShotPointsForTeam(self, team):
        return sum([team.calculatedData.avgHighShotsTele / 3.0, team.calculatedData.avgLowShotsTele / 9.0, team.calculatedData.avgHighShotsAuto, team.calculatedData.avgLowShotsAuto / 3.0])

    def getStandardDevShotPointsForTeam(self, team):
        return utils.sumStdDevs([team.calculatedData.sdHighShotsTele / 3.0, team.calculatedData.sdLowShotsTele / 9.0, team.calculatedData.sdHighShotsAuto, team.calculatedData.sdLowShotsAuto / 3.0])

    def getAverageAutoRotorsStartedForTeam(self, team):
        if team.calculatedData.avgGearsPlacedAuto >= 3:
            avgRotorsStartedAuto = 2
        elif team.calculatedData.avgGearsPlacedAuto >= 1:
            avgRotorsStartedAuto = 1
        else:
            avgRotorsStartedAuto = 0
        return avgRotorsStartedAuto

    def getTotalAverageRotorsStartedForTeam(self, team):
        avgTotalGearsPlaced = team.calculatedData.avgGearsPlacedAuto + team.calculatedData.avgGearsPlacedTele
        if avgTotalGearsPlaced >= 12:
            avgRotorsStarted = 4
        elif avgTotalGearsPlaced >= 6:
            avgRotorsStarted = 3
        elif avgTotalGearsPlaced >= 2:
            avgRotorsStarted = 2
        else:
            avgRotorsStarted = 1
        return avgRotorsStarted

    def getAverageTeleRotorsStartedForTeam(self, team):
        return getTotalAverageRotorsStartedForTeam(team) - getAverageAutoRotorsStartedForTeam(team)

    def getTotalAverageGearPointsForTeam(self, team):
        return getAverageAutoRotorsStartedForTeam(team) * 60 + getAverageTeleRotorsStartedForTeam(team) * 40

    def getStandardDevGearPointsForTeam(self, team):
        autoGearValue = getAverageAutoRotorsStartedForTeam(team) * 60 / team.calculatedData.avgGearsPlacedAuto
        autoGearSD = autoGearValue * sdGearsPlacedAuto
        teleGearValue = getAverageTeleRotorsStartedForTeam(team) * 40 / team.calculatedData.avgGearsPlacedTele
        teleGearSD = teleGearValue * sdGearsPlacedTele
        return utils.sumStdDevs([autoGearSD, teleGearSD])

    def getTotalAverageLiftoffPointsForTeam(self, team):
        return team.calculatedData.liftoffAbility * 40

    def getStandardDevLiftoffPointsForTeam(self, team):
        return team.calculatedData.sdLiftoffAbility * 40

    def getTotalAverageShotPointsForAlliance(self, alliance):
        return sum(self.getAverageShotPointsForTeam, alliance)

    def getStandardDevShotPointsForAlliance(self, alliance):
        return self.standardDeviationForRetrievalFunctionForAlliance(self.getStandardDevShotPointsForTeam, alliance)

    def getTotalAverageGearsPlacedForTeam(self, team):
        return team.calculatedData.avgGearsPlacedAuto + team.calculatedData.avgGearsPlacedTele

    def getTotalAverageGearsPlacedForAlliance(self, alliance):
        return sum(map(getTotalAverageGearsPlacedForTeam, alliance))

    def getStandardDevGearsPlacedForTeam(self, team):
        return utils.sumStdDevs([team.calculatedData.sdGearsPlacedAuto, team.calculatedData.sdGearsPlacedTele])

    def getStandardDevGearsPlacedForAlliance(self, alliance):
        return self.standardDeviationForRetrievalFunctionForAlliance(self.getStandardDevGearsPlacedForTeam, alliance)

    #PROBABILITIES

    def getWinChanceForMatchForAllianceIsRed(self, match, allianceIsRed):
        winChance = match.calculatedData.redWinChance if allianceIsRed else match.calculatedData.blueWinChance
        return winChance if not math.isnan(winChance) else None

    def get40kPAChanceForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        return self.probabilityDensity(40.01, self.getTotalAverageShotPointsForAlliance(alliance), self.getStandardDevShotPointsForTeam(alliance))

    def get40kPAChanceForAllianceWithNumbers(self, allianceNumbers):
        self.get40kPAChanceForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def getAllRotorsTurningChanceForAlliance(self, alliance):
        alliance = map(self.su.replaceWithAverageIfNecessary, alliance)
        return self.probabilityDensity(13.0, self.getTotalAverageGearsPlacedForAlliance(alliance), self.getStandardDevGearsPlacedForAlliance(alliance))

    def getAllRotorsTurningChanceForAllianceWithNumbers(self, allianceNumbers):
        return self.getAllRotorsTurningChanceForAlliance(self.su.teamsForTeamNumbersOnAlliance(allianceNumbers))

    def getDF(self, s1, s2, n1, n2):
        numerator = ((s1**4/n1) + (s2**4/n2)) ** 2
        denominator = (s1**8/((n1**2)*(n1-1))) + (s2**8/((n2**2)*(n2-1)))
        return numerator / denominator

    # Seeding

    def getScoreAcrossAllMatches(self, team):
        allMatches = SchemaUtils.getCompletedMatchesForTeam(team)
        totalScore = 0
        for match in allMatches:
            if team.number in match.redAllianceTeamNumbers:
                totalScore += match.redScore
            else:
                totalScore += match.blueScore
        return totalScore

    def getSeedingFunctions(self):
        return [lambda t: t.calculatedData.actualNumRPs, lambda t: self.getScoreAcrossAllMatches(t)]

    def getPredictedSeedingFunctions(self):
        return [lambda t: t.calculatedData.predictedNumRPs]

    def predictedNumberOfRPs(self, team):
        predictedRPsFunction = lambda m: self.predictedRPsForAllianceForMatch(self.su.getTeamAllianceIsRedInMatch(team, m), m)
        predictedRPs = sum([predictedRPsFunction(m) for m in self.su.getMatchesForTeam(team) if not self.su.matchIsCompleted(m) and predictedRPsFunction(m) != None])
        return predictedRPs + self.actualNumberOfRPs(team)

    def actualNumberOfRPs(self, team):
        return self.getSumForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numRPs)

    def scoreRPsGainedFromMatchWithScores(self, score, opposingScore):
        if score > opposingScore: return 2
        elif score == opposingScore: return 1
        else: return 0

    def RPsGainedFromMatchForAlliance(self, allianceIsRed, match):
        ourFields = self.su.getFieldsForAllianceForMatch(allianceIsRed, match)
        opposingFields = self.su.getFieldsForAllianceForMatch(not allianceIsRed, match)
        numRPs = self.scoreRPsGainedFromMatchWithScores(ourFields[0], opposingFields[0])
        return numRPs + int(utils.convertFirebaseBoolean(ourFields[1])) + int(utils.convertFirebaseBoolean(ourFields[2]))

    def RPsGainedFromMatchForTeam(self, team, match):
        return self.RPsGainedFromMatchForAlliance(self.su.getTeamAllianceIsRedInMatch(team, match), match)

    def predictedRPsForAllianceForMatch(self, allianceIsRed, match):
        alliance = map(self.su.replaceWithAverageIfNecessary, self.su.getAllianceForMatch(match, allianceIsRed))
        scoreRPs = 2 * (self.getWinChanceForMatchForAllianceIsRed(match, allianceIsRed) or 0)
        boilerRPs = 0
        rotorRPs = 0
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
                     (lambda t: t.calculatedData.avgGearControl, self.cachedComp.gearControlZScores)]

    def cacheSecondTeamData(self):
        map(lambda (func, dictionary): self.rValuesForAverageFunctionForDict(func, dictionary), self.rScoreParams())
        map(self.doSecondCachingForTeam, self.comp.teams)
        try:
            self.cachedComp.actualSeedings = self.TBAC.makeEventRankingsRequest()
        except:
            self.cachedComp.actualSeedings = []
        self.cachedComp.predictedSeedings = self.teamsSortedByRetrievalFunctions(self.getPredictedSeedingFunctions())
        self.doSecondCachingForTeam(self.averageTeam)

    def doCachingForTeam(self, team):
        cachedData = self.cachedTeamDatas[team.number]
        cachedData.completedTIMDs = self.su.retrieveCompletedTIMDsForTeam(team)

    def doSecondCachingForTeam(self, team):
        cachedData = self.cachedTeamDatas[team.number]
        map(lambda dKey: utils.setDictionaryValue(cachedData.alphas, dKey, self.alphaForTeamForDefense(team, dKey)), self.defenseList)
        map(lambda dKey: utils.setDictionaryValue(cachedData.betas, dKey, self.betaForTeamForDefense(team, dKey)), self.defenseList)

    #CALCULATIONS

    def getFirstCalculationsForAverageTeam(self):
        a = self.averageTeam.calculatedData

    def doFirstCalculationsForTeam(self, team):
        if not len(self.su.getCompletedTIMDsForTeam(team)) <= 0:
            if not self.su.teamCalculatedDataHasValues(team.calculatedData):
                team.calculatedData = DataModel.CalculatedTeamData()
            t = team.calculatedData
            print "Completed first calcs for " + str(team.number)
        firstCalcDict = firstCalculationDict(team)
        for k in firstCalcDict.keys():
            t.__dict__[k] = firstCalcDict[k]()

    def doSecondCalculationsForTeam(self, team):
        if not len(self.su.getCompletedTIMDsForTeam(team)) <= 0:
            pass

    def doThirdCalculationsForTeam(self, team):
        if not len(self.su.getCompletedMatchesForTeam(team)) <= 0:
            t = team.calculatedData
            t.predictedNumRPs = self.predictedNumberOfRPs(team)
            try:
                t.actualNumRPs = self.getTeamRPsFromTBA(team)
                t.actualSeed = self.getTeamSeed(team)
            except:
                t.actualNumRPs = self.actualNumberOfRPs(team)
                t.actualSeed = self.teamsSortedByRetrievalFunctions(self.getSeedingFunctions())
            t.predictedSeed = self.cachedComp.predictedSeedings.index(team) + 1
            t.firstPickAbility = self.firstPickAbility(team) # Checked
            t.overallSecondPickAbility = self.overallSecondPickAbility(team) # Checked
            print "Completed second calcs for team " + str(team.number)

    def doFirstCalculationsForMatch(self, match): #This entire thing being looped is what takes a while
        print "Performing calculations for match Q" + str(match.number)
        if self.su.matchIsCompleted(match):
            match.calculatedData.actualBlueRPs = self.RPsGainedFromMatchForAlliance(True, match)
            match.calculatedData.actualRedRPs = self.RPsGainedFromMatchForAlliance(False, match)
        match.calculatedData.predictedBlueScore = self.predictedScoreForAllianceWithNumbers(match.blueAllianceTeamNumbers)
        match.calculatedData.predictedRedScore = self.predictedScoreForAllianceWithNumbers(match.redAllianceTeamNumbers)
        match.calculatedData.sdPredictedBlueScore = self.stdDevPredictedScoreForAllianceNumbers(match.blueAllianceTeamNumbers)
        match.calculatedData.sdPredictedRedScore = self.stdDevPredictedScoreForAllianceNumbers(match.redAllianceTeamNumbers)
        match.calculatedData.fortykPAChanceRed = self.get40kPAChanceForAllianceWithNumbers(match.redAllianceTeamNumbers)
        match.calculatedData.fortykPAChanceBlue = self.get40kPAChanceForAllianceWithNumbers(match.blueAllianceTeamNumbers)
        match.calculatedData.allRotorsTurningChanceRed = self.getAllRotorsTurningChanceForAllianceWithNumbers(match.redAllianceTeamNumbers)
        match.calculatedData.allRotorsTurningChanceBlue = self.getAllRotorsTurningChanceForAllianceWithNumbers(match.blueAllianceTeamNumbers)
        match.calculatedData.blueWinChance = self.winChanceForMatchForAllianceIsRed(match, False)
        match.calculatedData.redWinChance = self.winChanceForMatchForAllianceIsRed(match, True)
        match.calculatedData.predictedBlueRPs = self.predictedRPsForAllianceForMatch(False, match)
        match.calculatedData.predictedRedRPs = self.predictedRPsForAllianceForMatch(True, match)
        print "Done! Match " + str(match.number)

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
            startTime = time.time()
            threads = []
            manager = multiprocessing.Manager()
            calculatedTIMDs = manager.list()
            numTIMDsCalculating = 0
            for timd in self.comp.TIMDs:
                thread = FirstTIMDProcess(timd, calculatedTIMDs, self)
                threads.append(thread)
                thread.start()
            self.cacheFirstTeamData()
            self.doFirstTeamCalculations()
            self.cacheSecondTeamData()
            self.doSecondTeamCalculations()
            self.doMatchesCalculations()
            self.doThirdTeamCalculations()
            map(lambda o: FirebaseWriteObjectProcess(o, FBC).start(), self.cachedComp.teamsWithMatchesCompleted + self.su.getCompletedTIMDsInCompetition() + self.comp.matches)
            FBC.addCompInfoToFirebase()
            endTime = time.time()
            self.writeCalculationDiagnostic(endTime - startTime)
        else:
            print "No Data"
