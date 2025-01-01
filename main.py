from drive_service import copy_invoice_template, export_pdf
from gmail_service import gmail_create_draft_with_attachment, gmail_create_message_with_attachment
from sheet_service import get_invoice_number, get_db_sheet, add_invoice_record_to_sheet
from docs_service import get_document, replace_template_values
from utils import getUADateWithDate
from datetime import datetime
from dateutil.relativedelta import relativedelta


def main(): 
    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    invoice_number = get_invoice_number()

    if (invoice_number is None):
        print("ERR!! Can't retrieve invoice number")
        return 0

    dataframe_db = get_db_sheet()
    if (dataframe_db.empty):
        print("ERR!! Can't retrieve db")
        return 0

    doc_title = dataframe_db['invoice_title'].iloc[0] + '_' + str(invoice_number)
    document_copy_id = copy_invoice_template(doc_title=doc_title)
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


    # get first value from pandas dataframe email_to column
    email_to = dataframe_db['email_to'].iloc[0]
    # get not empty values from email_cc column
    email_cc = dataframe_db[dataframe_db['email_cc'].notnull()]['email_cc'].values.tolist()
    email_cc_str = ','.join(email_cc)

    # Get the previous month date
    previous_month_date = datetime.today() - relativedelta(months=1)
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

    invoice_doc_link = f'https://docs.google.com/document/d/{document_copy_id}/edit'
    add_invoice_record_to_sheet({
        'invoice_number': invoice_number,
        'invoice_date': invoice_date,
        'invoice_doc': invoice_doc_link,
    })
        


if __name__ == "__main__": 
    main()

