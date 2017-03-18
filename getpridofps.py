import firebaseCommunicator
import DataModel

p = firebaseCommunicator.PyrebaseCommunicator()
p.initializeFirebase()
comp = DataModel.Competition(p)
comp.updateTeamsAndMatchesFromFirebase()
comp.updateTIMDsFromFirebase()
for t in comp.TIMDs:
	timd = p.firebase.child('TeamInMatchDatas').child(str(t.teamNumber) + "Q" + str(t.matchNumber)).get().val()
	if not timd: continue
	if 'SuperNotes' in timd.keys():
		print str(t.teamNumber) + "Q" + str(t.matchNumber)
		p.firebase.child("TeamInMatchDatas").child(str(t.teamNumber) + "Q" + str(t.matchNumber)).child('SuperNotes').remove()