from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_document(google_creds, document_id: str):
    try:
        service = build('docs', 'v1', credentials=google_creds)

        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=document_id).execute()

        print('The title of the document is: {}'.format(document.get('title')))

        return document
    except HttpError as err:
        print(err)
        return None

def replace_template_values(document_id: str, params: dict[str, str], google_creds):
    try:
        service = build('docs', 'v1', credentials=google_creds)

        requests = []

        for key, value in params.items():
            requests.append({
                'replaceAllText': {
                    'containsText': {
                        'text': f'{{{key}}}',
                        'matchCase': True
                    },
                    'replaceText': value
                }
            })

        result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

        return result

    except HttpError as err:
        print(err)
        return None

