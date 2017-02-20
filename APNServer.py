from apns import APNs, Frame, Payload

apns = APNs(use_sandbox=True, cert_file='./apns-dev-cert.pem')

# Send a notification
token_hex = '1D6AA2EA9ED2EF31BBDB4976DDD6E3475D295281F4F3419E4D6B0FC3B8224C'
payload = Payload(alert="Hello World!", sound="default", badge=1)
apns.gateway_server.send_notification(token_hex, payload)