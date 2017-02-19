import utils
import pdb

def firstCalculationDict(team, calc):
	cd = team.calculatedData
	cd.avgHighShotsTele =  calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsTele)
	cd.avgHighShotsAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsAuto)
	cd.avgLowShotsAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsAuto)
	cd.avgLowShotsTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsTele)
	cd.disabledPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.didStartDisabled)
	cd.incapacitatedPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.didBecomeIncapacitated)
	cd.liftoffPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.didLiftoff)
	cd.baselineReachedPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.didReachBaselineAuto)
	cd.avgGearsPlacedTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedTele)
	cd.avgGearsPlacedAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedAuto)
	cd.avgAgility = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankAgility)
	cd.avgSpeed = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankSpeed)
	cd.avgBallControl = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankBallControl)
	cd.avgGearControl = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankGearControl)
	cd.avgDefense = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankDefense)
	cd.avgKeyShotTime = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.avgKeyShotTime)
	cd.liftoffAbility = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.liftoffAbility)
	cd.sdLiftoffAbility = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.liftoffAbility)
	cd.sdGearsPlacedTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedTele)
	cd.sdGearsPlacedAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedAuto)
	cd.sdHighShotsAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsAuto)
	cd.sdHighShotsTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsTele)
	cd.sdLowShotsAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsAuto)
	cd.sdLowShotsTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsTele)
	cd.sdGearsPlacedAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedAuto)
	cd.sdGearsPlacedTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedTele)
	cd.sdBaselineReachedPercentage = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didReachBaselineAuto))
	cd.disfunctionalPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.wasDisfunctional)
	cd.avgGearsPlacedAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedAuto)
	cd.avgGearsPlacedTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numGearsPlacedTele)
	cd.avgHoppersOpenedAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.numHoppersOpenedAuto)
	cd.avgHoppersOpenedTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.numHoppersOpenedTele)
	cd.avgGearsEjectedTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsEjectedTele)
	cd.avgGearsFumbledTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsFumbledTele)
	cd.avgDrivingAbility = calc.drivingAbility(team)
	cd.autoShootingPositions = calc.getAutoShootingPositions(team)
	cd.gearScoringPositionsAuto = calc.getGearScoringPositionsAuto(team)
	calc.getAvgFuncForKeys(team, cd.avgGearsPlacedByLiftAuto, lambda tm: tm.gearsPlacedByLiftAuto, calc.lifts)
	calc.getAvgFuncForKeys(team, cd.avgGearsPlacedByLiftTele, lambda tm: tm.gearsPlacedByLiftTele, calc.lifts)

def secondCalculationDict(team, calc):
	cd = team.calculatedData
	cd.predictedNumRPs = calc.predictedNumberOfRPs(team)
	cd.actualNumRPs = calc.actualNumberOfRPs(team)
	cd.firstPickRotorBonusChance = calc.firstPickAllRotorsChance(team)
	try:
		cd.predictedSeed = calc.cachedComp.predictedSeedings.index(team) + 1
		cd.actualNumRPs = calc.getTeamRPsFromTBA(team)
		cd.actualSeed = calc.getTeamSeed(team)
	except:
		cd.actualSeed = calc.cachedComp.actualSeedings.index(team) + 1
		cd.actualNumRPs = calc.actualNumberOfRPs(team)
	cd.RScoreDefense = calc.cachedComp.defenseZScores[team.number]
	cd.RScoreBallControl = calc.cachedComp.ballControlZScores[team.number]
	cd.RScoreGearControl = calc.cachedComp.gearControlZScores[team.number]
	cd.RScoreSpeed = calc.cachedComp.speedZScores[team.number]
	cd.RScoreAgility = calc.cachedComp.agilityZScores[team.number]
	cd.RScoreDrivingAbility = calc.cachedComp.drivingAbilityZScores[team.number]
	cd.firstPickAbility = calc.firstPickAbility(team)
	cd.overallSecondPickAbility = calc.overallSecondPickAbility(team)

	

def averageTeamDict(calc):
	a = calc.averageTeam.calculatedData
	a.avgHighShotsTele = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgHighShotsTele)
	a.avgHighShotsAuto = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgHighShotsAuto)
	a.avgLowShotsAuto = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgLowShotsAuto)
	a.avgLowShotsTele = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgLowShotsTele)
	a.baselineReachedPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.baselineReachedPercentage)
	a.disabledPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.disabledPercentage)
	a.incapacitatedPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.incapacitatedPercentage)
	a.liftoffPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.liftoffPercentage)
	a.sdBaselineReachedPercentage = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.baselineReachedPercentage)
	a.avgGearsPlacedTele = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgGearsPlacedTele)
	a.avgGearsPlacedAuto = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgGearsPlacedAuto)
	a.avgAgility = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgAgility)
	a.avgSpeed = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgSpeed)
	a.avgBallControl = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgBallControl)
	a.avgGearControl = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgGearControl)
	a.avgDefense = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgDefense)
	a.avgKeyShotTime = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgKeyShotTime)
	a.liftoffAbility = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.liftoffAbility)
	a.sdLiftoffAbility = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdLiftoffAbility)
	a.sdGearsPlacedTele = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdGearsPlacedTele)
	a.sdGearsPlacedAuto = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdGearsPlacedAuto)
	a.sdHighShotsAuto = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdHighShotsAuto)
	a.sdHighShotsTele = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdHighShotsTele)
	a.sdLowShotsAuto = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdLowShotsAuto)
	a.sdLowShotsTele = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdLowShotsTele)
	print("Completed first calcs for team " + str(calc.averageTeam.number))

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
