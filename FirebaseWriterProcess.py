import firebaseCommunicator
import multiprocessing
import DataModel

class FirebaseWriteObjectProcess(multiprocessing.Process):
	"""docstring for FirebaseWriteProcesser"""
	def __init__(self, o, FBC):
		super(FirebaseWriteObjectProcess, self).__init__()
		self.object = o
		self.FBC = FBC
	def run(self):
		if isinstance(self.object, DataModel.Team): self.FBC.addCalculatedTeamDataToFirebase(self.object)
		elif isinstance(self.object, DataModel.Match): self.FBC.addCalculatedMatchDataToFirebase(self.object)
		elif isinstance(self.object, DataModel.TeamInMatchData): self.FBC.addCalculatedTIMDataToFirebase(self.object)