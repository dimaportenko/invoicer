import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
TEMPLATE_DOC_ID = os.getenv('TEMPLATE_DOC_ID')

