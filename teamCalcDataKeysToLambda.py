import utils

def firstCalculationDict(team):
	return {
       		'avgHighShotsTele' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numHighShotsTele),
		    'avgHighShotsAuto' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numHighShotsAuto),
	        'avgLowShotsAuto' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numLowShotsAuto),
	        'avgLowShotsTele' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numLowShotsTele),
	        'disabledPercentage' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didStartDisabled)),
	        'incapacitatedPercentage' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: utils.convertFirebaseBoolean(tm.didBecomeIncapacitated)),
	        'avgGearsPlacedTele' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedTele),
	        'avgGearsPlacedAuto' : lambda : self.getAverageForDataFunctionForTeam(team, lambda tm: tm.numGearsPlacedAuto)
        }
	