
from auth import google_auth
from drive_service import copy_invoice_template, export_pdf
from gmail_service import gmail_create_draft_with_attachment, gmail_create_message_with_attachment
from sheet_service import get_invoice_number
from docs_service import get_document, replace_template_values
from utils import getUADateWithDate

from datetime import datetime


def main(): 
    creds = google_auth()

    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    invoice_number = get_invoice_number(gauth_creds=creds)

    if (invoice_number == None):
        print("ERR!! Can't retrieve invoice number")
        return 0

    document_copy_id = copy_invoice_template(google_creds=creds, invoice_number=invoice_number)
    if (document_copy_id == None):
        print("ERR!! Can't retrieve invoice template")
        return 0

    print(document_copy_id)
    print('---')

    document = get_document(document_id=document_copy_id)
    if (document != None):
        title = document.get('title')
        print(title)

        params = {
            'invoiceNumber': str(invoice_number),
            'date': invoice_date,
            'ua_date': getUADateWithDate(invoice_date)
        }

        result = replace_template_values(document_id=document_copy_id, params=params)

        print(result)
        
        pfd_file = export_pdf(google_creds=creds, document_id=document_copy_id)

        pdf_file_path = f'./docs/{title}.pdf'
        if (pfd_file != None):
            # save io file to ./docs/{title}.pdf
            with open(pdf_file_path, 'wb') as f:
                f.write(pfd_file.getbuffer())


        if pdf_file_path == None:
            print("ERR!! Can't export pdf")
            return 0

        message = gmail_create_message_with_attachment(to="test@gmail.com",  subject="Test subject message", file=pdf_file_path)
        if message == None:
            print("ERR!! Can't create message")
            return 0

        gmail_create_draft_with_attachment(gauth_creds=creds, message=message)

if __name__ == "__main__": 
    main()

