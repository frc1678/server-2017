import utils

def firstCalculationDict(team):
	return {
       		'avgHighShotsTele' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numHighShotsTele),
		    'avgHighShotsAuto' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numHighShotsAuto),
	        'avgLowShotsAuto' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numLowShotsAuto),
	        'avgLowShotsTele' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numLowShotsTele),
	        'disabledPercentage' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didStartDisabled)),
	        'incapacitatedPercentage' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didBecomeIncapacitated)),
			'liftoffPercentage' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didLiftoff)),
	        'avgGearsPlacedTele' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedTele),
	        'avgGearsPlacedAuto' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedAuto),
			'avgAgility' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankAgility),
			'avgSpeed' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankSpeed),
			'avgBallControl' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankBallControl),
			'avgGearControl' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.rankGearControl),
        	'avgKeyShotTime' : lambda : self.boilerShotTimeForKey(team),
       		'sdLiftoffPercentage' : lambda : self.getStandardDeviationForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didLiftoff)),
       		'liftoffAbility' : lambda : self.liftoffAbility(team) 
       }
