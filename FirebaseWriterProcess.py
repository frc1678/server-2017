import firebaseCommunicator
import multiprocessing
import DataModel

class FirebaseWriteObjectProcess(multiprocessing.Process):
	"""docstring for FirebaseWriteProcesser"""
	def __init__(self, o, PBC):
		super(FirebaseWriteObjectProcess, self).__init__()
		self.object = o
		self.PBC = PBC

	def run(self):
		if isinstance(self.object, DataModel.Team): self.PBC.addCalculatedTeamDataToFirebase(self.object)
		elif isinstance(self.object, DataModel.Match): self.PBC.addCalculatedMatchDataToFirebase(self.object)
		elif isinstance(self.object, DataModel.TeamInMatchData): self.PBC.addCalculatedTIMDataToFirebase(self.object)
