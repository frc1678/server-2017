import DataModel
from firebaseCommunicator import PyrebaseCommunicator
import csv
from Math import Calculator


pbc = PyrebaseCommunicator()
 
timds = pbc.firebase.child('TeamInMatchDatas').get().val()
for key, timd in timds.items():
	superNotesVal = timd.get('superNotes')
	# if superNotesVal:
	# 	supNotes = superNotesVal.get('finalNotes') if superNotesVal.get('finalNotes') else superNotesVal.get('firstNotes')
	# 	timd['superNotes'] = supNotes
	print type(timd.get('superNotes'))
	print key
	if type(timd.get('superNotes')) == dict:
		print "DICT"
		pbc.firebase.child('TeamInMatchDatas').child(key).child('superNotes').set(timd.get('superNotes').get('firstNotes'))	

