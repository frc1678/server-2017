import smtplib
import threading
from slackclient import SlackClient
import time
import pdb

sc = SlackClient('xoxp-49302180423-49316952386-140114605008-32492dbe60a2bb10d0f3d5cd92194ccc')

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
