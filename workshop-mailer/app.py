import re
import csv
import os
import sys
import logging
import argparse
import sqlite3

from smtplib import SMTP
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader


# WARNING: Environment variables are needed to be configured and set for this application to work.
# Run source ./env.sh to set the environment variables.
# See the README.md file for more information.

# TODO: Add command line argument parsing to allow for more flexibility.
# TODO: Pull data from a local database or Google Sheets.
# TODO: Get API key from LGL and pull data from LGL.


# Usage example
data = {
    'logo_url': 'https://rmumgcgthlkxvxhprzfl.supabase.co/storage/v1/object/public/haystack/logos/logo.png',
    'workshop_title': 'Community Labs Workshop',
    'instructor_name': 'James Rutter',
    'workshop_date': 'Saturday, January 20th',
    'workshop_time': '10:00am - 1:00pm',
    'workshop_location': 'Community Labs, 22 Church St., Deer Isle, ME 04627'
}

# Basic configuration of logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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
        logging.error('Environment variables were not set!')
        sys.exit(1)
    logging.info('Environment variables set')

    return app


# TODO: Add support for other file formats or sources of data. (e.g. Google Sheets or local database)
def get_emails(input_file: str) -> list[str]:
    """
    Retrieves a list of email addresses from a CSV file.

    Args:
        input_file (str): The path to the input CSV file. Other formats are not supported.

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
        logging.info(f'Emails retrieved! Number of emails: {len(emails)}')

    return emails


# TODO: Add DNS validation to check if the email address is valid.

def validate_email(email: str) -> bool:
    """
    Validates an email address.

    Args:
        email (str): An email address.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def get_workshop_students_from_db(db_path: str) -> list[dict[str, str]]:
    """
    Retrieves a list of workshop students from a local database.

    Args:
        db_path (str): The path to the local database.

    Returns:
        list[dict[str, str]]: A list of workshop students.
    """
    students = []
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        for row in rows:
            students.append({
                'name': row[0],
                'email': row[1],
                'phone': row[2],
                'address': row[3],
                'city': row[4],
                'state': row[5],
                'zip': row[6],
                'country': row[7],
                'workshop': row[8],
                'date': row[9],
                'time': row[10],
                'location': row[11],
                'instructor': row[12],
                'logo_url': row[13]
            })
        logging.info(
            f'Students retrieved! Number of students: {len(students)}')

    return students


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
    logging.info('Message constructed!')
    return msg


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
    logging.info('Template constructed!')
    return template.render(data)


def send_message(app: dict[str, str], msg: EmailMessage):
    try:
        with SMTP(app['host'], int(app['port'])) as server:
            server.starttls()  # Start TLS encryption
            server.login(app['account'], app['password'])
            server.send_message(msg)
            logging.info('Message sent!')
    except Exception as e:
        logging.error(e)


def parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Send emails to a list of recipients.')
    parser.add_argument('-i', '--input', type=str,
                        help='Path to the input CSV file.')
    parser.add_argument('-t', '--template', type=str,
                        help='Path to the HTML template file.')
    parser.add_argument('-d', '--data', type=str,
                        help='Path to the data file.', default=data)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    app = setup_environment()
    email_list = []
    if os.path.exists(args.input):
        email_list = get_emails(args.input)
    template = construct_email_template(args.template, args.data)
    msg = construct_email_message(email_list, template)
    # send_message(app, msg)


if __name__ == "__main__":
    main()
