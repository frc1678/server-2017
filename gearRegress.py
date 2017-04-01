#By Bryton Moeller (2015-2016)
import DataModel
import firebaseCommunicator
import Math
import pdb

PBC = firebaseCommunicator.PyrebaseCommunicator()
 
for k, v in PBC.firebase.child("TeamInMatchDatas").get().val().items():
	print v.get('superNotes')