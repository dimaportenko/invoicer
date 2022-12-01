from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_document(google_creds, documentId):
    try:
        service = build('docs', 'v1', credentials=google_creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=documentId).execute()

        print('The title of the document is: {}'.format(document.get('title')))

        return document
    except HttpError as err:
        print(err)
        return None
