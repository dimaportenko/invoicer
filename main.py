
from auth import google_auth
from invoices_db import get_invoice_number

from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import TEMPLATE_DOC_ID

def main(): 
    creds = google_auth()

    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    if (invoice_number == 0):
        invoice_number = get_invoice_number(creds)

    try:
        drive_service = build('drive', 'v3', credentials=creds)

        # doc_title = '_GoSource_invoice_{number}'.format(number = invoice_number)
        doc_title = f'_GoSource_invoice_{invoice_number}'
        body = {
            'name': doc_title,
        }
        # Call the Drive v3 API
        print(f'teplate id {TEMPLATE_DOC_ID}')
        drive_response = drive_service.files().copy(fileId=TEMPLATE_DOC_ID, body=body).execute()
        document_copy_id = drive_response.get('id')
        print(f'Copied document ID: {document_copy_id}')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


    # print(invoice_number)
    print('---')


if __name__ == "__main__": 
    main()

