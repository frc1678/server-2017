#By Bryton Moeller (2015-2016)
import DataModel
import firebaseCommunicator
import Math
import pdb

PBC = firebaseCommunicator.PyrebaseCommunicator()
PBC.initializeFirebase()
comp = DataModel.Competition(PBC)
comp.updateTeamsAndMatchesFromFirebase()
comp.updateTIMDsFromFirebase()
calculator = Math.Calculator(comp)
print calculator.cachedComp.teamsWithMatchesCompleted()