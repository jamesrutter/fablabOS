import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

sg_client = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

# Change to your verified sender
from_email = Email(email="fablab@haystack-mtn.org")
to_email = To(email="jamesdavidrutter@gmail.com")  # Change to your recipient
subject = "fablabOS: Reservation Confirmation"
content = Content(mime_type="text/plain", content="This is a test email.")
message = Mail(from_email=from_email, to_emails=to_email,
               subject=subject, plain_text_content=content)

# Get a JSON-ready representation of the Mail object
message_json = message.get()

# Send an HTTP POST request to /mail/send
response = sg_client.send(message)
print(response.status_code)
print(response.headers)
