import smtplib
from contextlib import contextmanager

from fastapi import Depends

from env import MAIL_SYSTEM_USERNAME, MAIL_SYSTEM_PASSWORD, SMTP_SERVER

@contextmanager
def get_mail_session():
    with smtplib.SMTP_SSL(SMTP_SERVER) as server:
        yield server

@contextmanager
def get_system_mail_session(mail_session: smtplib.SMTP = Depends(get_mail_session)):
    mail_session.login(MAIL_SYSTEM_USERNAME, MAIL_SYSTEM_PASSWORD)
    yield mail_session