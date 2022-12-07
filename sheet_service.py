import pandas as pd

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import SPREADSHEET_ID
from auth import google_auth
    
RANGE = 'A1:Z100'

def get_sheets_service():
    try:
        google_creds = google_auth()
        service = build('sheets', 'v4', credentials=google_creds)
        return service
    except HttpError as err:
        print(err)
        return None

# get sheets service object
sheets_service = get_sheets_service()

def get_db_sheet():
    if SPREADSHEET_ID == None or sheets_service is None:
        return pd.DataFrame()

    sheet = sheets_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()

    values = result.get('values', [])

    if not values:
        print("No data found")
        return pd.DataFrame()

    # print(values)

    # create dataframe and set fist line as column names
    df = pd.DataFrame(values)
    df.columns = df.iloc[0]
    df = df[1:] 
    return df
     

def get_invoice_number():

    df = get_db_sheet()
    if df is None:
        return 0

    df.Date = pd.to_datetime(df.Date)
    print(df["Date"].max())

    # print df where Date is not empty
    not_null_df = df[df["Date"].notnull() & df["Invoice #"].notnull()]

    # maximum invoice number + 1
    invoice_number = int(not_null_df["Invoice #"].max()) + 1
    print('--- invoice_number ---')
    print(invoice_number)
    
    return invoice_number

