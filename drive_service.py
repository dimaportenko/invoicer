from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import TEMPLATE_DOC_ID

def copy_invoice_template(google_creds, invoice_number): 
    try:
        drive_service = build('drive', 'v3', credentials=google_creds)

        # doc_title = '_GoSource_invoice_{number}'.format(number = invoice_number)
        doc_title = f'_GoSource_invoice_{invoice_number}'
        body = {
            'name': doc_title,
        }
        # Call the Drive v3 API
        drive_response = drive_service.files().copy(fileId=TEMPLATE_DOC_ID, body=body).execute()
        document_copy_id = drive_response.get('id')

        return document_copy_id

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

