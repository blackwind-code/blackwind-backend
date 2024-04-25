import datetime
from typing import List
import uuid
from sqlmodel import Field, SQLModel

from infra.verify import generate_verify_token
from model.auth.role import Role
from model.auth.user import User

class DiscordUser(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    discord_user_id: int
    user: User = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    roles: List[Role] = Field(default=[])
    verify_token: str = Field(default_factory=generate_verify_token, index=True, nullable=False)