
from auth import google_auth

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import SPREADSHEET_ID
    
RANGE = 'A1:Z100'

def main(): 
    # print("Hello World")
    creds = google_auth()

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()

        values = result.get('values', [])

        if not values:
            print("No data found")
            return

        for row in values:
            print(row)
            # print("%s %s %s %s %s" % (row[0], row[1], row[2], row[3], row[4]))


    except HttpError as err:
        print(err)


if __name__ == "__main__": 
    main()

