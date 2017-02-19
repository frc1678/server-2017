from apns import APNs, Frame, Payload

apns = APNs(use_sandbox=True, cert_file='cert.pem', key_file='key.pem')

# Send a notification
token_hex = 'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87'
payload = Payload(alert="Hello World!", sound="default", badge=1)
apns.gateway_server.send_notification(token_hex, payload)