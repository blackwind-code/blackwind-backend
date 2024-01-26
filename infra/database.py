from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from model.auth.user import User

from env import DATABASE_CONNECTION_STRING

engine = create_engine(DATABASE_CONNECTION_STRING, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)