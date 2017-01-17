import utils

def firstCalculationDict(team, c):
	cd = team.calculatedData
	cd.avgHighShotsTele =  c.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsTele)
	cd.avgHighShotsAuto = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numHighShotsAuto)
	cd.avgLowShotsAuto = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsAuto)
	cd.avgLowShotsTele = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.numLowShotsTele)
	cd.disabledPercentage = c.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didStartDisabled))
	cd.incapacitatedPercentage = c.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didBecomeIncapacitated))
	cd.liftoffPercentage = c.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didLiftoff))
	cd.avgGearsPlacedTele = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedTele)
	cd.avgGearsPlacedAuto = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedAuto)
	cd.avgAgility = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankAgility)
	cd.avgSpeed = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankSpeed)
	cd.avgBallControl = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankBallControl)
	cd.avgGearControl = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankGearControl)
	cd.avgDefense = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankDefense)		
	cd.avgKeyShotTime = c.boilerShotTimeFromKey(team)
	cd.liftoffAbility = c.getAverageForDataFunctionForTeam(team, lambda tm: tm.calculatedData.liftoffAbility)
	cd.sdLiftoffAbility = c.getStandardDeviationForDataFunctionForTeam(team, lambda tm: tm.calculatedData.liftoffAbility)
	 
def secondCalculationDict(team, c):
	cd = team.calculatedData
	cd.predictedNumRPs = c.predictedNumberOfRPs(team)
	cd.actualNumRPs = c.actualNumberOfRPs(team)
	cd.firstPickAbility = c.firstPickAbility(team)
	cd.overallSecondPickAbility = c.overallSecondPickAbility(team)
	cd.predictedSeed = c.cachedComp.predictedSeedings.index(team) + 1
	cd.actualSeed = c.cachedComp.actualSeedings.index(team) + 1
	cd.RScoreDefense = c.cachedComp.defenseZScores[team.number]
	cd.RScoreBallControl = c.cachedComp.ballControlZScores[team.number]
	cd.RScoreGearControl = c.cachedComp.gearControlZScores[team.number]
	cd.RScoreSpeed = c.cachedComp.defenseZScores[team.number]
	cd.RScoreAgility = c.cachedComp.agilityZScores[team.number]
