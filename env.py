import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_CONNECTION_STRING = os.environ.get('DATABASE_CONNECTION_STRING')

SMTP_SERVER = os.environ.get('SMTP_SERVER')
MAIL_SYSTME_ADDRESS = os.environ.get('MAIL_SYSTEM_ADDRESS')
MAIL_SYSTEM_USERNAME = os.environ.get('MAIL_SYSTEM_USERNAME')
MAIO_SYSTEM_PASSWORD = os.environ.get('MAIL_SYSTEM_PASSWORD')

