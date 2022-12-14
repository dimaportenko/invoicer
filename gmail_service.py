# [START gmail_create_draft_with_attachment]
from __future__ import print_function

import base64
import mimetypes
import os
from email.message import EmailMessage

from google_services import get_google_service


gmail_service = get_google_service(serviceName='gmail', version='v1')

def gmail_create_draft_with_attachment(message: EmailMessage):

    if message is None:
        print('ERR!! Can\'t create message')
        return None

    message_request = create_message_request_with_attachment(message)

    if gmail_service is None:
        print('ERR!! Can\'t create gmail service')
        return None

    draft = gmail_service.users().drafts().create(
        userId="me",
        body=message_request
    ).execute()
    print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')


def create_message_request_with_attachment(message: EmailMessage):
    
    if message is None:
        print('ERR!! Can\'t create message')
        return None

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_draft_request_body = {
        'message': {
            'raw': encoded_message
        }
    }

    return create_draft_request_body



def gmail_create_message_with_attachment(params: dict[str,str], msg_body: str, file: str):
    mime_message = EmailMessage()

    for key, value in params.items():
        mime_message[key] = value

    mime_message.set_content(msg_body)

    # guessing the MIME type
    type_subtype, _ = mimetypes.guess_type(file)
    if type_subtype is None:
        return None

    maintype, subtype = type_subtype.split('/')

    with open(file, 'rb') as fp:
        attachment_data = fp.read()

    filename = os.path.basename(file)

    mime_message.add_attachment(attachment_data, maintype, subtype, filename=filename)

    return mime_message

