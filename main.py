
from auth import google_auth
from drive_service import copy_invoice_template
from sheet_service import get_invoice_number
from docs_service import get_document, replace_template_values
from utils import getUADateWithDate

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

    document = get_document(google_creds=creds, document_id=document_copy_id)
    if (document != None):
        print(document.get('title'))

        params = {
            'invoiceNumber': str(invoice_number),
            'date': invoice_date,
            'ua_date': getUADateWithDate(invoice_date)
        }

        result = replace_template_values(document_id=document_copy_id, params=params, google_creds=creds)

        print(result)
        


if __name__ == "__main__": 
    main()

