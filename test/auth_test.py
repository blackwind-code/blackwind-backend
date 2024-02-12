import pytest
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from service.auth_service import AuthService

test_db_engine = create_engine("sqlite:///test.db")
SQLModel.metadata.drop_all(test_db_engine, SQLModel.metadata.tables.values())
SQLModel.metadata.create_all(test_db_engine)


def get_test_session():
    with Session(test_db_engine) as session:
        yield session

@pytest.mark.asyncio
async def test_AuthService():
    db_session = get_test_session()
    auth_service = AuthService(next(db_session))

    user = await auth_service.register('psm','psm7177@naver.com', '1234', 1234, 'SUS')
    assert user.id is not None
    assert user.username == 'psm'
    assert user.email == 'psm7177@naver.com'
    assert user.student_id == 1234
    assert user.department == 'SUS'

