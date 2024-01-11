from utils.google import setup_gsheets
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
import sqlite3
from sqlite3 import Error
import os

# Path to database
DATABASE = os.path.join(os.path.dirname(
    os.path.dirname(__file__)), 'db', 'fablab.db')


# Define the SCOPES
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Community Labs spreadsheet ID
COMMUNITY_LABS = '1F8xa0fTDC7bzKB_Kg-IhkqxYHCErvnMz2JNEBkrla8I'

# Define range
WORKSHOPS = 'workshops!A1:I100'  # range for workshops sheet
INSTRUCTORS = 'instructors!A1:G100'  # range for instructors sheet

###################################
# GOOGLE SHEETS UTILITY FUNCTIONS #
###################################


def get_workshops():
    """Returns a list of workshops from a given spreadsheet\n
    Args:
    - sheets: Google Sheets Resources service object"""
    sheets = setup_gsheets()
    result = sheets.values().get(spreadsheetId=COMMUNITY_LABS, range=WORKSHOPS).execute()
    try:
        workshops = result.get('values', [])
        if not workshops:
            print('No data found.')
            return None
        else:
            return workshops
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def update_workshops():
    """Updates the workshops table in the database"""
    pass


def get_workshops_by_month(month):
    """Returns a list of workshops in a given month"""
    pass


def get_cell_value(sheet, row, col):
    """Returns the value of a cell at a given row and column"""
    sheet.values().get(spreadsheetId=COMMUNITY_LABS,
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


def process_and_insert_row(values):
    for row in values[1:]:  # Skip the first row (header)
        row.append('workshop')  # Add the event type
        insert_event_row(row)


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
