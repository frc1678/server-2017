import smtplib
import threading

emails = ['colindunger@yahoo.com', 'abhi@vemulapati.com', 'bryton@themoellers.net']
gmail_user = '1678programming@gmail.com'

class EmailThread(threading.Thread):
	def reportServerCrash(self, message):
		smtpserver = smtplib.SMTP("smtp.gmail.com",587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo()
		smtpserver.login(gmail_user, "Squeezecrush1")
		header = 'To:' + ', '.join(emails) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: Server Crash \n'
		msg = header + '\n' + message
		smtpserver.sendmail(gmail_user, emails, msg)
		smtpserver.close()