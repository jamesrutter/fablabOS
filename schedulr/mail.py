import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content


def confirmation_email(user_email, user_name, reservation_details):

    # Setup the SendGrid client
    sg_client = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    # Change to your verified sender
    from_email = Email(email="fablab@haystack-mtn.org")
    to_email = To(email=user_email)  # Change to your recipient

    subject = "fablabOS: Reservation Confirmation"

    # Email body with dynamic content
    email_body = (
        f"Hello {user_name},\n\n"
        "Thank you for making a reservation at fablabOS. Here are your reservation details:\n\n"
        f"Reservation Details:\n{reservation_details}\n\n"
        "If you have any questions or need to make changes to your reservation, "
        "please contact us at fablab@haystack-mtn.org.\n\n"
        "Best regards,\n"
        "The fablabOS Team"
    )

    content = Content(mime_type="text/plain", content=email_body)
    message = Mail(from_email=from_email, to_emails=to_email,
                   subject=subject, plain_text_content=content)

    try:
        response = sg_client.send(message)
        print("Email sent successfully")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
    except Exception as e:
        print(f"An error occurred: {e}")
