from slackclient import SlackClient
import datetime
import time
def remind(message):
	sc = SlackClient("xoxp-49302180423-49316952386-140114605008-32492dbe60a2bb10d0f3d5cd92194ccc")
	map(lambda u: 
	sc.api_call(
		"chat.postMessage",
		channel="@" + u,
		text=message
	), ["bimbunky", "kylestach"])

remind("sick profile picture buddy.")
# while True:
# 	now = datetime.datetime.now()
# 	if now.weekday() in [5,6]:
# 		if (now.hour == 16 and now.minute >= 45) or (now.hour == 17 and now.minute <= 15):
# 			remind("Remember to sign out!")
# 		elif (now.hour == 8 and now.minute >= 55) or (now.hour == 9 and now.minute <= 15):
# 			remind("Remember to sign in!")
# 		time.sleep(18000)
# 	elif now.weekday() in [2,3]:
# 		if (now.hour == 20 and now.minute >= 45) or (now.hour == 21 and now.minute <= 15):
# 			remind("Remember to sign out!")
# 		elif (now.hour == 18 and now.minute >= 25) or (now.hour == 19 and now.minute <= 15):
# 			remind("Remember to sign in!")
# 		time.sleep(18000)
# 	time.sleep(90)