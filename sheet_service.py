import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2.credentials import Credentials

from config import SPREADSHEET_ID
    
RANGE = 'A1:Z100'

def get_invoice_number(gauth_creds: Credentials):
    try:
        service = build('sheets', 'v4', credentials=gauth_creds)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()

        values = result.get('values', [])

        if not values:
            print("No data found")
            return

        # print(values)

        # create dataframe and set fist line as column names
        df = pd.DataFrame(values)
        df.columns = df.iloc[0]
        df = df[1:]
        # print(df.columns)

        df.Date = pd.to_datetime(df.Date)
        print(df["Date"].max())

        # print df where Date is not empty
        not_null_df = df[df["Date"].notnull() & df["Invoice #"].notnull()]

        # maximum invoice number + 1
        invoice_number = int(not_null_df["Invoice #"].max()) + 1
        print('--- invoice_number ---')
        print(invoice_number)
        
        return invoice_number

    except HttpError as err:
        print(err)
        return 0

