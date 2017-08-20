import smtplib
import threading
from slackclient import SlackClient
import time
import pdb

sc = SlackClient('Slack Api')

#Sends slack message to listed users
def reportServerCrash(message):
	map(lambda u:
	sc.api_call(
		'chat.postMessage',
		channel = '@' + u,
		text = message
	), ['bimbunky', 'tesseract', 'peterc'])

#Sends slack message to listed user
def reportOverestimate(message):
	map(lambda u:
	sc.api_call(
		'chat.postMessage',
		channel = '@' + u,
		text = message
	), ['bimbunky'])
