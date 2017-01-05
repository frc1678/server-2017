import DataModel
import firebaseCommunicator
import TBACommunicator
import utils
import time

############# Getting TBA Data ###################
 # set to "<your initials>:TBA_communicator:0"

TBAC = TBACommunicator.TBACommunicator()
competition = DataModel.Competition()
competition.eventCode = TBAC.code



def makeFakeDatabase():
	FBC = firebaseCommunicator.FirebaseCommunicator(competition)
	FBC.JSONteams = TBAC.makeEventTeamsRequest()
	FBC.JSONmatches = TBAC.makeEventMatchesRequest()
	FBC.wipeDatabase()
	FBC.addTeamsToFirebase()
	FBC.addMatchesToFirebase()
	competition.updateTeamsAndMatchesFromFirebase()
	FBC.addTIMDsToFirebase(competition.matches) #You need to create the matches and teams before you call this

makeFakeDatabase()