import io

from tqdm import tqdm

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from auth import google_auth

from config import TEMPLATE_DOC_ID


def get_drive_service():
    try:
        google_creds = google_auth()
        service = build('drive', 'v3', credentials=google_creds)
        return service
    except HttpError as err:
        print(err)
        return None

# get drive service object
drive_service = get_drive_service()

def copy_invoice_template(doc_title: str):
    body = {
        'name': doc_title,
    }

    if drive_service is None:
        return None

    if TEMPLATE_DOC_ID is None:
        return None

    # Call the Drive v3 API
    drive_response = drive_service.files().copy(fileId=TEMPLATE_DOC_ID, body=body).execute()
    document_copy_id: str = drive_response.get('id')

    return document_copy_id


def export_pdf(document_id: str):
    if drive_service is None:
        return None
        
    request = drive_service.files().export_media(fileId=document_id,
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

    return file
