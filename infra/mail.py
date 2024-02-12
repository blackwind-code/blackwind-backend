import smtplib
from contextlib import contextmanager

from fastapi import Depends

from env import MAIL_SYSTEM_USERNAME, MAIO_SYSTEM_PASSWORD, SMTP_SERVER

def get_mail_session():
    with smtplib.SMTP_SSL(SMTP_SERVER) as server:
        yield server

def get_system_mail_session(mail_session: smtplib.SMTP = Depends(get_mail_session)):
    mail_session.login(MAIL_SYSTEM_USERNAME, MAIO_SYSTEM_PASSWORD)
    yield mail_session