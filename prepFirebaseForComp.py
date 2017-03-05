import DataModel
import firebaseCommunicator
import TBACommunicator
import utils
import time

############# Getting TBA Data ###################
#set to "<your initials>:TBA_communicator:0"

TBAC = TBACommunicator.TBACommunicator()
competition = DataModel.Competition()
competition.eventCode = TBAC.code
FBC = firebaseCommunicator.PyrebaseCommunicator()

FBC.JSONteams = TBAC.makeEventTeamsRequest()
FBC.JSONmatches = TBAC.makeEventMatchesRequest()
FBC.wipeDatabase()
FBC.addCurrentMatchToFirebase()
FBC.addTeamsToFirebase()
FBC.addMatchesToFirebase()
competition.updateTeamsAndMatchesFromFirebase()
FBC.addTIMDsToFirebase(competition.matches) #you need to create the matches and teams before you call this
