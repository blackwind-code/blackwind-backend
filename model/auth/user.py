import uuid
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    username: str
    email: str
    password: str
    student_id: int
    department: str
    verified: bool = Field(default=False)