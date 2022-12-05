import io

from tqdm import tqdm

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


from config import TEMPLATE_DOC_ID

def copy_invoice_template(google_creds, invoice_number: int): 
    try:
        drive_service = build('drive', 'v3', credentials=google_creds)

        # doc_title = '_GoSource_invoice_{number}'.format(number = invoice_number)
        doc_title = f'_GoSource_invoice_{invoice_number}'
        body = {
            'name': doc_title,
        }
        # Call the Drive v3 API
        if TEMPLATE_DOC_ID != None:
            drive_response = drive_service.files().copy(fileId=TEMPLATE_DOC_ID, body=body).execute()
            document_copy_id: str = drive_response.get('id')

            return document_copy_id

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')

    return None

def export_pdf(google_creds, document_id: str):
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=google_creds)

        # pylint: disable=maybe-no-member
        request = service.files().export_media(fileId=document_id,
                                               mimeType='application/pdf')
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        progressBar = tqdm(total=100)
        while done is False:
            status, done = downloader.next_chunk()
            progress = int(status.progress() * 100)

            print(F'Download {progress}.')
            progressBar.update(progress)

        progressBar.close()


    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file
