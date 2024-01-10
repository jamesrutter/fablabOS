from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import time as t

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/home/james/dev/fablabOS/keys/haystackos-dc31b0bd0f66.json'

SPREADSHEET_ID = '11N06kLKveP6VyTIk2VxJnacKmY9VtWs409vxREhcjZ8'
RANGE = 'A1:I100'


def main():
    start_time = t.clock_gettime(t.CLOCK_MONOTONIC_RAW)
    creds = None
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

    service = build('sheets', 'v4', credentials=creds)
    auth_time = t.clock_gettime(t.CLOCK_MONOTONIC_RAW) - start_time
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    values = result.get('values', [])
    fetch_time = t.clock_gettime(t.CLOCK_MONOTONIC_RAW)

    if not values:
        print('No data found.')
    else:
        print('Printing data from sheet...')
        for row in values:
            print(f'{row[0]}')
        end_time = t.clock_gettime(t.CLOCK_MONOTONIC_RAW)
        print('Done.')
        # Print total time taken to authenticate and fetch data
        print(f'Time taken to authenticate: {auth_time}')
        print(f'Time taken to fetch data: {fetch_time - start_time}')
        print(
            f'Time taken to print data: {t.clock_gettime(t.CLOCK_MONOTONIC_RAW) - end_time}')
        print(
            f'Total time taken: {t.clock_gettime(t.CLOCK_MONOTONIC_RAW) - start_time}')


if __name__ == '__main__':
    main()
