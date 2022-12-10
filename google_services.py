# import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import google_auth

def get_google_service(serviceName, version):
    try:
        google_creds = google_auth()
        service = build(serviceName=serviceName, version=version, credentials=google_creds)
        return service
    except HttpError as err:
        print(err)
        return None
