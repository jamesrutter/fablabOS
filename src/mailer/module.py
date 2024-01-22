import csv
import os
import sys
from smtplib import SMTP
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader


# WARNING: Environment variables are needed to be configured and set for this application to work.
# Run source env.sh to set the environment variables.
# See the README.md file for more information.

# TODO: Add command line argument parsing to allow for more flexibility.
# TODO: Add logging.
# TODO: Pull data from a database.

# Usage example
data = {
    'logo_url': 'https://rmumgcgthlkxvxhprzfl.supabase.co/storage/v1/object/public/haystack/logos/logo.png',
    'workshop_title': 'Community Labs Workshop',
    'instructor_name': 'James Rutter',
    'workshop_date': 'Saturday, January 20th',
    'workshop_time': '10:00am - 1:00pm',
    'workshop_location': 'Community Labs, 22 Church St., Deer Isle, ME 04627'
}


def setup_environment() -> dict[str, str]:
    """
    Sets up the environment variables needed for this application.
    """
    app = {}
    app['password'] = os.environ.get('APP_PASSWORD')
    app['account'] = os.environ.get('ACCOUNT_EMAIL')
    app['host'] = os.environ.get('SMTP_SERVER')
    app['port'] = os.environ.get('PORT')

    if app['password'] is None or app['account'] is None or app['host'] is None or app['port'] is None:
        print('Environment variables were not set!')
        sys.exit(1)
    print('\nEnvironment variables set, setup is complete!\n')
    return app


def get_emails(input_file: str) -> list[str]:
    """
    Retrieves a list of email addresses from a CSV file.

    Args:
        input_file (str): The path to the input CSV file.

    Returns:
        list[str]: A list of email addresses.
    """
    emails = []
    with open(input_file) as csvfile:
        reader = csv.reader(csvfile)
        # get index of column 'Pref. email'
        email_col_idx = next(reader).index('Pref. email')
        for row in reader:
            emails.append(row[email_col_idx])
        print(emails)

    return emails


def construct_email_message(address_list: list[str], email_template: str) -> EmailMessage:
    """
    Constructs an email message.

    Args:
        email_addresses (list[str]): A list of email addresses.

    Returns:
        EmailMessage: An email message.
    """
    email_list = address_list
    msg = EmailMessage()
    msg['Subject'] = 'Community Labs Workshop Memo'
    msg['From'] = 'James Rutter<fablab@haystack-mtn.org'
    msg['To'] = email_list
    msg.set_content(email_template, subtype='html')
    return msg


def send_message(app: dict[str, str], msg: EmailMessage):
    try:
        with SMTP(app['host'], int(app['port'])) as server:
            server.starttls()  # Start TLS encryption
            server.login(app['account'], app['password'])
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def construct_email_template(template_path, data) -> str:
    """
    Fills an HTML template with provided data using Jinja2.

    Args:
        template_path (str): The path to the HTML template file.
        data (dict): A dictionary containing the data to fill in the template.

    Returns:
        str: The filled HTML content.
    """
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_path)
    return template.render(data)


def main():
    app = setup_environment()
    email_list = []
    if os.path.exists('input.csv'):
        print('\nGetting emails from csv...\n')
        email_list = get_emails('input.csv')
    print('\nCreating email message...\n')
    template = construct_email_template('template.html', data)
    msg = construct_email_message(['jamesdavidrutter@gmail.com'], template)
    print(f'\nMessage Preview:\n{msg}')
    # print('\nSending emails...\n')
    send_message(app, msg)


if __name__ == "__main__":
    main()
