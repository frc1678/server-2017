import utils
import pdb

def firstCalculationDict(team, calc):
	cd = team.calculatedData
	cd.avgHighShotsTele =  calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsTele)
	cd.avgHighShotsAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsAuto)
	cd.avgLowShotsAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsAuto)
	cd.avgLowShotsTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsTele)
	cd.disabledPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didStartDisabled))
	cd.incapacitatedPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didBecomeIncapacitated))
	cd.liftoffPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didLiftoff))
	cd.baselineReachedPercentage = calc.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didReachBaselineAuto))
	cd.avgGearsPlacedTele = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedTele)
	cd.avgGearsPlacedAuto = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedAuto)
	cd.avgAgility = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankAgility)
	cd.avgSpeed = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankSpeed)
	cd.avgBallControl = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankBallControl)
	cd.avgGearControl = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankGearControl)
	cd.avgDefense = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankDefense)
	cd.avgKeyShotTime = calc.boilerShotTimeFromKey(team)
	cd.liftoffAbility = calc.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.liftoffAbility)
	cd.sdLiftoffAbility = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.liftoffAbility)
	cd.sdGearsPlacedTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedTele)
	cd.sdGearsPlacedAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedAuto)
	cd.sdHighShotsAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsAuto)
	cd.sdHighShotsTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsTele)
	cd.sdLowShotsAuto = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsAuto)
	cd.sdLowShotsTele = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsTele)
	cd.sdBaselineReachedPercentage = calc.getStandardDeviationForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didReachBaselineAuto))
	cd.disfunctionalPercentage = cd.disabledPercentage + cd.incapacitatedPercentage

def secondCalculationDict(team, calc):
	cd = team.calculatedData
	cd.predictedNumRPs = calc.predictedNumberOfRPs(team)
	cd.actualNumRPs = calc.actualNumberOfRPs(team)
	cd.firstPickAbility = calc.firstPickAbility(team)
	cd.overallSecondPickAbility = calc.overallSecondPickAbility(team)
	cd.predictedSeed = calc.cachedComp.predictedSeedings.index(team) + 1
	cd.actualSeed = calc.cachedComp.actualSeedings.index(team) + 1
	cd.RScoreDefense = calc.cachedComp.defenseZScores[team.number]
	cd.RScoreBallControl = calc.cachedComp.ballControlZScores[team.number]
	cd.RScoreGearControl = calc.cachedComp.gearControlZScores[team.number]
	cd.RScoreSpeed = calc.cachedComp.defenseZScores[team.number]
	cd.RScoreAgility = calc.cachedComp.agilityZScores[team.number]

def averageTeamDict(calc):
	a = calc.averageTeam.calculatedData
	a.avgHighShotsTele =  calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgHighShotsTele)
	a.avgHighShotsAuto = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgHighShotsAuto)
	a.avgLowShotsAuto = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgLowShotsAuto)
	a.avgLowShotsTele = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.avgLowShotsTele)
	a.baselineReachedPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.baselineReachedPercentage)
	a.disabledPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.disabledPercentage)
	a.incapacitatedPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.incapacitatedPercentage)
	a.liftoffPercentage = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.liftoffPercentage)
	a.avgGearsPlacedTele = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgGearsPlacedTele)
	a.avgGearsPlacedAuto = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgGearsPlacedAuto)
	a.avgAgility = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgAgility)
	a.avgSpeed = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgSpeed)
	a.avgBallControl = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgBallControl)
	a.avgGearControl = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgGearControl)
	a.avgDefense = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgDefense)
	a.avgKeyShotTime = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.avgKeyShotTime)
	a.liftoffAbility = calc.getAverageOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.liftoffAbility)
	a.sdLiftoffAbility = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdLiftoffAbility)
	a.sdGearsPlacedTele = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.sdGearsPlacedTele)
	a.sdGearsPlacedAuto = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.sdGearsPlacedAuto)
	a.sdHighShotsAuto = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdHighShotsAuto)
	a.sdHighShotsTele = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdHighShotsTele)
	a.sdLowShotsAuto = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdLowShotsAuto)
	a.sdLowShotsTele = calc.getStandardDeviationOfDataFunctionAcrossCompetition(lambda t: t.calculatedData.sdLowShotsTele)
