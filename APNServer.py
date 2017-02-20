from apns import APNs, Frame, Payload
import pyrebase as pyb
import pdb

apns = APNs(use_sandbox=True, cert_file='./apn-cert.pem')
config = {
		"apiKey": "mykey",
		"authDomain": "scouting-2017-5f51c.firebaseapp.com",
		"databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
		"storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyb.initialize_app(config)
fb = f.database()
def sendNoti(number, c, token):
	message = "Match " + str(number) + " is " + str(abs(number - c)) + " matches away!"
	payload = Payload(alert=message, sound="default", badge=1)
	apns.gateway_server.send_notification(token, payload)

def sendNotiForUsers(data):
	if data.get("data") == None: return
	currentMatchNum = int(data.get("data"))
	users = fb.child("AppTokens").get().val()
	[sendNotiForUser(u, currentMatchNum) for u in users.values()]

def sendNotiForUser(usr, currentMatchNum):
	token = usr["Token"]
	starred = usr.get("StarredMatches").values() if type(usr.get("StarredMatches")) == dict else usr.get("StarredMatches")
	observedMs = filter(lambda n: abs(currentMatchNum - n) <= 2, starred)
	print observedMs
	[sendNoti(n, currentMatchNum, token) for n in observedMs]

fb.child("currentMatchNum").stream(sendNotiForUsers)