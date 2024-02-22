import uuid

from typing import Optional

from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=True)
    username: str
    email: str
    password: str

