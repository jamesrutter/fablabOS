from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from io import BytesIO
import requests
import os

# Authentication and setup
creds = Credentials.from_authorized_user_file(
    'path_to_credentials.json', ['https://www.googleapis.com/auth/drive'])
service = build('drive', 'v3', credentials=creds)


# Path to database
DATABASE = '../db/fablab.db'

# Path to your service account key file
SERVICE_TOKEN = '/home/james/dev/fablabOS/keys/haystackos-dc31b0bd0f66.json'

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']