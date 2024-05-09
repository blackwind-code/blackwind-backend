from dotenv import load_dotenv
import pytest

load_dotenv()

from env import DATABASE_CONNECTION_STRING

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlmodel import Session
from infra.database import create_db_and_tables
from infra.mail import get_mail_session, get_system_mail_session
from service.auth_service import AuthService
from service.mail_service import MailService

test_db_engine = create_engine(DATABASE_CONNECTION_STRING, echo=True)
create_db_and_tables()

@contextmanager
def get_test_session():
    with Session(test_db_engine) as session:
        yield session

@contextmanager
@pytest.fixture
def auth_service():
    with (get_test_session() as db_session, get_mail_session() as mail_session, get_system_mail_session(mail_session) as sys_mail_session):
        mail_service = MailService(sys_mail_session)
        auth_service = AuthService(db_session, mail_service)
        yield auth_service

@pytest.mark.asyncio
async def test_AuthService(auth_service):
    new_user = await auth_service.register('username','example@dgist.ac.kr', 'asdf1234',202111111, 'SUS')
    assert 'username' == new_user.username

