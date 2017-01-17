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
            if not self.calculator.su.TIMCalculatedDataHasValues(
                self.timd.calculatedData): self.timd.calculatedData = DataModel.CalculatedTeamInMatchData() 
            team = self.calculator.su.getTeamForNumber(self.timd.teamNumber)
            match = self.calculator.su.getMatchForNumber(self.timd.matchNumber)    
            c = self.timd.calculatedData
            c.numHighShotsTele = self.calculator.weightFuelShotsForDataPoint(self.timd, match, self.timd.highShotTimesForBoilerTele)
            c.numHighShotsAuto = self.calculator.weightFuelShotsForDataPoint(self.timd, match, self.timd.highShotTimesForBoilerAuto)
            c.numLowShotsTele = self.calculator.weightFuelShotsForDataPoint(self.timd, match, self.timd.lowShotTimesForBoilerTele) 
            c.numLowShotsAuto = self.calculator.weightFuelShotsForDataPoint(self.timd, match, self.timd.lowShotTimesForBoilerAuto) 
            c.liftoffAbility = self.calculator.liftoffAbilityForTIMD(self.timd)           
            c.wasDisfunctional = utils.convertFirebaseBoolean(self.timd.didStartDisabled) or utils.convertFirebaseBoolean(self.timd.didBecomeIncapacitated)
            self.calculatedTIMDsList.append(self.timd)            