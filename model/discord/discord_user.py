from datetime import datetime
from typing import Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel

from infra.verify import generate_verify_token

class DiscordUser(SQLModel, table=True):
    __tablename__ = "discord_user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    discord_user_id: int
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    verify_token: str = Field(default_factory=generate_verify_token, index=True, nullable=False)
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="discord_user"
    )