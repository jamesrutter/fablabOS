from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import os
import sys

# Absolute path to service account key file
SERVICE_TOKEN = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'keys', 'token.json')

# Define the SCOPES
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']

######################################
# GOOGLE SHEETS API HELPER FUNCTIONS #
######################################


def setup_gdrive():
    """Authenticates the Google Sheets API
    Returns: Drive resource object """
    credentials = None
    if os.path.exists(SERVICE_TOKEN):
        print("------------------------")
        print('Service token found.')
        creds = Credentials.from_service_account_file(
            SERVICE_TOKEN, scopes=DRIVE_SCOPES)
    elif not credentials or not credentials.valid:
        print('Credentials not found.')
        sys.exit(1)  # Exit if credentials not found
    try:
        drive: Resource = build('drive', 'v3', credentials=creds)
        return drive
    except HttpError as error:
        print(f'An error occurred: {error}')
        sys.exit(1)


def setup_gsheets():
    """Authenticates the Google Sheets API
    Returns: Sheet Resource object"""
    credentials = None
    if os.path.exists(SERVICE_TOKEN):
        print('Service token found.')
        credentials = Credentials.from_service_account_file(
            SERVICE_TOKEN, scopes=SHEETS_SCOPES)
    elif not credentials or not credentials.valid:
        print('Credentials not found.')
        sys.exit(1)  # Exit if credentials not found
    try:
        service: Resource = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        return sheet
    except HttpError as error:
        print(f'An error occurred: {error}')
        sys.exit(1)
