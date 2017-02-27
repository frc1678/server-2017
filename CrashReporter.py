import smtplib
import threading
from slackclient import SlackClient
import time
import pdb
def reportServerCrash(message):
	sc = SlackClient("xoxp-49302180423-49316952386-140114605008-32492dbe60a2bb10d0f3d5cd92194ccc")
	map(lambda u:
	sc.api_call(
		"chat.postMessage",
		channel="@" + u,
		text=message
	), ["bimbunky", "tesseract", "rytonbay", "sam", "peterc"])

