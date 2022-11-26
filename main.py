
from auth import google_auth
from invoices_db import get_invoice_number

from datetime import datetime


def main(): 
    # print("Hello World")
    creds = google_auth()

    invoice_number = 0
    invoice_date = datetime.today().strftime('%m/%d/%Y')
    print(invoice_date)

    if (invoice_number == 0):
        invoice_number = get_invoice_number(creds)

    print(invoice_number)
    print('---')


if __name__ == "__main__": 
    main()

