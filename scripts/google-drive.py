from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import os
import sys
import sqlite3
import pprint
from sqlite3 import Error

# Path to database
DATABASE = 'fablab.db'

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
    sheet = setup_gsheets()
    values = get_gsheet_values(sheet, COMMUNITY_LABS, RANGE)
    for row in values:
        for cell in row:
            print(cell)


######################################
# GOOGLE SHEETS API HELPER FUNCTIONS #
######################################


def setup_gsheets():
    """Authenticates the Google Sheets API
    Returns: Credentials object"""
    credentials = None
    if os.path.exists(SERVICE_TOKEN):
        print('Service token found.')
        credentials = Credentials.from_service_account_file(
            SERVICE_TOKEN, scopes=SCOPES)
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


def get_gsheet_values(sheet, spreadsheet_id, range):
    """Returns a list of lists from a given spreadsheet"""
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    try:
        values = result.get('values', [])
        if not values:
            print('No data found.')
            sys.exit(1)
        else:
            return values
    except HttpError as error:
        print(f'An error occurred: {error}')
        sys.exit(1)

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

#############################
# DATABASE HELPER FUNCTIONS #
#############################


def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def insert_row(table, row):
    """Inserts a row into a given table"""
    conn = create_connection(DATABASE)
    try:
        c = conn.cursor()
        c.execute(f"""INSERT INTO {table} VALUES {row}""")
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


if __name__ == '__main__':
    main()
