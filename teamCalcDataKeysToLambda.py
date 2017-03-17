import utils
import DataModel
import pdb
import traceback

def firstCalculationDict(team, calc):
    cd = team.calculatedData
    mapFuncForCalcAvgsForTeam(team, lambda f: calc.getAverageForDataFunctionForTeam(team, f), 
        avgHighShotsTele = lambda tm: tm.calculatedData.numHighShotsTele, 
        avgHighShotsAuto = lambda tm: tm.calculatedData.numHighShotsAuto,
        avgLowShotsAuto = lambda tm: tm.calculatedData.numLowShotsAuto, 
        avgLowShotsTele = lambda tm: tm.calculatedData.numLowShotsTele, 
        incapacitatedPercentage = lambda tm: tm.didBecomeIncapacitated,
        disabledPercentage = lambda tm: tm.didStartDisabled,
        liftoffPercentage = lambda tm: tm.didLiftoff, 
        baselineReachedPercentage = lambda tm: tm.didReachBaselineAuto,
        avgAgility = lambda tm: tm.rankAgility, 
        avgSpeed = lambda tm: tm.rankSpeed,
        avgGearGroundIntakesTele = lambda tm: tm.numGearGroundIntakesTele, 
        avgGearLoaderIntakesTele = lambda tm: tm.numGearLoaderIntakesTele,
        avgBallControl = lambda tm: tm.rankBallControl, 
        avgGearControl = lambda tm: tm.rankGearControl,
        avgDefense = lambda tm: tm.rankDefense if tm.rankDefense else None, 
        avgKeyShotTime = lambda tm: tm.calculatedData.avgKeyShotTime,
        avgHopperShotTime = lambda tm: tm.calculatedData.avgHopperShotTime,
        liftoffAbility = lambda tm: tm.calculatedData.liftoffAbility, 
        disfunctionalPercentage = lambda tm: tm.calculatedData.wasDisfunctional,
        avgGearsPlacedAuto = lambda tm: tm.calculatedData.numGearsPlacedAuto, 
        avgGearsPlacedTele = lambda tm: tm.calculatedData.numGearsPlacedTele,
        avgHoppersOpenedAuto = lambda tm: tm.numHoppersOpenedAuto, 
        avgHoppersOpenedTele = lambda tm: tm.numHoppersOpenedTele, avgGearsEjectedTele = lambda tm: tm.numGearsEjectedTele, 
        avgGearsFumbledTele = lambda tm: tm.numGearsFumbledTele,
        avgDrivingAbility = lambda tm: tm.calculatedData.drivingAbility)
    mapFuncForCalcAvgsForTeam(team, lambda f: calc.getStandardDeviationForDataFunctionForTeam(team, f), 
        sdLiftoffAbility = lambda tm: tm.calculatedData.liftoffAbility,
        sdHighShotsAuto = lambda tm: tm.calculatedData.numHighShotsAuto,
        sdHighShotsTele = lambda tm: tm.calculatedData.numHighShotsTele,
        sdLowShotsAuto = lambda tm: tm.calculatedData.numLowShotsAuto,
        sdLowShotsTele = lambda tm: tm.calculatedData.numLowShotsTele,
        sdGearsPlacedAuto = lambda tm: tm.calculatedData.numGearsPlacedAuto,
        sdGearsPlacedTele = lambda tm: tm.calculatedData.numGearsPlacedTele,
        sdBaselineReachedPercentage = lambda tm: tm.didReachBaselineAuto)
    cd.autoShootingPositions = calc.getAutoShootingPositions(team)
    calc.getAvgFuncForKeys(team, cd.avgGearsPlacedByLiftAuto, lambda tm: tm.gearsPlacedByLiftAuto)
    calc.getAvgFuncForKeys(team, cd.avgGearsPlacedByLiftTele, lambda tm: tm.gearsPlacedByLiftTele)
    cd.gearScoringPositionsAuto = calc.getGearScoringPositionsAuto(team)

def secondCalculationDict(team, calc):
    cd = team.calculatedData
    cd.predictedNumRPs = calc.predictedNumberOfRPs(team)
    cd.firstPickRotorBonusChance = calc.firstPickAllRotorsChance(team)
    try:
        cd.actualNumRPs = calc.getTeamRPsFromTBA(team)
        cd.actualSeed = calc.getTeamSeed(team)
    except Exception as e:
        print e
        if team in calc.cachedComp.teamsWithMatchesCompleted:
            cd.actualSeed = calc.cachedComp.actualSeedings.index(team) + 1
            cd.actualNumRPs = calc.actualNumberOfRPs(team)
    if team in calc.cachedComp.teamsWithMatchesCompleted:
        cd.RScoreDefense = calc.cachedComp.defenseZScores[team.number]
        cd.RScoreBallControl = calc.cachedComp.ballControlZScores[team.number]
        cd.RScoreGearControl = calc.cachedComp.gearControlZScores[team.number]
        cd.RScoreSpeed = calc.cachedComp.speedZScores[team.number]
        cd.RScoreAgility = calc.cachedComp.agilityZScores[team.number]
        cd.RScoreDrivingAbility = calc.cachedComp.drivingAbilityZScores[team.number]
        cd.predictedSeed = calc.cachedComp.predictedSeedings.index(team) + 1
    cd.firstPickAbility = calc.firstPickAbility(team)
    cd.overallSecondPickAbility = calc.overallSecondPickAbility(team)

def TIMDCalcDict(timd, calc):
    if (not calc.su.TIMCalculatedDataHasValues(timd.calculatedData)):
        timd.calculatedData = DataModel.CalculatedTeamInMatchData()
    team = calc.su.getTeamForNumber(timd.teamNumber)
    match = calc.su.getMatchForNumber(timd.matchNumber)
    c = timd.calculatedData
    c.numGearsPlacedAuto = calc.getTotalValueForValueDict(timd.gearsPlacedByLiftAuto)
    c.numGearsPlacedTele = calc.getTotalValueForValueDict(timd.gearsPlacedByLiftTele)
    c.avgKeyShotTime = calc.getAvgKeyShotTimeForTIMD(timd, 'Key')
    c.avgHopperShotTime = calc.getAvgKeyShotTimeForTIMD(timd, 'Hopper')
    c.numHighShotsTele = calc.weightFuelShotsForDataPoint(timd, match, timd.highShotTimesForBoilerTele)
    c.numHighShotsAuto = calc.weightFuelShotsForDataPoint(timd, match, timd.highShotTimesForBoilerAuto)
    c.numLowShotsTele = calc.weightFuelShotsForDataPoint(timd, match, timd.lowShotTimesForBoilerTele)
    c.numLowShotsAuto = calc.weightFuelShotsForDataPoint(timd, match, timd.lowShotTimesForBoilerAuto)
    c.liftoffAbility = calc.liftoffAbilityForTIMD(timd)
    c.drivingAbility = calc.drivingAbility(timd)
    c.wasDisfunctional = utils.convertFirebaseBoolean(timd.didStartDisabled + utils.convertFirebaseBoolean(timd.didBecomeIncapacitated))
    c.numRPs = calc.RPsGainedFromMatchForAlliance(team.number in match.redAllianceTeamNumbers, match)

def averageTeamDict(calc):
    a = calc.averageTeam
    mapFuncForCalcAvgsForTeam(calc.averageTeam, lambda f: calc.getAverageOfDataFunctionAcrossCompetition(f),
        avgHighShotsTele = lambda t: t.calculatedData.avgHighShotsTele,
        avgHighShotsAuto = lambda t: t.calculatedData.avgHighShotsAuto,
        avgLowShotsAuto = lambda t: t.calculatedData.avgLowShotsAuto,
        avgLowShotsTele = lambda t: t.calculatedData.avgLowShotsTele,
        baselineReachedPercentage = lambda t: t.calculatedData.baselineReachedPercentage,
        disabledPercentage = lambda t: t.calculatedData.disabledPercentage,
        incapacitatedPercentage = lambda t: t.calculatedData.incapacitatedPercentage,
        liftoffPercentage = lambda t: t.calculatedData.liftoffPercentage,
        avgGearsPlacedTele = lambda t: t.calculatedData.avgGearsPlacedTele,
        avgGearsPlacedAuto = lambda t: t.calculatedData.avgGearsPlacedAuto,
        avgAgility = lambda t: t.calculatedData.avgAgility,
        avgSpeed = lambda t: t.calculatedData.avgSpeed,
        avgBallControl = lambda t: t.calculatedData.avgBallControl,
        avgGearControl = lambda t: t.calculatedData.avgGearControl,
        avgDefense = lambda t: t.calculatedData.avgDefense,
        avgKeyShotTime = lambda t: t.calculatedData.avgKeyShotTime,
        liftoffAbility = lambda t: t.calculatedData.liftoffAbility)
    mapFuncForCalcAvgsForTeam(calc.averageTeam, lambda f: calc.getStandardDeviationOfDataFunctionAcrossCompetition(f),
        sdBaselineReachedPercentage = lambda t: t.calculatedData.baselineReachedPercentage,
        sdLiftoffAbility = lambda t: t.calculatedData.sdLiftoffAbility,
        sdGearsPlacedTele = lambda t: t.calculatedData.sdGearsPlacedTele,
        sdGearsPlacedAuto = lambda t: t.calculatedData.sdGearsPlacedAuto,
        sdHighShotsAuto = lambda t: t.calculatedData.sdHighShotsAuto,
        sdHighShotsTele = lambda t: t.calculatedData.sdHighShotsTele,
        sdLowShotsAuto = lambda t: t.calculatedData.sdLowShotsAuto,
        sdLowShotsTele = lambda t: t.calculatedData.sdLowShotsTele)

def matchDict(match, calc):
    if calc.su.matchIsCompleted(match):
        match.calculatedData.actualBlueRPs = calc.RPsGainedFromMatchForAlliance(True, match)
        match.calculatedData.actualRedRPs = calc.RPsGainedFromMatchForAlliance(False, match)
    match.calculatedData.predictedBlueScore = calc.predictedScoreForAllianceWithNumbers(match.blueAllianceTeamNumbers)
    match.calculatedData.predictedRedScore = calc.predictedScoreForAllianceWithNumbers(match.redAllianceTeamNumbers)
    match.calculatedData.sdPredictedBlueScore = calc.stdDevPredictedScoreForAllianceNumbers(match.blueAllianceTeamNumbers)
    match.calculatedData.sdPredictedRedScore = calc.stdDevPredictedScoreForAllianceNumbers(match.redAllianceTeamNumbers)
    match.calculatedData.fortyKilopascalChanceRed = calc.get40KilopascalChanceForAllianceWithNumbers(match.redAllianceTeamNumbers)
    match.calculatedData.fortyKilopascalChanceBlue = calc.get40KilopascalChanceForAllianceWithNumbers(match.blueAllianceTeamNumbers)
    match.calculatedData.allRotorsTurningChanceRed = calc.getAllRotorsTurningChanceForAllianceWithNumbers(match.redAllianceTeamNumbers)
    match.calculatedData.allRotorsTurningChanceBlue = calc.getAllRotorsTurningChanceForAllianceWithNumbers(match.blueAllianceTeamNumbers)
    match.calculatedData.blueWinChance = calc.winChanceForMatchForAllianceIsRed(match, False)
    match.calculatedData.redWinChance = calc.winChanceForMatchForAllianceIsRed(match, True)
    match.calculatedData.predictedBlueRPs = calc.predictedRPsForAllianceForMatch(False, match)
    match.calculatedData.predictedRedRPs = calc.predictedRPsForAllianceForMatch(True, match)

def mapFuncForCalcAvgsForTeam(team, func, **calcDatas):
    [team.calculatedData.__dict__.update({k : func(dataFunc)}) for k, dataFunc in calcDatas.items()]
