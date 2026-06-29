import argparse
import os

from drive_service import copy_invoice_template, export_pdf
from gmail_service import gmail_create_draft_with_attachment, gmail_create_message_with_attachment
from sheet_service import get_invoice_number, get_db_sheet, add_invoice_record_to_sheet
from docs_service import get_document, replace_template_values
from utils import getUADateWithDate
from config import TEMPLATE_DOC_ID, TEMPLATE_DOC_ID_SIGNED
from datetime import datetime


def main(signed=False, no_draft=False, download=False, no_track=False):
    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    invoice_number = get_invoice_number(increment=not no_track)

    if (invoice_number is None):
        print("ERR!! Can't retrieve invoice number")
        return 0

    dataframe_db = get_db_sheet()
    if (dataframe_db.empty):
        print("ERR!! Can't retrieve db")
        return 0

    template_id = TEMPLATE_DOC_ID_SIGNED if signed else TEMPLATE_DOC_ID
    if (template_id is None):
        print("ERR!! Template id is not configured")
        return 0

    doc_title = dataframe_db['invoice_title'].iloc[0] + '_' + str(invoice_number)
    document_copy_id = copy_invoice_template(doc_title=doc_title, template_id=template_id)
    if (document_copy_id is None):
        print("ERR!! Can't retrieve invoice template")
        return 0

    print(document_copy_id)
    print('---')

    document = get_document(document_id=document_copy_id)
    if (document is None):
        print("ERR!! Can't retrieve document")
        return 0

    title = document.get('title')
    print(title)

    invoice_total = dataframe_db['invoice_total'].iloc[0]

    params = {
        'invoiceNumber': str(invoice_number),
        'date': invoice_date,
        'ua_date': getUADateWithDate(invoice_date),
        'invoice_total': invoice_total
    }

    result = replace_template_values(document_id=document_copy_id, params=params)

    print(result)
    
    pdf_file = export_pdf(document_id=document_copy_id)
    if pdf_file is None:
        print("ERR!! Can't retrieve pdf file")
        return 0

    pdf_file_path = f'./docs/{title}.pdf'
    with open(pdf_file_path, 'wb') as f:
        f.write(pdf_file.getbuffer())


    if pdf_file_path is None:
        print("ERR!! Can't export pdf")
        return 0

    if download:
        downloads_path = os.path.expanduser(f'~/Downloads/{title}.pdf')
        with open(downloads_path, 'wb') as f:
            f.write(pdf_file.getbuffer())
        print(f'Saved to {downloads_path}')


    if no_draft:
        print('Skipping email draft creation')
    else:
        create_draft(dataframe_db, invoice_number, pdf_file_path)

    if no_track:
        print('Skipping invoice record tracking')
    else:
        invoice_doc_link = f'https://docs.google.com/document/d/{document_copy_id}/edit'
        add_invoice_record_to_sheet({
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'invoice_doc': invoice_doc_link,
        })


def create_draft(dataframe_db, invoice_number, pdf_file_path):
    # get first value from pandas dataframe email_to column
    email_to = dataframe_db['email_to'].iloc[0]
    # get not empty values from email_cc column
    email_cc = dataframe_db[dataframe_db['email_cc'].notnull()]['email_cc'].values.tolist()
    email_cc_str = ','.join(email_cc)

    # Get the previous month date
    # comment - relativedelta(months=1) to have current month not previous
    previous_month_date = datetime.today() # - relativedelta(months=1)
    month_date = previous_month_date.strftime('%B %Y')
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
    if message is None:
        print("ERR!! Can't create message")
        return 0

    gmail_create_draft_with_attachment(message=message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate an invoice.')
    parser.add_argument('--signed', action='store_true',
                        help='Use the signed invoice template (TEMPLATE_DOC_ID_SIGNED).')
    parser.add_argument('--no-draft', action='store_true',
                        help="Don't create the Gmail draft.")
    parser.add_argument('--download', action='store_true',
                        help='Also save the final PDF into ~/Downloads.')
    parser.add_argument('--no-track', action='store_true',
                        help="Don't increment the invoice number or add a record to the sheet.")
    args = parser.parse_args()

    main(signed=args.signed, no_draft=args.no_draft, download=args.download,
         no_track=args.no_track)

