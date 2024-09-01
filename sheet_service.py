import pandas as pd

from config import SPREADSHEET_ID
from google_services import get_google_service
    
RANGE = 'A1:Z200'

# get sheets service object
sheets_service = get_google_service('sheets', 'v4')

def get_db_sheet():
    if SPREADSHEET_ID is None or sheets_service is None:
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

    # df.invoice_date = pd.to_datetime(df.invoice_date)
    # print(df["invoice_date"].max())

    # print df where Date is not empty
    not_null_df = df[df["invoice_date"].notnull() & df["invoice_number"].notnull()]

    # maximum invoice number + 1
    invoice_number = int(not_null_df["invoice_number"].max()) + 1
    print('--- invoice_number ---')
    print(invoice_number)
    
    return invoice_number

def get_next_invoice_record_row():
    df = get_db_sheet()
    if df is None:
        return 0

    not_null_df = df[df["invoice_date"].notnull() & df["invoice_number"].notnull()]

    # get last row number
    last_row = not_null_df.index[-1] + 2
    return last_row

# english alphabet array
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

def get_sheet_column_by_name(column_name):
    df = get_db_sheet()
    if df is None:
        return 0

    column = df.columns.get_loc(column_name)
    column_letter = alphabet[column]
    return column_letter

# add invoice record to the sheet
# params key names should be the same as in the sheet
def add_invoice_record_to_sheet(params):
    if sheets_service is None:
        return None

    # get next row number
    next_row = get_next_invoice_record_row()

    # get column names by params keys
    # iterate over params keys and get column letter by name
    columns = []
    for key in params.keys():
        column = get_sheet_column_by_name(key)
        columns.append(column)

    # create request body
    values = list(params.values())
    
    # data for batchUpdate request
    data = []
    for i in range(len(columns)):
        data.append({
            'range': f'{columns[i]}{next_row}',
            'values': [[values[i]]]
        })


    result = sheets_service.spreadsheets().values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body={
        "valueInputOption": "USER_ENTERED",
        "data": data
    }).execute()

    return result


if __name__ == '__main__':
    row_number = get_next_invoice_record_row()
    print(f'--- row_number --- {row_number}')

    column_number = get_sheet_column_by_name('invoice_number')
    print(f'--- column_letter --- {column_number}')

    invoice_doc_latter = get_sheet_column_by_name('invoice_doc')
    print(f'--- invoice_doc_latter --- {invoice_doc_latter}')

    print(f'--- alphabet --- {alphabet}')

    add_invoice_record_to_sheet({
        'invoice_number': 1,
        'invoice_date': '12/10/2022',
        'invoice_doc': 'https://www.google.com',
    })
