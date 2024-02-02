from infra.database import get_session
from service.auth_service import AuthService

test_db_engine = create_engine

engine = create_engine(DATABASE_CONNECTION_STRING, echo=True)


def test_AuthService():
    db_session = get_session()
    AuthService()

