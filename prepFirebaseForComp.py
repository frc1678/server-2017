import DataModel
import firebaseCommunicator
import TBACommunicator
import utils
import time

############# Getting TBA Data ###################
#Set to "<your initials>:TBA_communicator:0"

TBAC = TBACommunicator.TBACommunicator()
FBC = firebaseCommunicator.PyrebaseCommunicator()
FBC.initializeFirebase()
competition = DataModel.Competition(FBC)
competition.eventCode = TBAC.code
competition.FBC.JSONteams = TBAC.makeEventTeamsRequest()
competition.FBC.JSONmatches = TBAC.makeEventMatchesRequest()
competition.FBC.wipeDatabase()
competition.FBC.addCurrentMatchToFirebase()
competition.FBC.addTeamsToFirebase()
competition.FBC.addMatchesToFirebase()
competition.updateTeamsAndMatchesFromFirebase()
competition.FBC.addTIMDsToFirebase(competition.matches) #You need to create the matches and teams before you call this
