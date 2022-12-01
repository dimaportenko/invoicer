
from auth import google_auth
from drive_service import copy_invoice_template
from sheet_service import get_invoice_number
from docs_service import get_document

from datetime import datetime


def main(): 
    creds = google_auth()

    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    if (invoice_number == 0):
        invoice_number = get_invoice_number(creds)

    document_copy_id = copy_invoice_template(google_creds=creds, invoice_number=invoice_number)
    print(document_copy_id)
    print('---')

    document = get_document(google_creds=creds, documentId=document_copy_id)
    if (document != None):
        print(document.get('title'))


if __name__ == "__main__": 
    main()

