import multiprocessing
import warnings
import DataModel
import utils

class FirstTIMDProcess(multiprocessing.Process):
    def __init__(self, timd, calculatedTIMDsList, calculator):
        super(FirstTIMDProcess, self).__init__()
        self.timd = timd
        self.calculatedTIMDsList = calculatedTIMDsList
        self.calculator = calculator
        warnings.simplefilter('error', RuntimeWarning)

    def run(self):
        if (not self.calculator.su.timdIsCompleted(self.timd)):
            print "TIMD is not complete for team " + str(self.timd.teamNumber) + " in match " + str(self.timd.matchNumber)
            self.calculatedTIMDsList.append(self.timd)
        else:
            print "Beginning first calculations for team " + str(self.timd.teamNumber) + " in match " + str(self.timd.matchNumber)
            team = self.calculator.su.getTeamForNumber(self.timd.teamNumber)
            match = self.calculator.su.getMatchForNumber(self.timd.matchNumber)

            self.calculator.matches = filter(lambda m: not self.calculator.su.teamInMatch(team, m) == (self.timd.matchNumber != m.number), self.calculator.comp.matches)
            self.calculator.TIMDs = filter(lambda t: t.matchNumber in [m.number for m in self.calculator.matches], self.calculator.comp.TIMDs)

            if not self.calculator.su.TIMCalculatedDataHasValues(
                    self.timd.calculatedData): self.timd.calculatedData = DataModel.CalculatedTeamInMatchData()
            c = self.timd.calculatedData
            c.teleopShotAbility = self.calculator.getTIMDTeleopShotAbility(self.timd)
            c.highShotAccuracyTele = self.calculator.TIMDShotAccuracy(self.timd.numHighShotsMadeTele, self.timd.numHighShotsMissedTele)  # Checked

            c.highShotAccuracyAuto = self.calculator.TIMDShotAccuracy(self.timd.numHighShotsMadeAuto, self.timd.numHighShotsMissedAuto)  # Checked
            c.lowShotAccuracyTele = self.calculator.TIMDShotAccuracy(self.timd.numLowShotsMadeTele, self.timd.numLowShotsMissedTele)  # Checked
            c.lowShotAccuracyAuto = self.calculator.TIMDShotAccuracy(self.timd.numLowShotsMadeAuto, self.timd.numLowShotsMissedAuto)  # Checked
            c.siegeAbility = self.calculator.singleSiegeAbility(self.timd)
            c.autoAbility = self.calculator.autoAbility(self.timd)
            c.siegeConsistency = utils.convertFirebaseBoolean(self.timd.didChallengeTele) or utils.convertFirebaseBoolean(self.timd.didScaleTele)
            c.numRPs = self.calculator.RPsGainedFromMatchForTeam(team, match)
            c.numAutoPoints = self.calculator.autoAbility(self.timd)
            c.numScaleAndChallengePoints = c.siegeAbility  # they are the same
            c.highShotsAttemptedTele = self.timd.numHighShotsMadeTele + self.timd.numHighShotsMissedTele
            c.lowShotsAttemptedTele = self.timd.numLowShotsMadeTele + self.timd.numLowShotsMissedTele
            c.numBallsIntakedOffMidlineAuto = len(self.timd.ballsIntakedAuto) if self.timd.ballsIntakedAuto != None else 0
            c.numTimesSuccesfulCrossedDefensesAuto = self.calculator.numCrossingsForTIMD(self.timd, self.timd.timesSuccessfulCrossedDefensesAuto)
            c.numTimesFailedCrossedDefensesAuto = self.calculator.numCrossingsForTIMD(self.timd, self.timd.timesFailedCrossedDefensesAuto)
            c.numTimesSuccesfulCrossedDefensesTele = self.calculator.numCrossingsForTIMD(self.timd, self.timd.timesSuccessfulCrossedDefensesTele)
            c.numTimesFailedCrossedDefensesTele = self.calculator.numCrossingsForTIMD(self.timd, self.timd.timesFailedCrossedDefensesTele)
            c.crossingsForDefensePercentageAuto = utils.dictPercentage(c.numTimesSuccesfulCrossedDefensesAuto, c.numTimesFailedCrossedDefensesAuto)
            c.crossingsForDefensePercentageTele = utils.dictPercentage(c.numTimesSuccesfulCrossedDefensesTele, c.numTimesFailedCrossedDefensesTele)
            c.totalNumTimesCrossedDefensesAuto = self.calculator.totalCrossesInAutoForTIMD(self.timd)
            c.crossingTimeForDefenseAuto = self.calculator.valueCrossingsForTIMD(self.timd, self.timd.timesSuccessfulCrossedDefensesAuto)
            c.crossingTimeForDefenseTele = self.calculator.valueCrossingsForTIMD(self.timd, self.timd.timesSuccessfulCrossedDefensesTele)
            c.wasDisfunctional = utils.convertFirebaseBoolean(self.timd.didGetDisabled) or utils.convertFirebaseBoolean(self.timd.didGetIncapacitated)
            self.calculatedTIMDsList.append(self.timd)            