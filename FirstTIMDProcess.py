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
            c.numHighShotsTele = sum(map(lambda v: v['numShots'], self.highShotTimesForBoilerTele))
            c.numHighShotsAuto = sum(map(lambda v: v['numShots'], self.highShotTimesForBoilerAuto))
            c.numLowShotsTele = sum(map(lambda v: v['numShots'], self.lowShotTimesForBoilerTele))
            c.numLowShotsAuto  = sum(map(lambda v: v['numShots'], self.lowShotTimesForBoilerAuto))
            
            if not self.calculator.su.TIMCalculatedDataHasValues(
                    self.timd.calculatedData): self.timd.calculatedData = DataModel.CalculatedTeamInMatchData()
            c = self.timd.calculatedData
            
            c.wasDisfunctional = utils.convertFirebaseBoolean(self.timd.didGetDisabled) or utils.convertFirebaseBoolean(self.timd.didGetIncapacitated)
            self.calculatedTIMDsList.append(self.timd)            