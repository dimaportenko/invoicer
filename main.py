
from auth import google_auth
from drive_service import copy_invoice_template, export_pdf
from gmail_service import gmail_create_draft_with_attachment, gmail_create_message_with_attachment
from sheet_service import get_invoice_number, get_db_sheet
from docs_service import get_document, replace_template_values
from utils import getUADateWithDate

from datetime import datetime


def main(): 
    creds = google_auth()

    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    invoice_number = get_invoice_number()

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

        dataframe_db = get_db_sheet()
        if (dataframe_db.empty):
            print("ERR!! Can't retrieve db")
            return 0

        # get first value from pandas dataframe email_to column
        email_to = dataframe_db['email_to'].iloc[0]
        # get not empty values from email_cc column
        email_cc = dataframe_db[dataframe_db['email_cc'].notnull()]['email_cc'].values.tolist()
        email_cc_str = ','.join(email_cc)

        month_date = datetime.today().strftime('%B %Y')
        subject = f'Invoice #{invoice_number} {month_date}'

        body_template = dataframe_db['email_body'].iloc[0]
        # subject from template with {{invoiceNumber}} and {{date}}
        # Invoice #{{invoice_number}} {{date}} in attachment"
        msg_body = body_template.replace('{{invoice_number}}', str(invoice_number)).replace('{{date}}', month_date)
        # msg_body = body_template.format(invoice_number=invoice_number, date=month_date)

        message_params = {
            'To': email_to,
            'CC': email_cc_str,
            'Subject': subject, 
        }

        # message = gmail_create_message_with_attachment(to="",  subject="Test subject message", file=pdf_file_path)

        # msg_body = f'Invoice #{invoice_number}'
        message = gmail_create_message_with_attachment(params=message_params, file=pdf_file_path, msg_body=msg_body)

        print(message)
        if message == None:
            print("ERR!! Can't create message")
            return 0

        gmail_create_draft_with_attachment(gauth_creds=creds, message=message)

        


if __name__ == "__main__": 
    main()

