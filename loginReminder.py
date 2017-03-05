import time
from slackclient import SlackClient
slack_token = os.environ["my_token"]
sc = SlackClient(slack_token)
loginReminderChannels = ["list", "of", "usernames"]

while(True):
	for person in loginReminderChannels:
		currentDay = time.strftime("%A")
		currentTime = str(time.strftime("%H:%M"))
		if 'Wednesday' in currentDay or 'Thursday' in currentDay:
			if currentTime == '18:30':
				sc.api_call(
				"chat.postMessage",
				channel = "@" + person,
				text = "Remember to login! :smiley:"
				)
			elif currentTime == '21:00':
				sc.api_call(
				"chat.postMessage",
				channel = "@" + person,
				text = "Remember to logout! :smiley:"
				)
		elif 'Saturday' in currentDay or 'Sunday' in currentDay:
			if currentTime == '9:00':
				sc.api_call(
				"chat.postMessage",
				channel = "@" + person,
				text = "Remember to login! :smiley:"
				)
			elif currentTime == '17:00':
				sc.api_call(
				"chat.postMessage",
				channel = "@" + person,
				text = "Remember to logout! :smiley:"
				)
	time.sleep(60)
