#Last Updated: 8/26/17
import utils
import DataModel
import pdb
import traceback

def mapFuncForCalcAvgsForTeam(team, func, **calcDatas):		
	[team.calculatedData.__dict__.update({k : func(dataFunc)}) for k, dataFunc in calcDatas.items()]

def firstCalculationDict(team, calc):
    cd = team.calculatedData
    mapFuncForCalcAvgsForTeam(team, lambda f: calc.getAverageForDataFunctionForTeam(team, f),
	scoutDataPoints = lambda tm: tm.calculatedData.scoutDataPoints,
	#repeat for all scout and super data points for auto and tele
        )
    mapFuncForCalcAvgsForTeam(team, lambda f: calc.getStandardDeviationForDataFunctionForTeam(team, f),
	sdImportantTeleDataPoint = lambda tm: tm.calculatedData.ImportantTeleDataPoint,
        #repeat for all main tele data points (2017 was high shot, low shot, didLiftOff)
	)
    mapFuncForCalcAvgsForTeam(team, lambda f: calc.getRecentAverageForDataFunctionForTeam(team, f),
        lfmDisabledPercentage = lambda tm : tm.didStartDisabled,
        lfmScoutDataPoints = lambda tm: tm.ScoutDataPoints,
	#same data as first one, just lfm
	#add driverAbility
        )
    #year-specific, get main ways of scoring, 2017:
    '''cd.autoShootingPositions = calc.getAutoShootingPositions(team)
    calc.getAvgFuncForKeys(team, cd.avgGearsPlacedByLiftAuto, lambda tm: tm.gearsPlacedByLiftAuto)
    calc.getAvgFuncForKeys(team, cd.avgGearsPlacedByLiftTele, lambda tm: tm.gearsPlacedByLiftTele)
    cd.gearScoringPositionsAuto = calc.getGearScoringPositionsAuto(team)'''

def Rscorecalcs(team, calc):
    cd = team.calculatedData
    cd.RScoreDefense = calc.cachedComp.defenseZScores[team.number]
    cd.RScoreBallControl = calc.cachedComp.ballControlZScores[team.number]
    cd.RScoreGearControl = calc.cachedComp.gearControlZScores[team.number]
    cd.RScoreSpeed = calc.cachedComp.speedZScores[team.number]
    cd.RScoreAgility = calc.cachedComp.agilityZScores[team.number]
    cd.avgDrivingAbility = calc.drivingAbilityForTeam(team)
    # cd.lfmAvgDrivingAbility = calc.recentDrivingAbilityForTeam(team)

def secondCalculationDict(team, calc):
    cd = team.calculatedData
    cd.predictedNumRPs = calc.predictedNumberOfRPs(team)
    #change for year
    # 2017: cd.firstPickRotorBonusChance = calc.firstPickAllRotorsChance(team)
    try:
        cd.actualNumRPs = calc.getTeamRPsFromTBA(team)
        cd.actualSeed = calc.getTeamSeed(team)
    except Exception as e:
        if team in calc.cachedComp.actualSeedings:
            cd.actualSeed = calc.cachedComp.actualSeedings.index(team) + 1
            cd.actualNumRPs = calc.actualNumberOfRPs(team)
    if team in calc.cachedComp.teamsWithMatchesCompleted:
        cd.RScoreDrivingAbility = calc.cachedComp.drivingAbilityZScores[team.number]
        cd.predictedSeed = calc.cachedComp.predictedSeedings.index(team) + 1
    cd.firstPickAbility = calc.firstPickAbility(team)
    cd.allRotorsAbility = calc.allRotorsAbility(team)

def TIMDCalcDict(timd, calc):
    if (not calc.su.TIMCalculatedDataHasValues(timd.calculatedData)):
        timd.calculatedData = DataModel.CalculatedTeamInMatchData()
    team = calc.su.getTeamForNumber(timd.teamNumber)
    match = calc.su.getMatchForNumber(timd.matchNumber)
    c = timd.calculatedData
    c.mainDataPointsAutoAndTele = calc.getTotalValueForValueDict(timd.mainDataPointForAutoAndTele)
    c.mainDataPointsTimed = calc.getAvgKeyShotTimeForTIMD(timd, 'location')
    c.numHighShotsTele = calc.weightFuelShotsForDataPoint(timd, match, 'teleopFuelHigh', timd.highShotTimesForBoilerTele)
    c.numHighShotsAuto = calc.weightFuelShotsForDataPoint(timd, match, 'autoFuelHigh', timd.highShotTimesForBoilerAuto)
    c.numLowShotsTele = calc.weightFuelShotsForDataPoint(timd, match, 'teleopFuelLow', timd.lowShotTimesForBoilerTele)
    c.numLowShotsAuto = calc.weightFuelShotsForDataPoint(timd, match, 'autoFuelLow', timd.lowShotTimesForBoilerAuto)
    c.liftoffAbility = calc.liftoffAbilityForTIMD(timd)
    c.wasDisfunctional = utils.convertFirebaseBoolean(timd.didStartDisabled + utils.convertFirebaseBoolean(timd.didBecomeIncapacitated))
    c.disfunctionalPercentage = utils.convertFirebaseBoolean(timd.didStartDisabled) + 0.5 * utils.convertFirebaseBoolean(timd.didBecomeIncapacitated)
    c.numRPs = calc.RPsGainedFromMatchForAlliance(team.number in match.redAllianceTeamNumbers, match)

def averageTeamDict(calc):
    a = calc.averageTeam
    mapFuncForCalcAvgsForTeam(calc.averageTeam, lambda f: calc.getAverageOfDataFunctionAcrossCompetition(f),
	dataPoint = lambda t: t.calculatedData.dataPoint,
	#again, repeat for all data points
	)
    mapFuncForCalcAvgsForTeam(calc.averageTeam, lambda f: calc.getStandardDeviationOfDataFunctionAcrossCompetition(f),
	sdMainScoringMethods = lambda t: t.calculatedData.sdMainScoringMethod,
        )

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
