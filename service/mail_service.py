
from fastapi import Depends
from env import MAIL_SYSTME_ADDRESS

from infra.mail import get_system_mail_session


class MailService:
    def __init__(self, sys_mail_session = Depends(get_system_mail_session)) -> None:
        self.mail_session = sys_mail_session

    async def send_mail(self, mail_to, message):
        self.mail_session.sendmail(MAIL_SYSTME_ADDRESS, mail_to, message)