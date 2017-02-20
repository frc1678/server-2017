from apns import APNs, Frame, Payload

apns = APNs(use_sandbox=True, cert_file='./newfile.pem')

# Send a notification
token_hex = '272FDC7F60D378414445AE371CB204E52A4A5FC50F262F2F08A9AD16E2765692'
payload = Payload(alert="Hello World!", sound="default", badge=1)
apns.gateway_server.send_notification(token_hex, payload)