#Last Updated: 8/31/17
from slackclient import SlackClient

sc = SlackClient('Slack Api')

#Sends slack message to listed user(s)
def reportServerCrash(message):
	map(lambda u:
	sc.api_call(
		'chat.postMessage',
		channel = '@' + u,
		text = message
	), ['users'])

#Sends slack message to listed user(s)
def reportOverestimate(message):
	map(lambda u:
	sc.api_call(
		'chat.postMessage',
		channel = '@' + u,
		text = message
	), ['users'])
