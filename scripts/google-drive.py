from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time as t
import os
import sys
import sqlite3

# LOAD DATABASE CONNECTION
conn = sqlite3.connect('fablab.db')
c = conn.cursor()


# Path to your service account key file
SERVICE_TOKEN = '/home/james/dev/fablabOS/keys/haystackos-dc31b0bd0f66.json'

# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Define spreadsheet ID
SPREADSHEET_ID = '11N06kLKveP6VyTIk2VxJnacKmY9VtWs409vxREhcjZ8'

# Community Labs spreadsheet ID
COMMUNITY_LABS = '1F8xa0fTDC7bzKB_Kg-IhkqxYHCErvnMz2JNEBkrla8I'

# Define range
RANGE = 'A1:I100'


def main():
    credentials = None
    if os.path.exists(SERVICE_TOKEN):
        print('Service token found.')
        credentials = Credentials.from_service_account_file(
            SERVICE_TOKEN, scopes=SCOPES)
    elif not credentials or not credentials.valid:
        print('Credentials not found.')
        sys.exit(1)  # Exit if credentials not found

    start_time = t.clock_gettime(t.CLOCK_MONOTONIC_RAW)
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=COMMUNITY_LABS, range=RANGE).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')
        else:
            print('Printing data from sheet...')
            print(f'Rows: {len(values)} rows found.')
            return values
    except HttpError as error:
        print(f'An error occurred: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()


# def update_workshops():
#     """Updates the workshops table in the database"""
#     sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE,)

# def get_workshops_by_month(month):
#     """Returns a list of workshops in a given month"""
#     pass

def get_cell_value(sheet, row, col):
    """Returns the value of a cell at a given row and column"""
    sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                       range=f"A{row}").execute().get("values")[0][0]
