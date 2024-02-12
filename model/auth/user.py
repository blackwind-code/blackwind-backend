import uuid
from sqlmodel import Field, SQLModel

from infra.verify import generate_verify_token

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    username: str
    email: str
    password: str
    student_id: int
    department: str
    verify_token: str = Field(default_factory=generate_verify_token, index=True, nullable=False)
    verified: bool = Field(default=False)