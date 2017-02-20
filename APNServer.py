from apns import APNs, Frame, Payload
import pyrebase as pyb
import pdb

apns = APNs(use_sandbox=True, cert_file='./newfile.pem')
config = {
        "apiKey": "mykey",
        "authDomain": "scouting-2017-5f51c.firebaseapp.com",
        "databaseURL": "https://scouting-2017-5f51c.firebaseio.com/",
        "storageBucket": "scouting-2017-5f51c.appspot.com"
}

f = pyb.initialize_app(config)
fb = f.database()
# 272FDC7F60D378414445AE371CB204E52A4A5FC50F262F2F08A9AD16E2765692
def sendNoti(number, c, token):
	message = "Match " + str(number) + " is " + str(abs(number - c)) + " matches away!"
    payload = Payload(alert=message, sound="default", badge=1)
    apns.gateway_server.send_notification(token, payload)

def sendNotiForUsers(data):
	if data.get("data") == None: return
	currentMatchNum = int(data.get("data"))
	users = firebase.child("AppTokens").get().val()
	pdb.set_trace()
	[sendNotiForUser(u, currentMatchNum) for u in users]

def checkNotiForUser(usr, currentMatchNum):
	token = usr.get("Token")
	observedMs = filter(lambda n: abs(currentMatchNum - n) <= 2, usr.get("StarredMatches").values())
	[sendNoti(n, currentMatchNum, token) for n in observedMs]

fb.child("currentMatchNum").stream(sendNotiForUsers)