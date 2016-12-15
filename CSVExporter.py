# CSV Exporter, by Bryton 2/10/16
import utils


def TSVExportAll(comp):
	s = ""
	firstTeam = True
	with open('./dataExportAll.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in cd.keys():
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for value in cd.values():
				s += str(value) + "	"
			s += "\n"
		file.write(s)
		file.close()

def TSVExportCVR(comp):
	s = ""
	CVRKeys = ["RScoreDrivingAbility",	"disabledPercentage",	"numAutoPoints",	"sdLowShotsTele",	"sdHighShotsTele",	"actualSeed",	"incapacitatedPercentage",	"avgShotsBlocked",	"highShotAccuracyTele",	"sdShotsBlocked",	"siegeConsistency",	"disfunctionalPercentage",	"sdSiegeAbility",	"overallSecondPickAbility"]
	firstTeam = True
	with open('./dataExportCVR.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in CVRKeys:
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for key in CVRKeys:
				s += str(cd[key]) + "	"
			s += "\n"
		file.write(s)
		file.close()

def TSVExportMini(comp):
	s = ""
	MiniKeys = ["numAutoPoints", "actualSeed",	"siegeConsistency",	"disfunctionalPercentage", "avgDrivingAbility", "defensesCrossableAuto", "avgGroundIntakes", "pitNumberOfWheels"]
	firstTeam = True
	with open('./dataExportMini.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in MiniKeys:
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for key in MiniKeys:
				if key == 'pitNumberOfWheels':
					s += str(team.pitNumberOfWheels)
				else:
					s += str(cd[key]) + "	"
			s += "\n"
		file.write(s)
		file.close()

def TSVExport(comp, keys, name):
	s = ""
	MiniKeys = keys
	firstTeam = True
	with open('./TSVExport-' + name + '.tsv', 'w') as file:
		for team in comp.teams:
			cd = team.calculatedData.__dict__
			t = team.__dict__
			if firstTeam:
				firstTeam = False
				s += "number" + "	"
				for key in MiniKeys:
					s += key + "	"
				s += "\n"
			s += str(team.number) + "	"
			for key in MiniKeys:
				try:
					s += str(cd[key]) + "	"
				except:
					try:
						s += str(t[key]) + "	"
					except:
						print "*** TSV EXPORT ERROR ***\nKEY: " + key + " NOT FOUND ON A CALCULATED TEAM DATA, NOR ON A TEAM DATA"
			s += "\n"
		file.write(s)
		file.close()
def TSVExportSAC(comp):
	keys = ["disfunctionalPercentage","disabledPercentage", "incapacitatedPercentage", "firstPickAbility","overallSecondPickAbility","siegeAbility","siegeConsistency","challengePercentage","scalePercentage","RScoreDrivingAbility","avgDrivingAbility", "RScoreDefense","avgDefense", 'RScoreBallControl',"avgBallControl", "RScoreSpeed", "avgSpeed", "RScoreAgility", "avgAgility","RScoreTorque","avgTorque","autoAbility", "sdAutoAbility", "highShotAccuracyAuto", "avgLowShotsTele","avgHighShotsTele", "sdHighShotsTele","highShotAccuracyTele", "teleopShotAbility", "crossingsSuccessRateForDefenseTele","avgTimeForDefenseCrossTele", "crossingsSuccessRateForDefenseAuto"]
	TSVExport(comp, keys, "SAC")

def TSVExportCMP(comp): 
	keys = ["overallSecondPickAbility", "firstPickAbility", 	"actualSeed",	"actualNumRPs", "numAutoPoints", "RScoreDrivingAbility", "siegeAbility", 	"disfunctionalPercentage",	"defensesCrossableAuto","defensesCrossableTele","avgGroundIntakes", "RScoreSpeed", "RScoreAgility", "RScoreBallControl", "avgDrivingAbility", "avgSpeed", "avgAgility", "avgTorque", "avgDefense", "avgLowShotsAttemptedTele", "teleopShotAbility", "avgLowShotsAuto", "avgLowShotsTele", "avgHighShotsTele", 	"highShotAccuracyTele",	"breachPercentage",	"siegeConsistency",	"challengePercentage","pitProgrammingLanguage", "avgTimeForDefenseCrossTele", "avgTimeForDefenseCrossAuto", "autoAbility","autoAbilityExcludeD","autoAbilityExcludeLB","highShotAccuracyAuto","avgHighShotsAuto",  "RScoreDefense" 	 ,"RScoreTorque", "sdAutoAbility",	"avgFailedTimesCrossedDefensesTele",	"sdHighShotsTele",	"predictedNumRPs",	"sdMidlineBallsIntakedAuto",  "avgFailedTimesCrossedDefensesAuto", 	 "lowShotAccuracyAuto", 	 "avgHighShotsAttemptedTele", 	 "incapacitatedPercentage", 	 "predictedSeed",  "twoBallAutoAttemptedPercentage", 	 "predictedSuccessfulCrossingsForDefenseTele", 	 "avgNumTimesUnaffected", 	 "reachPercentage", 	 "crossingsSuccessRateForDefenseTele", 	 "slowedPercentage", 	 "avgBallsKnockedOffMidlineAuto", 	 "avgMidlineBallsIntakedAuto", 	 "crossingsSuccessRateForDefenseAuto", 	 "sdGroundIntakes", 	 "avgBallControl", "avgNumTimesBeached","sdHighShotsAuto",	"sdFailedDefenseCrossesTele",	"avgNumTimesSlowed",	"sdSiegeAbility",	"twoBallAutoAccuracy",	"lowShotAccuracyTele",	"sdTeleopShotAbility",	"sdFailedDefenseCrossesAuto",	"siegeAbility",	"sdSuccessfulDefenseCrossesTele",	"avgSuccessfulTimesCrossedDefensesTele",	"scalePercentage",	"disabledPercentage",		"avgShotsBlocked",	"sdBallsKnockedOffMidlineAuto",	"sdShotsBlocked",	"sdSuccessfulDefenseCrossesAuto",	"blockingAbility",	"twoBallAutoAttemptedPercentage",	"sdLowShotsTele",	"beachedPercentage",	"sdLowShotsAuto",	"unaffectedPercentage",	"avgSuccessfulTimesCrossedDefensesAuto"]
	TSVExport(comp, keys, "CHAMPS")