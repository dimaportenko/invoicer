from google_services import get_google_service


docs_service = get_google_service('docs', 'v1')

def get_document(document_id: str):

    if docs_service is None:
        return None

    # Retrieve the documents contents from the Docs service.
    document = docs_service.documents().get(documentId=document_id).execute()

    print('The title of the document is: {}'.format(document.get('title')))

    return document

def replace_template_values(document_id: str, params: dict[str, str]):

    if docs_service is None:
        return None

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

    result = docs_service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

    return result

