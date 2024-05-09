from typing import Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel

from infra.verify import generate_verify_token

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    username: str
    email: str
    password: str
    student_id: int
    department: str
    verify_token: str = Field(default_factory=generate_verify_token, index=True, nullable=False)
    verified: bool = Field(default=False)
    discord_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="discord_user.id")
    discord_user: Optional["DiscordUser"] = Relationship(back_populates="user")