from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import os
import sys
import sqlite3
from sqlite3 import Error

# Path to database
DATABASE = '../db/fablab.db'

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
    for row in values[1:]:
        row.append('workshop')
        insert_event_row(row)


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


def update_workshops():
    """Updates the workshops table in the database"""
    pass


def get_workshops_by_month(month):
    """Returns a list of workshops in a given month"""
    pass


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


def insert_event_row(row):
    """Inserts a row into the event table"""
    print(f"Inserting row: {row} ... ")
    conn = create_connection(DATABASE)
    c = conn.cursor()
    query = """INSERT INTO events 
               (date_start, time_start, time_end, event_name, fee_reg_amount, fee_facilitator_amount, max_participants, min_participants, event_description, event_type) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    try:
        c.execute(query, row)
        conn.commit()
        conn.close()
        print('Row inserted successfully.')
    except Error as e:
        print(e)
        conn.close()


def process_row(row):
    """Processes a row from the Google Sheet"""
    date = row[0]
    time_start = row[1]
    time_end = row[2]
    event_name = row[3]
    fee_reg_amount = row[4]
    fee_facilitator_amount = row[5]
    max_participants = row[6]
    min_participants = row[7]
    event_description = row[8]
    row = (date, time_start, time_end, event_name, fee_reg_amount,
           fee_facilitator_amount, max_participants, min_participants, event_description)
    insert_event_row(row)


if __name__ == '__main__':
    main()
